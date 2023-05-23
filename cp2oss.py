#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import yaml
import argparse
import os
import sys
import queue
import logging
from uploader import UploaderFactory, UploaderInterface
from qcloud_cos.cos_threadpool import SimpleThreadPool
from typing import TypedDict
import progressbar

#  上传文件列表类型
class UploadQueueItem(TypedDict):
    local_file: str
    object_key: str
    

def dir_to_upload_queue(upoad_dir: str, bucket_prefix: str) -> queue.Queue[UploadQueueItem]:
    """
    遍历目录，返回文件列表

    args:
        upoad_dir (str): 本地文件夹路径
        bucket_prefix (str): 对象存储路径
    """
    q = queue.Queue[UploadQueueItem]()

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


def load_bucket_config(filename: str, name: str) -> dict:
    """
    加载yml配置文件，拿到对应的密钥

    Args:
        filename (str): 文件本地路径名
        uploader (UploaderInterface): 上传对象
    """
    with open(filename, 'r') as ymlFile:
        conf = yaml.safe_load(ymlFile)
        if 'buckets' not in conf or name not in conf['buckets']:
            errmsg = 'Invalid bucket!, --bucket {} 不在配置文件内, 请选择{}'.format(name, ' '.join([x for x in conf['buckets'].keys()]))
            raise Exception(errmsg)
        
        return conf['buckets'][name]

class UploadingBar:
    def __init__(self, max_value) -> None:
        self.counter = 0
        self.bar = progressbar.ProgressBar(max_value=max_value)

    def update(self, n=1):
        self.counter += n
        self.bar.update(self.counter)

def process_upload(upload_queue: queue.Queue[UploadQueueItem], uploader: UploaderInterface):
    """
    多线程执行文件上传任务

    Args:
        upload_queue (dict): 文件本地路径名
        uploader (UploaderInterface): 上传对象
    """

    # 上传进度条
    bar = UploadingBar(upload_queue.qsize())
    def upload_handler(local_file: str, object_key: str):
        res = uploader.upload_file(local_file, object_key)
        bar.update()
        return res

    # 创建上传的线程池
    pool = SimpleThreadPool()
    nums_file = 0
    while not upload_queue.empty():
        # 统计要上传文件的个数
        nums_file = nums_file + 1
        item = upload_queue.get()
        # pool.add_task(uploader.upload_file, item['local_file'], item['object_key'])
        pool.add_task(upload_handler, item['local_file'], item['object_key'])

    pool.wait_completion()
    result = pool.get_result()

    if not result['success_all']:
        logging.warning("Not all files upload sucessed. you should retry")

    # 从线程的返回中获取上传成功的文件列表
    nested_list = [x[2] for x in result.get('detail')]
    combined_list = [item for sublist in nested_list for item in sublist]
    # 字符串排序
    uploaded_list = sorted(combined_list, key=str)
    
    # 打印文件列表到控制台
    print('\n'.join(uploaded_list))

    # 上传文件数量不匹配警告
    if nums_file != len(uploaded_list):
        logging.error('理应上传 {}, 成功上传 {}, 可能部分文件上传失败，请检查！'.format(nums_file, len(uploaded_list)))
    
    print('上传到{}共{}个'.format(uploader, nums_file))

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
    logging.basicConfig(level=logging.WARN, stream=sys.stdout)

    logging.info('上传本地目录 {} 到 {}:{}'.format(upoad_dir, bucket_nickname, bucket_prefix))

    # 加载配置文件获取oss/cos配置
    bucket_cfg = load_bucket_config(configFile, bucket_nickname)
    # 获取文件上传对象
    uploader = UploaderFactory.create_uploader(bucket_cfg)

    upload_queue = dir_to_upload_queue(upoad_dir, bucket_prefix)
    process_upload(upload_queue, uploader)

    
    