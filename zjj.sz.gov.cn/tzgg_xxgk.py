import datetime
import feapder
from feapder import Item
from lxml import etree
from urllib.parse import quote,unquote

class AirSpiderXxgk(feapder.AirSpider):
    '''
                       函数入口
                        :return:
               '''
    def start_requests(self):

        for page in range(1,6):
            if page==1:
                url="http://zjj.sz.gov.cn/xxgk/tzgg/index.html"
            else:
                url=f"http://zjj.sz.gov.cn/xxgk/tzgg/index_{page}.html"
            yield feapder.Request(url, callback=self.parse, verify=False, method="GET")




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
        html = response.text
        html = etree.HTML(html)
        trs = html.xpath('//ul[@class="ftdt-list"]/li')
        for tr in trs:
            info = {}
            info["block"] = "信息公开"
            info["collet_area"] = "通知公告"
            info["collet_area2"] = ' '
            info["plate"] = " "
            info["pulic_type"] = " "
            info["city"] = ""
            info["field"] = ""
            info["create_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            info["title"] = tr.xpath('./a[1]/@title')[0]
            info["file_link"] = tr.xpath('./a[1]/@href')[0]
            info["public_time"] = tr.xpath('./span/text()')[0]
            print(info)

            yield feapder.Request(info["file_link"], callback=self.down_file, meta=info)






    def down_file(self, request, response):
        info = request.meta
        html = response.content.decode("utf-8")
        info["html"] = html


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
        item.html= info["html"]
        # print(item)





if __name__ == "__main__":
    AirSpiderXxgk(thread_count=1).start()
