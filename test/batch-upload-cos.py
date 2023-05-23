# -*- coding=utf-8
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from qcloud_cos import CosServiceError
from qcloud_cos import CosClientError
from qcloud_cos.cos_threadpool import SimpleThreadPool

import sys
import os
import logging

# 正常情况日志级别使用 INFO，需要定位时可以修改为 DEBUG，此时 SDK 会打印和服务端的通信信息
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

# 设置用户属性, 包括 secret_id, secret_key, region等。Appid 已在 CosConfig中 移除，请在参数 Bucket 中带上 Appid。Bucket 由 BucketName-Appid 组成
secret_id = os.environ['COS_SECRET_ID']     # 用户的 SecretId，建议使用子账号密钥，授权遵循最小权限指引，降低使用风险。子账号密钥获取可参见 https://cloud.tencent.com/document/product/598/37140
secret_key = os.environ['COS_SECRET_KEY']   # 用户的 SecretKey，建议使用子账号密钥，授权遵循最小权限指引，降低使用风险。子账号密钥获取可参见 https://cloud.tencent.com/document/product/598/37140
region = 'ap-beijing'      # 替换为用户的 region，已创建桶归属的 region 可以在控制台查看，https://console.cloud.tencent.com/cos5/bucket
                           # COS 支持的所有 region 列表参见 https://cloud.tencent.com/document/product/436/6224
token = None               # 如果使用永久密钥不需要填入 token，如果使用临时密钥需要填入，临时密钥生成和使用指引参见 https://cloud.tencent.com/document/product/436/14048

config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token)  # 获取配置对象
client = CosS3Client(config)

uploadDir = '/root/logs'
bucket = 'examplebucket-125000000'
g = os.walk(uploadDir)
# 创建上传的线程池
pool = SimpleThreadPool()
for path, dir_list, file_list in g:
    for file_name in file_list:
        srcKey = os.path.join(path, file_name)
        cosObjectKey = srcKey.strip('/')
        # 判断 COS 上文件是否存在
        exists = False
        try:
            response = client.head_object(Bucket=bucket, Key=cosObjectKey)
            exists = True
        except CosServiceError as e:
            if e.get_status_code() == 404:
                exists = False
            else:
                print("Error happened, reupload it.")
        if not exists:
            print("File %s not exists in cos, upload it", srcKey)
            pool.add_task(client.upload_file, bucket, cosObjectKey, srcKey)


pool.wait_completion()
result = pool.get_result()
if not result['success_all']:
    print("Not all files upload sucessed. you should retry")