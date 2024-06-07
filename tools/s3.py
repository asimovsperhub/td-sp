import io
import os
import sys
import urllib.parse

import requests
from minio import Minio

sys.path.insert(
    0,
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

def downloadFile(url) -> bytes:
    res = requests.get(url)
    content = res.content
    return content


def S3Upload(bucket: str, content: bytes, filename: str, filesize: int = 0):
    useSSL = False
    client = Minio(
        "42.193.247.183:9000",
        access_key="JvTpb5Gnt4qCL69v",
        secret_key="AnyVSSQK2aTWM2QmE3HjZQB1040gYB5L", secure=useSSL
    )
    found = client.bucket_exists(bucket)
    if not found:
        client.make_bucket(bucket)
    # 存储桶，路径，[]byte,大小
    # Upload unknown sized data  length=-1, part_size=10*1024*1024, 大文件内存可能出问题
    result = client.put_object(
        "announcement", filename, io.BytesIO(content), length=-1, part_size=10 * 1024 * 1024,
    )
    return result


if __name__ == '__main__':
    url = "https://gf.gzggzy.cn/gz2/M00/8C/0E/CsUnsmQdOTeATPiTAACCtr4m3x483.xlsx?fileId=8a45a732842dfd9c0187122782b277df&attname=110KV%E5%BC%80%E5%8F%91%E5%8C%BA%E7%AB%99%E8%87%B3%E7%A6%8F%E8%80%80%E7%AB%99%E7%94%B5%E5%8A%9B%E7%AE%A1%E6%B2%9F%E5%B7%A5%E7%A8%8B%28%E5%9C%9F%E5%BB%BA%E9%83%A8%E5%88%86%29%E6%96%BD%E5%B7%A5%E6%80%BB%E6%89%BF%E5%8C%85-%E6%B8%85%E5%8D%951.xlsx"
    url = urllib.parse.unquote(url)
    filename = url.split("=")[-1]
    filename = "/ygp/" + filename
    print(url, filename)
    content = downloadFile(url)
    if content:
        result = S3Upload("announcement", content, filename)
        print(result.object_name)
