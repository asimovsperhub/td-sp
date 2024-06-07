import datetime
import random
import re
import base64
import json
import ddddocr
import requests
import feapder
from feapder import Item
from lxml import etree

#获取token
def get_token():
    cookies = {
        "sid": "14DB881CEB8B4988BAA8AE39CB776C75"
    }
    url = "http://zfcg.szggzy.com:8081/EpointWebBuilder/rest/getOauthInfoAction/getNoUserAccessToken"
    response = requests.post(url, cookies=cookies, verify=False).json()
    info={}
    info["access_token"]=response["custom"]["access_token"]
    info["refresh_token"]=response["custom"]["refresh_token"]
    return info

class AirSpiderYjzj(feapder.AirSpider):
    '''
            启动函数入口
            :return:
   '''
    def start_requests(self):
        url_list=["http://zfcg.szggzy.com:8081/gsgg/002001/002001006/list.html"]
        for url in url_list:
            if url=="http://zfcg.szggzy.com:8081/gsgg/002001/002001006/list.html":
                for page in range(1,59):
                    if page==1:
                        url="http://zfcg.szggzy.com:8081/gsgg/002001/002001006/list.html"
                    else:
                        url = f"http://zfcg.szggzy.com:8081/gsgg/002001/002001006/{page}.html"
                    yield feapder.Request(url,callback=self.parse1, verify=False, method="GET")
                    break


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
        request.cookies = {
            "userGuid": "1047923792",
            "oauthClientId": "admin",
            "oauthPath": "http://127.0.0.1:8080/EpointWebBuilder",
            "oauthLoginUrl": "http://127.0.0.1:1112/membercenter/login.html?redirect_uri=",
            "oauthLogoutUrl": "",
            "fontZoomState": "0",
            "noOauthRefreshToken": "27bb125a030de3d0da81454b9f710e7a",
            "noOauthAccessToken": "066979910bc74737e92be6621b92c0e6"
        }
        return request

    def parse1(self, request, response):
        '''
                    解析页面
                    :return:
           '''
        html = response.text
        html = etree.HTML(html)
        trs = html.xpath('//ul[@class="news-items"]//li')
        for tr in trs:
            info = {}
            info["block"] = "公示公告"
            info["collet_area"]="意见征集公告"
            info["plate"] = "招标信息"
            info["pulic_type"] = "意向公开"
            info["city"] = "深圳"
            info["field"] = "其他"
            info["create_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            info["title"] = tr.xpath(".//a/@title")[0]
            info["file_link"] = tr.xpath(".//a/@href")[0]
            info["public_time"] = tr.xpath("./span[@class='news-time']/text()")[0].strip()
            info["file"] =" "
            info["money"] =" "
            info["company"] =" "

            yield feapder.Request(info["file_link"], callback=self.down_file1,
                                  meta=info)



    def down_file1(self, request, response):
        '''
                    下载附件
                    :return:
           '''
        info = request.meta
        html = response.text
        html = etree.HTML(html)
        trs = html.xpath('//tbody//text()')
        text = "".join(trs)
        info["public_text"] = text
        try:
            contact = str(re.findall("联系人(.*)，", text)[0]).replace("：", '').replace("，", '')
        except:
            contact = " "

        try:
            contact_number = str(re.findall("电话(.*)", text)[0]).replace("：", '').replace("，", '')
        except:
            contact_number = " "
        info["contact"] = contact
        info["contact_number"]=contact_number
        info["money"]=" "

        link = html.xpath('//p[@id="NEWS"]/a/@onclick')[-1]
        file_link = re.findall("EpointWebBuilder(.*?)','", link)[0]
        attachGuid = re.findall("attachGuid=(.*?)&appUrl", file_link)[0]

        url = "http://zfcg.szggzy.com:8081/EpointWebBuilder/rest/frontAppNotNeedLoginAction/getVerificationCode"
        data = {
            "params": "{\"width\":\"100\",\"height\":\"40\",\"codeNum\":\"4\",\"interferenceLine\":\"1\",\"codeGuid\":\"\"}"
        }
        result=get_token()
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Authorization": f'Bearer {result["access_token"]}',
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "http://zfcg.szggzy.com:8081",
            "Pragma": "no-cache",
            "Referer": "http://zfcg.szggzy.com:8081/pageVerify.html",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }
        cookies = {

            "noOauthRefreshToken": result["refresh_token"],
            "noOauthAccessToken": result["access_token"],
            "oauthClientId": "admin",
            "oauthPath": "http://127.0.0.1:8080/EpointWebBuilder",
            "oauthLoginUrl": "http://127.0.0.1:1112/membercenter/login.html?redirect_uri=",
            "oauthLogoutUrl": ""
        }
        response = requests.post(url, headers=headers, cookies=cookies, data=data, verify=False)
        sid = response.headers['Set-Cookie']
        sid = re.findall(";, sid=(.*?); Path=/EpointWebBuilder/;", sid)[0]

        response = json.loads(response.text)
        img_imf = response["custom"]["imgCode"]
        verificationCodeGuid = response["custom"]["verificationCodeGuid"]

        img_imf = img_imf.replace('data:image/jpg;base64,', '')
        img = base64.b64decode(img_imf)
        file_path = "E:\download\img"
        filename = file_path + '\\' + str(random.randint(1, 100)) + '.jpg'
        #写图片
        with open(filename, 'wb') as f:
            f.write(img)
        ocr = ddddocr.DdddOcr()
        #识别图片
        with open(filename, 'rb') as f:
            img_bytes = f.read()
        res = ocr.classification(img_bytes)

        #保存文档
        url = "http://zfcg.szggzy.com:8081/EpointWebBuilder/pages/webbuildermis/attach/ztbAttachDownloadAction.action"
        params = {
            "cmd": "getContent",
            "attachGuid": attachGuid,
            "appUrlFlag": "ztb001",
            "siteGuid": "7eb5f7f1-9041-43ad-8e13-8fcb82ea831a",
            "verificationCode": res,
            "verificationGuid": verificationCodeGuid
        }
        cookies = {
            "sid": sid,
            "noOauthRefreshToken": result["refresh_token"],
            "noOauthAccessToken": result["access_token"],
            "oauthClientId": "admin",
            "oauthPath": "http://127.0.0.1:8080/EpointWebBuilder",
            "oauthLoginUrl": "http://127.0.0.1:1112/membercenter/login.html?redirect_uri=",
            "oauthLogoutUrl": ""
        }
        data = '------WebKitFormBoundaryBuP8Ck223Eaoh6Oz--\\r\\n'.encode('unicode_escape')
        response = requests.post(url, headers=headers, cookies=cookies, params=params, data=data, verify=False).content
        print(len(response))
        file_path = "E:\download\采购文件公示"
        filename = file_path + '\\' + info["title"] + '.docx'
        with open(filename, 'wb') as f:
            f.write(response)
        print("保存成功")








    #     info = request.meta
    #     html = response.text
    #     info["html"] = html
    #     item = Item()
    #     item.table_name = "szzfcg"  # 表名
    #     item.block = info["block"]
    #     item.plate = info["plate"]
    #     item.pulic_type = info["pulic_type"]
    #     item.city = info["city"]
    #     item.field = info["field"]
    #     item.create_time = info["create_time"]
    #     item.filename = info["filename"]
    #     item.public_time = info["public_time"]
    #     item.file_link = info["file_link"]
    #     item.title = info["title"]
    #     item.province = info["province"]
    #     item.pinmu = info["pinmu"]
    #     item.area = info["area"]
    #     item.html = info["html"]
    #
    #     yield item




if __name__ == "__main__":
    AirSpiderYjzj(thread_count=1).start()
