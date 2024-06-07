import datetime
import feapder
from feapder import Item
from lxml import etree
import tools

"""
政策咨询
"""

class AirSpiderZnzx(feapder.AirSpider):
    '''
                       函数入口
                        :return:
               '''
    def start_requests(self):

        # for lx in range(1, 13):
        #     if lx==1:
        #         page_count=38
        #     if lx==2:
        #         page_count=370
        #     if lx==3:
        #         page_count=7
        #     if lx==4:
        #         page_count=15
        #     if lx==5:
        #         page_count=100
        #     if lx==6:
        #         page_count=3
        #     if lx==7:
        #         break
        #     if lx==8:
        #         page_count=7
        #     if lx==9:
        #         page_count=4
        #     if lx==10:
        #         page_count=3
        #     if lx==11:
        #         page_count=10
        #     if lx==12:
        #         page_count=745
        #     url = "http://search.ccgp.gov.cn/znzxsearch"
        #     for page in range(1,2):
        #         params = {
        #             "searchtype": "1",
        #             "page_index": str(page),
        #             "searchchannel": str(lx),
        #             "kw": "",
        #             "start_time": "",
        #             "end_time": "",
        #             "timeType": "0"
        #         }
        #         yield feapder.Request(url, params=params, verify=False, method="GET",lx=lx)
        url = "http://search.ccgp.gov.cn/znzxsearch"
        pages=int(25000/2)
        for page in range(1, pages):
            params = {
                "searchtype": "1",
                "page_index": str(page),
                "searchchannel": "",
                "kw": "",
                "start_time": "",
                "end_time": "",
                "timeType": "0"
            }
            yield feapder.Request(url, params=params, verify=False, method="GET")

    def download_midware(self, request):
        '''
                          下载中间件
                            :return:
                   '''
        request.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "$Cookie": "HMF_CI=c073a0a042ff7ecb18b1b632111d56074aedbbb2a8b74eb73c58fefef1dbe861352a61a7662855ff2a70ddb1c6e4935e4fbc26287a635b0968424728d9e64de63e; Hm_lvt_9459d8c503dd3c37b526898ff5aacadd=1677002480,1677002600; HMY_JC=f4c29e36f7345cb0b7633bf06d247238504ffb80a93547445c885a65d96155670b,; HBB_HC=5d434950322ef2b233bd2430de59a9f4b72351343bd805646512902d9f811c6d0d48527ab9edb88617c2bc0b24e3ffbbc7; JSESSIONID=6nR1Le_X1dsJ3A9v1CDJwAKTV4UAJcEH2vF_4MiveGR0X5nQJRCZ\\u00211144578798; Hm_lpvt_9459d8c503dd3c37b526898ff5aacadd=1677003190",
            "Pragma": "no-cache",
            "Referer": "http://search.ccgp.gov.cn/znzxsearch?searchtype=1&page_index=2&searchchannel=1&kw=&start_time=&end_time=&timeType=0",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
        }
        pro = tools.get_proxy()
        request.proxies = pro
        return request

    def parse(self, request, response):
        '''
                            解析页面
                            :return:
                   '''
        # lx=request.lx
        zx_list=["","政采法规","购买服务","监督检查","国际专栏","PPP频道","案例解读","","财政部政府采购信息公告 ","节能环保清单","政府采购评审专家劳务报酬标准","采购目录","其他"]
        html = response.text
        html = etree.HTML(html)
        trs = html.xpath('//ul[@class="vT-srch-result-list-nr"]/li')
        for tr in trs:
            info = {}
            info["created_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # 标题
            info["title"] = tr.xpath('./a/text()')[0]
            # 类型
            info["type"] = tr.xpath('./span/text()')[0]
            # 外部链接
            info["url"] = tr.xpath('./a/@href')[0]
            # 发布时间
            info["publish"] = tr.xpath('./em/text()')[0].strip()
            # print(info)
            yield feapder.Request(info["url"], callback=self.down_file,
                                  meta=info)

    def down_file(self, request, response):
        info = request.meta
        html = response.text
        info["html"] = html
        res = etree.HTML(html)

        trs = res.xpath('//div[@class="TRS_Editor"]//text()')
        attachment= [i for i in res.xpath("//a/@href") if str(i).endswith(".pdf")]
        info["content"] = "".join(trs)
        item = Item()
        item.table_name = "consultation"  # 表名
        item.title = info["title"].replace("\r","").replace("\n","").replace("\t","")
        item.type = "法律法规" if "法规" in info["type"] else "最新资讯"
        item.url = info["url"]
        item.created_at = info["created_at"]
        item.publish = info["publish"]
        item.content = info["content"]
        item.attachment = attachment[0] if attachment else ""
        # print(item)
        yield item




if __name__ == "__main__":
    AirSpiderZnzx(thread_count=1).start()
