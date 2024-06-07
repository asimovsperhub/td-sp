import logging
import os
import pickle
import sys
from typing import Any

import redis

sys.path.insert(
    0,
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
cache_cli = redis.StrictRedis(  # 缓存客户端对象
    host="81.71.49.57",
    db=2,
    password='Zhaobiao123..',
    socket_connect_timeout=1  # 链接超时设置为1秒
)


def set_cache(key: str, instance: Any, *args, **kwargs):
    data = pickle.dumps(instance)
    try:
        cache_cli.set(key, data, *args, **kwargs)
    except Exception as e:
        logging.getLogger().error(e)
    finally:
        return instance


def get_cache(key: str, default: Any = None) -> Any:
    try:
        data = cache_cli.get(key)
        if not data:
            return default
        default = pickle.loads(data)
    except Exception as e:
        logging.getLogger().error(e)
        return default
    else:
        return default


def del_cache(*keys: str):
    try:
        cache_cli.delete(*keys)
    except Exception as e:
        logging.getLogger().error(e)


if __name__ == '__main__':
    # cache_cli.hset("ntf_key","1","1")
    # print(cache_cli.hget("sign_hash",'1'))
    # import json
    # data = cache_cli.blpop("eth_getTransactionByHash",0)
    # print(data[1])
    # data = json.loads(data[1])
    # print(data)
    cache_cli.hincrby("opensea_lock:1265", 'b', amount=1)
    cache_cli.hincrby("opensea_lock", 'b', amount=1)
    cache_cli.hincrby("opensea_lock", 'b', amount=1)
    cache_cli.delete("opensea_lock")
    # cache_cli.hdel("opensea_lock",'a')
    cache_cli.set("abc:123", "123", ex=60 * 60 * 2)
