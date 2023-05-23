#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import yaml
import argparse
import os
import sys
import queue
import logging
from uploader import UploaderFactory
from qcloud_cos.cos_threadpool import SimpleThreadPool

# 遍历目录文件，返回上传文件列表
def dir_to_upload_queue(upoad_dir, bucket_prefix) -> queue:
    # 文件上传列表，{ 'srcKey': srcKey, 'objectKey': objectKey }
    q = queue.Queue()

    # 获取文件夹绝对路径
    abspath = os.path.abspath(upoad_dir)
    # 遍历本地文件夹
    g = os.walk(abspath)
    for path, dir_list, file_list in g:
        for file_name in file_list:
            local_file = os.path.join(path, file_name)
            object_key = os.path.relpath(local_file, start=abspath).strip('/')
            object_key = os.path.join(bucket_prefix, object_key).strip('/')
            q.put({ 'local_file': local_file, 'object_key': object_key })
    return q
    
# 加载yml配置文件，拿到对应的密钥
def load_bucket_config(filename, name):
    with open(filename, 'r') as ymlFile:
        conf = yaml.safe_load(ymlFile)
        if 'buckets' not in conf or name not in conf['buckets']:
            errmsg = 'Invalid bucket!, --bucket {} 不在配置文件内, 请选择{}'.format(name, ' '.join([x for x in conf['buckets'].keys()]))
            raise Exception(errmsg)
        
        return conf['buckets'][name]

# 多线程上传文件
def process_upload(upload_queue, bucket_cfg):
    # 创建上传的线程池
    pool = SimpleThreadPool()
    uploader = UploaderFactory.create_uploader(bucket_cfg)
    while not upload_queue.empty():
        item = upload_queue.get()
        pool.add_task(uploader.upload_file, item['local_file'], item['object_key'])

    pool.wait_completion()
    result = pool.get_result()
    if not result['success_all']:
        logging.warning("Not all files upload sucessed. you should retry")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='把本地文件夹复制到阿里云oss/腾讯云cos.')
    parser.add_argument('-c', '--config', help = '配置文件, 默认是当前目录的config.yml')
    parser.add_argument('-d', '--dir', help = '本地文件夹路径', required = True)
    parser.add_argument('-b', '--bucket', help = '配置文件里的bucket名字', required = True)
    parser.add_argument('-p', '--prefix', help = '对象存储目录，默认空', required = False)

    # 获取参数
    args = parser.parse_args()
    configFile = args.config or 'config.yml'
    upoad_dir = args.dir
    bucket_prefix = args.prefix or ''
    bucket_nickname = args.bucket

    # 正常情况日志级别使用 INFO，需要定位时可以修改为 DEBUG，此时 SDK 会打印和服务端的通信信息
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    logging.info('上传本地目录 {} 到 {}:{}'.format(upoad_dir, bucket_nickname, bucket_prefix))

    # 加载配置文件获取oss/cos配置
    bucket_cfg = load_bucket_config(configFile, bucket_nickname)

    upload_queue = dir_to_upload_queue(upoad_dir, bucket_prefix)

    process_upload(upload_queue, bucket_cfg)

    
    