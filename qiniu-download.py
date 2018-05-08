# -*- coding: utf-8 -*-
from qiniu import Auth
from qiniu import BucketManager

import json
import requests
import os

def parse(filename):
    configfile = open(filename)
    jsonconfig = json.load(configfile)
    configfile.close()
    return jsonconfig

def key(cf):
    key = cf['key']
    return key['access_key'], key['secret_key']

def down(cf):
    down = cf['down']
    return down['bucket_name'], down['url']

if __name__ == '__main__':
    config = parse("qiniu.conf")
    access_key, secret_key = key(config)
    q = Auth(access_key, secret_key)
    bucket = BucketManager(q)

    # 存储空间名和URL
    bucket_name, url = down(config)
    # 前缀
    prefix = ''
    # 列举条目
    limit = 200
    # 列举出除'/'的所有文件以及以'/'为分隔的所有前缀
    delimiter = None
    # 标记
    marker = None
    path = './images/'
    ret, eof, info = bucket.list(bucket_name, prefix, marker, limit, delimiter)
    for i in ret['items']:
        img = i['key']
        img_path = path + img[:img.rindex('/')]
        print(img)
        base_url = url + '/' + img
        # print(base_url)
        # 如果空间有时间戳防盗链或是私有空间，可以调用该方法生成私有链接
        private_url = q.private_download_url(base_url, expires=100)
        # print(private_url)
        r = requests.get(private_url)
        if r.content:
            if not os.path.exists(img_path):
                os.makedirs(img_path)
            file = open(path + img, "wb")
            file.write(r.content)
            file.flush()
            file.close()