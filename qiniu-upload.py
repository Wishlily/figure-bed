#coding=utf-8
import sys,os
from qiniu import Auth
from qiniu import BucketManager
import qiniu
import json

def parse(filename):
    configfile = open(filename)
    jsonconfig = json.load(configfile)
    configfile.close()
    return jsonconfig

def key(cf):
    key = cf['key']
    return key['access_key'], key['secret_key']

def up(cf):
    up = cf['up']
    return up['bucket_name']

def upload(q, bucket_name, f, name):
    if os.path.splitext(f)[1] in ['.jpg','.png', '.JPG']:
        token = q.upload_token(bucket_name, name)
        ret, info = qiniu.put_file(token, name, f)
        return info.status_code

if __name__ == '__main__':
    config = parse("qiniu.conf")
    access_key, secret_key = key(config)
    q = Auth(access_key, secret_key)
    bucket = BucketManager(q)

    bucket_name= up(config)

    count = 0
    path = './images/'
    for parent, dirnames, filenames in os.walk(path):
        count += len(filenames)
        for filename in filenames:
            filepath = os.path.join(parent,filename)
            print(filepath)
            name = filepath.replace(path,'')
            status_code = upload(q, bucket_name, filepath, name)
            if status_code != 200:
                print("up error:", status_code)
    print(count)
