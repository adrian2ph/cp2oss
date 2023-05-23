# -*- coding: utf-8 -*-
import os
import logging
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from .uploader_interface import UploaderInterface

class UploaderCos(UploaderInterface):
    def __init__(self):
        self.client = None
        self.bucket_name = None

    def initialize(self, secret_id: str, secret_key: str, region: str, bucket_name: str):
        # 配置密钥信息
        config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=None, Scheme='https')
        # 创建 COS 客户端
        self.client = CosS3Client(config)
        self.bucket_name = bucket_name

    def upload_file(self, file_path: str, object_name: str):
        if not self.client or not self.bucket_name:
            raise ValueError("UploaderCos not initialized. Call initialize() before uploading files.")
        
        # 检查文件是否存在
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File '{file_path}' not found.")

        # 本地路径 简单上传
        response = self.client.put_object_from_local_file(
            Bucket=self.bucket_name,
            LocalFilePath=file_path,
            Key=object_name,
        )

        if response['ETag'] and 'Error' not in response:
            logging.debug(f"File '{file_path}' uploaded successfully as '{object_name}'.")
        else:
            raise Exception(f"Error occurred while uploading file '{file_path}': {response['Response']['Error']['Message']}")
