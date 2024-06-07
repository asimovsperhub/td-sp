import base64
import json
import os
import sys

import requests

sys.path.insert(
    0,
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

"""
+-------------------------+---------------------+------+-----+---------+----------------+
| Field                   | Type                | Null | Key | Default | Extra          |
+-------------------------+---------------------+------+-----+---------+----------------+
| id                      | bigint(20) unsigned | NO   | PRI | NULL    | auto_increment |
| bulletin_type           | varchar(100)        | NO   | MUL |         |                |
| city                    | varchar(100)        | NO   | MUL |         |                |
| industry_classification | varchar(100)        | YES  | MUL |         |                |
| release_time            | varchar(100)        | NO   | MUL |         |                |
| bidopening_time         | varchar(100)        | NO   | MUL |         |                |
| title                   | varchar(255)        | NO   | MUL |         |                |
| abstract                | varchar(255)        | NO   |     |         |                |
| enterprise              | varchar(255)        | NO   |     |         |                |
| announcement_content    | longtext            | NO   | MUL | ''      |                |
| link                    | varchar(255)        | NO   |     |         |                |
| attachment              | varchar(255)        | NO   |     |         |                |
| amount                  | varchar(100)        | NO   |     |         |                |
| contact_person          | char(100)           | NO   |     |         |                |
| contact_information     | char(100)           | NO   |     |         |                |
| created_at              | datetime            | YES  | MUL | NULL    |                |
+-------------------------+---------------------+------+-----+---------+----------------+
"""
user = "asimov"
password = "asimov@77"
bas64encoded_creds = base64.b64encode(bytes(user + ":" + password, "utf-8")).decode("utf-8")
host = "http://81.71.49.57:4080"
index = "/api/index"
index_name = "biding"
doc = "/api/" + index_name + "/_doc/"

list = ["id", "bulletin_type", "notice_nature", "city", "industry_classification", "release_time", "tender_deadline",
        "bidopening_time", "title", "announcement_content", "attachment", "amount", "contact_person",
        "contact_information", "contact_content", "link"]


def create_index(index_name) -> str:
    """
    :param bas64encoded_creds:
    :return:
    """
    data = {
        "name": index_name,
        "storage_type": "disk",
        "settings": {},
        "mappings": {
            "properties": {
                "@timestamp": {
                    "type": "date",
                    "index": True,
                    "store": False,
                    "sortable": True,
                    "aggregatable": True,
                    "highlightable": False,
                    "term_positions": False
                },
                "id": {
                    "type": "numeric",
                    "index": True,
                    "store": True,
                    "sortable": True,
                    "aggregatable": True,
                    "highlightable": False,
                    "term_positions": False
                },
                "bulletin_type": {
                    "type": "text",
                    "index": True,
                    "store": True,
                    "sortable": False,
                    "aggregatable": True,
                    "highlightable": True,
                    "term_positions": True
                },
                "city": {
                    "type": "text",
                    "index": True,
                    "store": True,
                    "sortable": False,
                    "aggregatable": False,
                    "highlightable": True,
                    "term_positions": True
                },
                "industry_classification": {
                    "type": "text",
                    "index": True,
                    "store": True,
                    "sortable": False,
                    "aggregatable": False,
                    "highlightable": True,
                    "term_positions": True
                },
                "release_time": {
                    "type": "text",
                    "index": True,
                    "store": True,
                    "sortable": False,
                    "aggregatable": False,
                    "highlightable": True,
                    "term_positions": True
                },
                "bidopening_time": {
                    "type": "text",
                    "index": True,
                    "store": True,
                    "sortable": False,
                    "aggregatable": False,
                    "highlightable": True,
                    "term_positions": True
                },
                "title": {
                    "type": "text",
                    "index": True,
                    "store": True,
                    "sortable": False,
                    "aggregatable": False,
                    "highlightable": True,
                    "term_positions": True
                },
                "abstract": {
                    "type": "text",
                    "index": True,
                    "store": True,
                    "sortable": False,
                    "aggregatable": False,
                    "highlightable": True,
                    "term_positions": True
                },
                "enterprise": {
                    "type": "text",
                    "index": True,
                    "store": True,
                    "sortable": False,
                    "aggregatable": False,
                    "highlightable": True,
                    "term_positions": True
                },
                "announcement_content": {
                    "type": "text",
                    "index": True,
                    "store": True,
                    "sortable": False,
                    "aggregatable": False,
                    "highlightable": True,
                    "term_positions": True
                },
                "attachment": {
                    "type": "text",
                    "index": True,
                    "store": True,
                    "sortable": False,
                    "aggregatable": False,
                    "highlightable": True,
                    "term_positions": True
                },
                "amount": {
                    "type": "text",
                    "index": True,
                    "store": True,
                    "sortable": False,
                    "aggregatable": False,
                    "highlightable": True,
                    "term_positions": True
                },
                "contact_person": {
                    "type": "text",
                    "index": True,
                    "store": True,
                    "sortable": False,
                    "aggregatable": False,
                    "highlightable": True,
                    "term_positions": True
                },
                "contact_information": {
                    "type": "text",
                    "index": True,
                    "store": True,
                    "sortable": False,
                    "aggregatable": False,
                    "highlightable": True,
                    "term_positions": True
                },
                "link": {
                    "type": "text",
                    "index": True,
                    "store": True,
                    "sortable": False,
                    "aggregatable": False,
                    "highlightable": True,
                    "term_positions": True
                },
            }
        }
    }

    headers = {"Content-type": "application/json", "Authorization": "Basic " + bas64encoded_creds}
    zinc_host = host
    zinc_url = zinc_host + index

    res = requests.put(zinc_url, headers=headers, data=json.dumps(data))
    print(res.status_code)
    if res.status_code == 200:
        return "create successful"
    else:
        return "create failed"


def push(data: dict, id: int):
    headers = {"Content-type": "application/json", "Authorization": "Basic " + bas64encoded_creds}
    # data = "/api/" + index_name + "/_doc/"
    zinc_url = host + doc + str(id)
    res = requests.put(zinc_url, headers=headers, data=json.dumps(data))
    if res.status_code != 200:
        print("push data failed :", len(data), res.text)
    else:
        print("push data success :", len(data), id)


def get_data():
    headers = {"Content-type": "application/json", "Authorization": "Basic " + bas64encoded_creds}
    zinc_url = host + f"/es/{index_name}/_search"
    json_data = {"query": {"query_string": {"query": "深圳网"}}, "from": 0,
                 "size": 20}
    res = requests.post(zinc_url, headers=headers, json=json_data)
    if res.status_code != 200:
        print("get data failed :", res.text)
    print(res.text)


if __name__ == '__main__':
    create_index(index_name)
