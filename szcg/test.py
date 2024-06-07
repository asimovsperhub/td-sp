import requests

import re
# headers = {
#     "Connection": "keep-alive",
#     "Pragma": "no-cache",
#     "Cache-Control": "no-cache",
#     "Upgrade-Insecure-Requests": "1",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
#     "Sec-Fetch-Site": "none",
#     "Sec-Fetch-Mode": "navigate",
#     "Sec-Fetch-User": "?1",
#     "Sec-Fetch-Dest": "document",
#     "Accept-Language": "zh-CN,zh;q=0.9",
#     "$Cookie": "JSESSIONID=JTpLQxuIeefx632m-ERMxQCgWHjG7L30rch_jzD-3kTecG-i2-2_\\u0021-1177488671\\u00212092975900"
# }
# url = "https://www.szzfcg.cn/viewer.do?id=1012012386"
#
# response = requests.get(url, headers=headers)
#
# print(response.text)
# print(response)

a="https://www.szzfcg.cn/portal/documentView.do?method=view&id=1011817013"
id=re.findall("id=(.*)",a)[0]
url=f"https://www.szzfcg.cn/portal/documentView.do?method=view&id={id}"
print(id)
