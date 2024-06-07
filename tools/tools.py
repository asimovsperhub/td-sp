import datetime
import json
import os
import random
import sys
from importlib import reload
from pprint import pformat
import re
from textrank4zh import TextRank4Keyword, TextRank4Sentence

sys.path.insert(
    0,
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from crawldata_spider.tools.db import MysqlDb, Db
from crawldata_spider.tools import redis_cli

target_url = "http://www.baidu.com"
proxy_host = random.choice(
    ['http-dynamic.xiaoxiangdaili.com', 'http-dynamic-S02.xiaoxiangdaili.com', 'http-dynamic-S03.xiaoxiangdaili.com',
     'http-dynamic-S04.xiaoxiangdaili.com'])
proxy_port = 10030
# 949484192264507392:W7NgW3PO
proxy_username = '950210861799460864'
proxy_pwd = 'NvPqqONn'


def get_proxy():
    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host": proxy_host,
        "port": proxy_port,
        "user": proxy_username,
        "pass": proxy_pwd,
    }

    proxies = {
        'http': proxyMeta,
        'https': proxyMeta,
    }

    return proxies


def filterHtmlTag(htmlstr):
    '''
    过滤html中的标签
    '''
    # 兼容换行
    s = htmlstr.replace('\r\n', '\n')
    s = htmlstr.replace('\r', '\n')

    # 规则
    # re.I 忽略大小写
    re_cdata = re.compile('//<!\[CDATA\[[^>]*//\]\]>', re.I)  # 匹配CDATA
    re_script = re.compile('<\s*script[^>]*>[\S\s]*?<\s*/\s*script\s*>', re.I)  # script
    re_style = re.compile('<\s*style[^>]*>[\S\s]*?<\s*/\s*style\s*>', re.I)  # style
    re_br = re.compile('<br\\s*?\/??>', re.I)  # br标签换行
    re_strong = re.compile('<strong\\s*?\/??>', re.I)  # strong
    re_p = re.compile('<\/p>', re.I)  # p标签换行
    re_h = re.compile('<[\!|/]?\w+[^>]*>', re.I)  # HTML标签
    re_comment = re.compile('<!--[^>]*-->')  # HTML注释
    re_hendstr = re.compile('^\s*|\s*$')  # 头尾空白字符
    re_lineblank = re.compile('[\t\f\v ]*')  # 空白字符
    re_linenum = re.compile('\n+')  # 连续换行保留1个

    # 处理
    s = re_cdata.sub('', s)  # 去CDATA
    s = re_script.sub('', s)  # 去script
    s = re_style.sub('', s)  # 去style
    s = re_br.sub('\n', s)  # br标签换行
    # s = re_strong.sub('',s)
    s = re_p.sub('\n', s)  # p标签换行
    s = re_h.sub('', s)  # 去HTML标签
    s = re_comment.sub('', s)  # 去HTML注释
    s = re_lineblank.sub('', s)  # 去空白字符
    s = re_linenum.sub('\n', s)  # 连续换行保留1个
    s = re_hendstr.sub('', s)  # 去头尾空白字符

    # 替换实体
    s = replaceCharEntity(s)

    return s


def replaceCharEntity(htmlStr):
    '''
      替换html中常用的字符实体
      使用正常的字符替换html中特殊的字符实体
      可以添加新的字符实体到CHAR_ENTITIES 中
      CHAR_ENTITIES是一个字典前面是特殊字符实体  后面是其对应的正常字符
      :param htmlStr:
      '''
    CHAR_ENTITIES = {'nbsp': ' ', '160': ' ',
                     'lt': '<', '60': '<',
                     'gt': '>', '62': '>',
                     'amp': '&', '38': '&',
                     'quot': '"', '34': '"', }
    re_charEntity = re.compile(r'&#?(?P<name>\w+);')
    sz = re_charEntity.search(htmlStr)
    while sz:
        entity = sz.group()  # entity全称，如>
        key = sz.group('name')  # 去除&;后的字符如（" "--->key = "nbsp"）    去除&;后entity,如>为gt
        try:
            htmlStr = re_charEntity.sub(CHAR_ENTITIES[key], htmlStr, 1)
            sz = re_charEntity.search(htmlStr)
        except KeyError:
            # 以空串代替
            htmlStr = re_charEntity.sub('', htmlStr, 1)
            sz = re_charEntity.search(htmlStr)
    return htmlStr


def repalceFont(htmlstr):
    # 兼容换行
    s = htmlstr.replace('\r\n', '\n')
    s = htmlstr.replace('\r', '\n')
    re_font = re.compile('@"<(?!br).*?>"', re.I)  # 匹配非br

    s = re_font.sub('', s)  # 去非br
    s = replaceCharEntity(s)
    return s


"""
jieba >= 0.35
numpy >= 1.7.1
networkx >= 1.9.1
"""


def text_abstract(text: str) -> str:
    try:
        reload(sys)
        sys.setdefaultencoding('utf-8')
    except:
        pass
    tr4w = TextRank4Keyword()

    tr4w.analyze(text=text, lower=True, window=10)

    tr4s = TextRank4Sentence()
    tr4s.analyze(text=text, lower=True, source='all_filters')

    abstract = []
    for item in tr4s.get_key_sentences(num=7, sentence_min_len=6):
        cont = item.sentence
        cont.replace("（", "").replace("）", "")
        cont = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', cont)
        abstract.append(cont)
    if len(abstract) > 5:
        ab = ",".join(abstract[5:7]).replace(" ", "")
    elif 3 <= len(abstract) <= 5:
        ab = ",".join(abstract[3:5]).replace(" ", "")
    else:
        ab = ",".join(abstract).replace(" ", "")
    return ab


def get_json(json_str):
    """
    @summary: 取json对象
    ---------
    @param json_str: json格式的字符串
    ---------
    @result: 返回json对象
    """

    try:
        return json.loads(json_str) if json_str else {}
    except Exception as e1:
        return {}


def dumps_json(data, indent=4, sort_keys=False):
    """
    @summary: 格式化json 用于打印
    ---------
    @param data: json格式的字符串或json对象
    ---------
    @result: 格式化后的字符串
    """
    try:
        if isinstance(data, str):
            data = get_json(data)

        data = json.dumps(
            data,
            ensure_ascii=False,
            indent=indent,
            skipkeys=True,
            sort_keys=sort_keys,
            default=str,
        )

    except Exception as e:
        data = pformat(data)

    return data


def format_sql_value(value):
    if isinstance(value, str):
        value = value.strip()

    elif isinstance(value, (list, dict)):
        value = dumps_json(value, indent=None)

    elif isinstance(value, (datetime.date, datetime.time)):
        value = str(value)

    elif isinstance(value, bool):
        value = int(value)

    return value


def list2str(datas):
    """
    列表转字符串
    :param datas: [1, 2]
    :return: (1, 2)
    """
    data_str = str(tuple(datas))
    data_str = re.sub(",\)$", ")", data_str)
    return data_str


mdb = Db("42.193.247.183", "tender")


# 定时task
def set_sub_redis():
    wxdata = {}
    subdata = {}
    _ = [subdata.setdefault(i[0], []).append({"type": i[1], "city": i[2], "keywords": i[3]}) for i in
         mdb.search("select user_id,type,location,keywords  from member_subscribe;") if i]
    _ = [wxdata.setdefault(i[1], i[0]) for i in mdb.search(" select main_id,open_id   from  sys_wx_user;") if i]
    for k, v in wxdata.items():
        wxdata[k] = subdata.get(v)
    redis_cli.set_cache("subscribeWx", wxdata)
    redis_cli.set_cache("subscribe", subdata)


def parseWx_sub():
    # parse
    data = []
    sb = redis_cli.get_cache("subscribeWx")
    if sb:
        for k, v in sb.items():
            if v:
                for i in v:
                    open_id = k
                    type = i.get("type")
                    city = i.get("city")
                    keywords = i.get("keywords")
                    data.append((open_id, type, city, keywords))
    return data


def parse_sub():
    # parse
    data = []
    sb = redis_cli.get_cache("subscribe")
    if sb:
        for k, v in sb.items():
            if v:
                for i in v:
                    user_id = k
                    type = i.get("type")
                    city = i.get("city")
                    keywords = i.get("keywords")
                    if type and city and keywords:
                        data.append((user_id, type, city, keywords))
    return data


if __name__ == '__main__':
    # from bs4 import BeautifulSoup
    # html = "中标候选人公示\n投资项目统一代码：2211-441900-04-02-310151\n工程编码（标段编码）：E4419000748006417001001\n招标编号：SJASJI12300067\n投资项目名称：天涯亭农贸综合市场\n招标项目名称：天涯亭农贸综合市场\n工程（标段）名称：天涯亭农贸综合市场\n招标方式：公开招标\n招标场所：东莞市公共资源交易中心\n建设单位：东莞市石碣镇城中社区居民委员会\n招标单位：东莞市石碣镇城中社区居民委员会\n招标代理：广东睿德项目管理有限公司\n监督部门：东莞市石碣镇住房和城乡建设局\n最高报价：4,523,755.14元"
    # re_cdata = re.search("%s.*?" % "候选", html)
    # if re_cdata:
    #     print(re_cdata)
    set_sub_redis()
    sb = redis_cli.get_cache("subscribe")
    wxsb = parseWx_sub()
    for i in wxsb:
        print(i)
    # for k,v in wxsb.items():
    #     print(k,v)
    for i in parse_sub():
        print(i)
    # for i in  parseWx_sub():
    #     print(i)
