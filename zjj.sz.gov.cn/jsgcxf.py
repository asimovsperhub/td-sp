import datetime
import math
import time
import json
import feapder
from feapder import Item

class AirSpiderCgjs(feapder.AirSpider):
    '''
                       函数入口
                        :return:
               '''
    def start_requests(self):
        time_ = int(time.time() * 1000)
        task_list={'建设工程消防': [{'消防设计审查结果': 'http://zjj.sz.gov.cn/ztfw/gcjs/xffw/xfsjscjg/index.html'}, {'消防验收审查结果': 'http://zjj.sz.gov.cn/ztfw/gcjs/xffw/xfysjg/index.html'}, {'消防验收备案结果': 'http://zjj.sz.gov.cn/ztfw/gcjs/xffw/xfysbajg/index.html'}]}
        for key, values in task_list.items():
            for value in values:
                for k,v in value.items():
                    if k=='消防设计审查结果':
                        doctype = "1"
                        url=f"http://zjj.sz.gov.cn/jzxypj/enterpriseInfoService/getXfDesignInfoList.json?rows=100&page=1&engname=&constunit=&doctype={doctype}&_={time_}"
                    elif k=='消防验收审查结果':
                        doctype = "2"
                        url = f"http://zjj.sz.gov.cn/jzxypj/enterpriseInfoService/getXfDesignInfoList.json?rows=100&page=1&engname=&constunit=&doctype={doctype}&_={time_}"
                    elif k=='消防验收备案结果':
                        doctype="3"
                        url = f"http://zjj.sz.gov.cn/jzxypj/enterpriseInfoService/getXfDesignInfoList.json?rows=100&page=1&engname=&constunit=&doctype={doctype}&_={time_}"
                    yield feapder.Request(url,verify=False, method="GET", doctype=doctype,lx1=key, lx2=k,count=1)
                break



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
        lx1 = request.lx1
        lx2 = request.lx2
        doctype = request.doctype
        count = request.count
        json_data=json.loads(response.text)["rows"]
        total=json.loads(response.text)["total"]
        page=math.ceil(int(total) / 100)+1
        print(page)
        for data in json_data:
            info = {}
            info["block"] = "工程建设服务"
            info["collet_area"] = lx1
            info["collet_area2"] = lx2
            info["plate"] = "政策资讯"
            info["pulic_type"] = "最新资讯"
            info["city"] = ""
            info["field"] = ""
            info["create_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            info["title"] = data["engineering_name"]
            if lx2=='消防设计审查结果':
                info["file_link"] =  'http://zjj.sz.gov.cn/ztfw/gcjs/xffw/xfsjscjg/index.html'

            if lx2=='消防验收审查结果':
                info["file_link"] = 'http://zjj.sz.gov.cn/ztfw/gcjs/xffw/xfysjg/index.html'
            if lx2=='消防验收备案结果':
                info["file_link"] = 'http://zjj.sz.gov.cn/ztfw/gcjs/xffw/xfysbajg/index.html'

            info["public_time"] = data["bjsj"]
            data = {
                "id":str(data["id"])
            }
            url = "http://zjj.sz.gov.cn/jzxypj/enterpriseInfoService/getXfDetailInfo.json"

            yield feapder.Request(url, data=data, verify=False, callback=self.down_file, method="POST",meta=info)
        # 翻页
        count=count+1
        if count<page:
            url = f"http://zjj.sz.gov.cn/jzxypj/enterpriseInfoService/getXfDesignInfoList.json?rows=100&page={str(count)}&engname=&constunit=&doctype={doctype}&_={time}"
            yield feapder.Request(url, verify=False,  callback=self.parse,method="GET", doctype=doctype, lx1=lx1, lx2=lx2, count=count)


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
        print(item)





if __name__ == "__main__":
    AirSpiderCgjs(thread_count=1).start()
