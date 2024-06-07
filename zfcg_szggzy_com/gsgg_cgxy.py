import datetime
import feapder
from feapder import Item
from lxml import etree


"""
政策资讯
"""
class AirSpiderZzgg(feapder.AirSpider):
    '''
                       函数入口
                        :return:
               '''
    def start_requests(self):

        for page in range(1,3):
            if page == 1:
                url = "http://zfcg.szggzy.com:8081/cgxy/list.html"
            else:
                url = f"http://zfcg.szggzy.com:8081/cgxy/{page}.html"
            yield feapder.Request(url, callback=self.parse1, verify=False, method="GET")


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
            "Pragma": "no-cache",
            "Referer": "http://zfcg.szggzy.com:8081/",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
        }

        return request

    def parse1(self, request, response):
        '''
                            解析页面
                            :return:
                   '''
        html = response.text
        html = etree.HTML(html)

        trs = html.xpath('//ul[@class="news-items"]/li')
        for tr in trs:
            info = {}
            info["block"] = "政策法规"
            info["collet_area"] = "法律法规"
            info["plate"] = "政策资讯"
            info["pulic_type"] = "政策资讯"
            info["city"] = "深圳"
            info["field"] = "其他"
            info["create_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            info["title"] = tr.xpath('./a/@title')[0]
            info["file_link"] = tr.xpath('./a/@href')[0]
            info["public_time"] = tr.xpath('./span/text()')[0].strip()
            info["file"] = " "
            info["money"] = " "
            info["company"] = " "

            yield feapder.Request(info["file_link"], callback=self.down_file1,
                                  meta=info)



    def down_file1(self, request, response):
        '''
                   解析公告
                    :return:
           '''
        info = request.meta
        html = response.text
        html = etree.HTML(html)
        trs = html.xpath('//tbody//text()')
        text = "".join(trs)
        info["public_text"] =text
        info["contact"] = " "
        info["contact_number"]=" "
        # print(info)

        #
        # item = Item()
        # item.table_name = "zfcg_szggzy"  # 表名
        # item.block = info["block"]
        # item.collet_area = info["collet_area"]
        # item.plate = info["plate"]
        # item.pulic_type = info["pulic_type"]
        # item.city = info["city"]
        # item.field = info["field"]
        # item.create_time = info["create_time"]
        #
        item = Item()
        item.table_name = "consultation"  # 表名
        item.type = info["pulic_type"]
        item.created_at = info["create_time"]
        item.title = info["title"]
        item.url = info["file_link"]
        item.publish = info["public_time"].replace("\r","").replace("\n","") if info["public_time"] else ""
        item.content = info["public_text"]
        print(item)


if __name__ == "__main__":
    AirSpiderZzgg(thread_count=1).start()
