import datetime
import time
import random
import re
import feapder
from feapder import Item
from lxml import etree
from urllib.parse import quote,unquote

class AirSpiderCgjs(feapder.AirSpider):
    '''
                       函数入口
                        :return:
               '''
    def start_requests(self):

        task_list=[
                  {'科技标准与建筑节能': [{'建设科技': 'http://zjj.sz.gov.cn/ztfw/jzjn/jskj2017/index.html'}, {'建材管理': 'http://zjj.sz.gov.cn/ztfw/jzjn/jcgl2017/index.html'}, {'装配式建筑': 'http://zjj.sz.gov.cn/ztfw/jzjn/zjgl2017/index.html'}, {'建设工程标准规范管理': 'http://zjj.sz.gov.cn/ztfw/jzjn/gfgl/index.html'}]},
                   {'工程造价服务': [{'合同与计价实务': 'http://zjj.sz.gov.cn/ztfw/gcjs/jjsw/index.html'}, {'专业研究': 'http://zjj.sz.gov.cn/ztfw/gcjs/zyyj/index.html'}, {'图书资料': 'http://zjj.sz.gov.cn/ztfw/gcjs/tszl/index.html'}, {'资料下载': 'http://zjj.sz.gov.cn/ztfw/gcjs/zlxz/index.html'}]},
                   {'工程检测信息': [{'检测资质': 'http://zjj.sz.gov.cn/ztfw/gcjs/jczz/index.html'}, {'业务流程': 'http://zjj.sz.gov.cn/ztfw/gcjs/ywlc/index.html'}, {'见证卡办理': 'http://zjj.sz.gov.cn/ztfw/gcjs/jzkbl/index.html'}, {'下载中心': 'http://zjj.sz.gov.cn/ztfw/gcjs/xzzx/index.html'}, {'房屋安全信息资料库': 'http://zjj.sz.gov.cn/ztfw/gcjs/qyxx/fwaq/index.html'}]},
                   ]
        for task in task_list:
            for key,values in task.items():
                for value in values:
                    for k,url in value.items():
                        if k in ['图书资料', '检测资质', '业务流程', '见证卡办理']:
                            yield feapder.Request(url, callback=self.parse2, verify=False, method="GET", lx1=key, lx2=k)

                        else:
                            yield feapder.Request(url, verify=False, method="GET", lx1=key, lx2=k,count=1)

        # task_list={'建设工程消防': [{'消防设计审查结果': 'http://zjj.sz.gov.cn/ztfw/gcjs/xffw/xfsjscjg/index.html'}, {'消防验收审查结果': 'http://zjj.sz.gov.cn/ztfw/gcjs/xffw/xfysjg/index.html'}, {'消防验收备案结果': 'http://zjj.sz.gov.cn/ztfw/gcjs/xffw/xfysbajg/index.html'}]}
        # for key, values in task_list.items():
        #     for value in values:
        #         for k, url in value.items():
        #             yield feapder.Request(url,callback=self.parse3,verify=False, method="GET", lx1=key, lx2=k)



    def download_midware(self, request):
        '''
                          下载中间件
                            :return:
                   '''
        request.headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}


        return request

    def parse(self, request, response):
        '''
                            解析页面
                            :return:
                   '''
        url=request.url
        count=request.count

        lx1=request.lx1
        lx2=request.lx2
        html = response.text
        html = etree.HTML(html)
        last_page=html.xpath('//a[@class="last"]/@href')[0]
        try:
            page = int(re.findall("index_(.*?).html", last_page)[0])
        except:
            page=1
        trs = html.xpath('//ul[@class="ftdt-list"]/li')
        for tr in trs:
            info={}
            info["block"] = "工程建设服务"
            info["collet_area"] = lx1
            info["collet_area2"] =lx2
            info["plate"] = "政策资讯"
            info["pulic_type"] = "最新资讯"
            info["city"] = ""
            info["field"] = ""
            info["create_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            info["title"] = tr.xpath('./a[1]/@title')[0]
            info["file_link"] = tr.xpath('./a[1]/@href')[0]
            info["public_time"] = tr.xpath('./span/text()')[0].split("\r")[0]
            yield feapder.Request(info["file_link"], callback=self.down_file,
                                  meta=info)
        if page>1:
            count=count+1
            if count<page+1:
                next_url=url.split("index")[0]+f'index_{str(count)}.html'
                yield feapder.Request(next_url, callback=self.parse,
                                      lx1=lx1, lx2=lx2,count=1)

    def parse2(self, request, response):
        '''
                            解析页面
                            :return:
                   '''
        lx1 = request.lx1
        lx2 = request.lx2
        info = {}
        info["block"] = "工程建设服务"
        info["collet_area"] = lx1
        info["collet_area2"] = lx2
        info["plate"] = "政策资讯"
        info["pulic_type"] = "最新资讯"
        info["city"] = ""
        info["field"] = ""
        info["create_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        info["source"] = "深圳市住房和建设局"

        if lx2=='检测资质':
            info["title"] ="检测资质"
            info["file_link"] ="http://zjj.sz.gov.cn/ztfw/gcjs/jczz/content/post_10438816.html"
            info["public_time"] ="2023-02-21 16:35"
        if lx2=='图书资料':
            info["title"] ="图书资料"
            info["file_link"] ="http://zjj.sz.gov.cn/ztfw/gcjs/tszl/"
            info["public_time"] =""
        if lx2=='业务流程':
            info["title"] ="业务流程"
            info["file_link"] ="http://zjj.sz.gov.cn/ztfw/gcjs/ywlc/content/post_10438809.html"
            info["public_time"] ="2023-02-21 15:10"
        if lx2=='见证卡办理':
            info["title"] ="见证卡办理"
            info["file_link"] ="http://zjj.sz.gov.cn/ztfw/gcjs/jzkbl/content/post_10438805.html"
            info["public_time"] ="2023-02-21 15:09"
        yield feapder.Request(info["file_link"], callback=self.down_file,
                              meta=info)



    def down_file(self, request, response):
        info = request.meta
        html = response.content.decode("utf-8")
        info["html"] = html
        res = etree.HTML(html)


        item = Item()
        item.table_name = "zjjsz"  # 表名
        item.block = info["block"]
        item.collet_area = info["collet_area"]
        item.collet_area2 = info["collet_area2"]
        item.plate = info["plate"]
        item.pulic_type = info["pulic_type"]
        item.city = info["city"]
        item.field = info["field"]
        item.create_time = info["create_time"]
        item.title = info["title"]
        item.file_link = info["file_link"]
        item.public_time = info["public_time"]
        item.public_text = info["public_text"]
        item.html= info["html"]
        print(item)





if __name__ == "__main__":
    AirSpiderCgjs(thread_count=1).start()
