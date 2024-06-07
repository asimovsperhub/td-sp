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

def get_token():
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Length": "0",
        "Origin": "http://zfcg.szggzy.com:8081",
        "Pragma": "no-cache",
        "Referer": "http://zfcg.szggzy.com:8081/pageVerify.html",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    cookies = {
        "sid": "14DB881CEB8B4988BAA8AE39CB776C75"
    }
    url = "http://zfcg.szggzy.com:8081/EpointWebBuilder/rest/getOauthInfoAction/getNoUserAccessToken"
    response = requests.post(url, cookies=cookies, verify=False).json()
    info={}
    info["access_token"]=response["custom"]["access_token"]
    info["refresh_token"]=response["custom"]["refresh_token"]
    return info
class AirSpiderCggg(feapder.AirSpider):
    '''
                       函数入口
                        :return:
               '''
    def start_requests(self):

            for page in range(1,1317):
                if page==1:
                    url="http://zfcg.szggzy.com:8081/gsgg/002001/002001002/list.html"
                    yield feapder.Request(url, callback=self.parse1, verify=False, method="GET")
                elif 101>page>1:
                    url=f"http://zfcg.szggzy.com:8081/gsgg/002001/002001002/{page}.html"
                    yield feapder.Request(url, callback=self.parse1, verify=False, method="GET")
                else:
                    url=f"http://zfcg.szggzy.com:8081/gsgg/002001/002001002/list.html?categoryNum=002001002&pageIndex={page}"

                    yield feapder.Request(url,callback=self.parse2, verify=False, method="GET")
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

        return request

    def parse1(self, request, response):
        '''
                            解析页面
                            :return:
                   '''
        html = response.text
        print(len(html))
        html = etree.HTML(html)

        trs = html.xpath('//ul[@class="news-items"]/li')
        for tr in trs:
            info = {}
            info = {}
            info["block"] = "公示公告"
            info["collet_area"] = "采购公告"
            info["plate"] = "招标信息"
            info["pulic_type"] = "招标公告"
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

    def parse2(self, request, response):
        '''
                            解析页面(通过接口爬取) (翻页需要验证码)
                            :return:
                   '''

        page =re.findall("pageIndex=(.*)",request.url)[0]
        result = get_token()
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Authorization": f'Bearer {result["access_token"]}',
            "Cache-Control": "no-cache",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "http://zfcg.szggzy.com:8081",
            "Pragma": "no-cache",
            "Proxy-Connection": "keep-alive",
            "Referer": "http://zfcg.szggzy.com:8081/gsgg/002001/002001002/list.html?categoryNum=002001002&pageIndex=102",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }
        cookies = {

            "oauthClientId": "admin",
            "oauthPath": "http://127.0.0.1:8080/EpointWebBuilder",
            "oauthLoginUrl": "http://127.0.0.1:1112/membercenter/login.html?redirect_uri=",
            "oauthLogoutUrl": "",
            "fontZoomState": "0",
            "userGuid": "1047923792",
            "noOauthRefreshToken": result["refresh_token"],
            "noOauthAccessToken": result["access_token"]
        }
        url = "http://zfcg.szggzy.com:8081/EpointWebBuilder/rest/frontAppNotNeedLoginAction/getVerificationCode"
        data = {
            "params": "{\"width\":\"100\",\"height\":\"40\",\"codeNum\":\"4\",\"interferenceLine\":\"1\",\"codeGuid\":\"\"}"
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
        filename = file_path + '\\' + str(random.randint(100, 200)) + '.jpg'
        with open(filename, 'wb') as f:
            f.write(img)
        ocr = ddddocr.DdddOcr()
        with open(filename, 'rb') as f:
            img_bytes = f.read()
        res = ocr.classification(img_bytes)
        cookies["sid"] = sid
        url = "http://zfcg.szggzy.com:8081/EpointWebBuilder/rest/frontAppNotNeedLoginAction/getPageInfoList"
        data = {
            "params": "{\"siteGuid\":\"\",\"categoryNum\":\"002001002\",\"pageIndex\":\"%s\",\"pageSize\":1,\"controlname\":\"subpagelist\",\"ImgGuid\":\"%s\",\"YZM\":\"%s\"}" % (
            page, verificationCodeGuid, res)
        }
        response = requests.post(url, headers=headers, cookies=cookies, data=data, verify=False).json()
        json_data=response["custom"]["infodata"]
        for data in json_data:
            info = {}
            info = {}
            info["block"] = "公示公告"
            info["collet_area"] = "采购公告"
            info["plate"] = "招标信息"
            info["pulic_type"] = "招标公告"
            info["city"] = "深圳"
            info["field"] = "其他"
            info["create_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            info["title"] = data["customtitle"].replace("<font color='#CC00FF'>[公开招标]</font>",'')
            info["file_link"] ="http://zfcg.szggzy.com:8081/"+data["infourl"]
            info["public_time"] =data["infodate"]
            info["file"] = " "
            info["money"] = " "
            info["company"] = " "
            print(info)
            yield feapder.Request(info["file_link"], callback=self.down_file1,
                                  meta=info)
            break

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
        info["public_text"] = text


        try:
            contact = re.findall("项目联系人：(.*?)</span>",response)[0]
        except:
            contact=" "
        info["contact"]=contact
        contact_number = " "
        try:
            regular = re.compile(r'\d{3,4}-\d{6,9}|\d{3}-\d{9}')
            contact_number = re.findall(regular, text)[0]
        except:
            number_list = re.findall('(\d+)', text)
            for number in number_list:
                if int(number) > 1000000:
                    contact_number = number
        info["contact_number"]=contact_number
        # 匹配金额
        try:
            money = re.findall("预算金额（单位：元）：(.*?)</span>",response)[0]
        except:
            money=' '
        info["money"]=money
        print(info)

        #下载附件
        link = html.xpath('//p[@id="NEWS"]/a/@onclick')[-1]
        file_link = re.findall("EpointWebBuilder(.*?)','", link)[0]
        attachGuid = re.findall("attachGuid=(.*?)&appUrl", file_link)[0]

        url = "http://zfcg.szggzy.com:8081/EpointWebBuilder/rest/frontAppNotNeedLoginAction/getVerificationCode"
        data = {
            "params": "{\"width\":\"100\",\"height\":\"40\",\"codeNum\":\"4\",\"interferenceLine\":\"1\",\"codeGuid\":\"\"}"
        }
        result = get_token()
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
        # 写图片
        with open(filename, 'wb') as f:
            f.write(img)
        ocr = ddddocr.DdddOcr()
        # 识别图片
        with open(filename, 'rb') as f:
            img_bytes = f.read()
        res = ocr.classification(img_bytes)

        # 保存文档
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
    AirSpiderCggg(thread_count=1).start()
