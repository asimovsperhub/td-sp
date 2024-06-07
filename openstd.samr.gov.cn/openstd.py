import json
import os
import time

import feapder
from feapder import Item


class Open(feapder.AirSpider):
    def start_requests(self):
        for type in ['sfjs', 'dfxfg', 'jcfg', 'xzfg', 'flfg']:
            params = {
                'type': type,
                'searchType': 'title;vague',
                'sortTr': 'f_bbrq_s;desc',
                'gbrqStart': '',
                'gbrqEnd': '',
                'sxrqStart': '',
                'sxrqEnd': '',
                'sort': 'true',
                'page': '1',
                'size': '10',
                '_': str(int(time.time() * 1000)),
            }
            yield feapder.Request(url='https://flk.npc.gov.cn/api/', params=params, method="GET",
                                  download_midware=self.download_midware, request_sync=True,
                                  callback=self.parse, page=1, lawtype=type)

    def download_midware(self, request):
        """
        :param request:
        :return:
        """
        request.headers = {
            'authority': 'flk.npc.gov.cn',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'zh-CN,zh;q=0.9',
            'referer': 'https://flk.npc.gov.cn/dfxfg.html',
            'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }
        # request.proxies = {"https": "https://ip:port", "http": "http://ip:port"}
        return request

    def parse(self, request, response):
        res = json.loads(response.text)
        if res.get("result"):
            res = res.get("result")
            if res.get("data"):
                data = res.get("data")
                for i in data:
                    d = {}
                    d['expiry'] = i.get("expiry")
                    d['id'] = i.get("id")
                    d['office'] = i.get("office")
                    d['publish'] = i.get("publish")
                    d['title'] = i.get("title")
                    d['type'] = i.get("type")
                    d['url'] = i.get("url")
                    d['lawtype'] = request.lawtype
                    json_data = {
                        'id': i.get("id"),
                    }
                    yield feapder.Request(url='https://flk.npc.gov.cn/api/detail', data=json_data, method="POST",
                                          download_midware=self.download_midware, request_sync=True,
                                          callback=self.details_pm, item=d)

            totalSizes = res.get("totalSizes", 0)
            if request.page < totalSizes:
                page = request.page + 1
                params = {
                    'type': type,
                    'searchType': 'title;vague',
                    'sortTr': 'f_bbrq_s;desc',
                    'gbrqStart': '',
                    'gbrqEnd': '',
                    'sxrqStart': '',
                    'sxrqEnd': '',
                    'sort': 'true',
                    'page': str(page),
                    'size': '10',
                    '_': str(int(time.time() * 1000)),
                }
                yield feapder.Request(url='https://flk.npc.gov.cn/api/', params=params, method="GET",
                                      download_midware=self.download_midware, request_sync=True,
                                      callback=self.parse, page=page)

    def details_pm(self, request, response):
        res = json.loads(response.text)
        item = request.item
        if res.get("result"):
            res = res.get("result")
            if res.get("body"):
                res = res.get("body")
                if isinstance(res, list):
                    for i in res:
                        path = i.get("path")
                        download_url = "https://wb.flk.npc.gov.cn" + path
                        item[i.get("type").lower()] = path.split("/")[-1]
                        item['id'] = path.split("/")[-1].split(".")[0]
                        yield feapder.Request(url=download_url, method="GET",
                                              download_midware=self.download_midware, request_sync=True,
                                              callback=self.download_file, filename=path.split("/")[-1],
                                              filepath=item.get("lawtype"))
        it = Item()
        it.table_name = 'law'
        it.fileid = item.get("id")
        it.publish = item.get("publish")
        it.expiry = item.get("expiry")
        it.office = item.get("office")
        it.title = item.get("title")
        it.type = item.get("type")
        it.word = item.get("word")
        it.pdf = item.get("pdf")
        it.lawtype = item.get("lawtype")
        it.url = item.get("url")

        yield it

    def download_file(self, request, response):
        dir = f"/home/fvdownload/{request.filepath}/"
        if not os.path.exists(dir):
            os.makedirs(dir)
        with open(f"{dir}/{request.filename}", 'wb+') as f:
            f.write(response.content)


if __name__ == "__main__":
    Open(thread_count=1).start()
