import random
import requests
from lxml import etree
for i in range(1,2):
    url = f"http://zfcg.szggzy.com:8081/gsgg/002001/002001002/list.html?categoryNum=002001002&pageIndex={i}"
    response = requests.get(url, verify=False).text
    print(response)
    html = etree.HTML(response)
    # trs = html.xpath('//ul[@class="news-items"]/li')
    # for tr in trs:
    #     title = tr.xpath('./a/@title')[0]
    #     href = tr.xpath('./a/@href')[0]
    #     hr = tr.xpath('./span/text()')[0].strip()
    #     print(title, href,hr)




