import datetime
import time

import json
import feapder
from feapder import Item


class AirSpiderZhaobiao(feapder.AirSpider):
    '''
                       函数入口
                        :return:
               '''
    def start_requests(self):
            url="https://www.szygcgpt.com/app/portal/cmsXinXi/pageList"
            for lx in range(1, 7):
                _t = int(time.time())
                params = {
                    "_t": _t,
                    "xinXiGuanLiType": "5",
                    "msgType": str(lx)
                }
                yield feapder.Request(url, params=params, method="GET", lx=lx)



    def download_midware(self, request):
        '''
                          下载中间件
                            :return:
                   '''
        request.headers = {
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Content-Type": "application/json;charset=utf-8",
                "Pragma": "no-cache",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
                "sec-ch-ua": "\"Not_A Brand\";v=\"99\", \"Google Chrome\";v=\"109\", \"Chromium\";v=\"109\"",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "\"Windows\""
}


        return request

    def parse(self, request, response):
        '''
                            解析页面
                            :return:
                   '''
        lx=request.lx
        zhaobiao_lx=["国务院执行法规","地方性法规","部门规章","地方性政府规章","规范性文件","制度文件"]
        json_data = json.loads(response.text)["data"]["rows"]
        for data in json_data:
            info = {}
            info["block"] = "政策法规"
            info["collet_area"] = "政策法规"
            info["collet_area2"] = zhaobiao_lx[lx - 1]
            info["plate"] = "政策资讯"
            info["pulic_type"] = "法律法规"
            info["city"] = ""
            info["field"] = ""
            info["create_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            info["title"] = data["msgTitle"]
            ggGuid = data["guid"]
            info["file_link"] = f"https://www.szygcgpt.com/ygcg/layDetail?guid={ggGuid}"
            timeStamp = data["publishTime"]
            timeArray = time.localtime(int(timeStamp) / 1000)
            info["public_time"] = time.strftime("%Y-%m-%d", timeArray)
            info["public_text"]=data["msgContent"]
            info["province"]="广东"

            item = Item()
            item.table_name = "szygcgpt"  # 表名
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
            item.province = info["province"]
    #
            yield item



if __name__ == "__main__":
    AirSpiderZhaobiao(thread_count=1).start()
