# -*- coding: utf-8 -*-
import oss2
import logging
from .uploader_interface import UploaderInterface

class UploaderOss(UploaderInterface):
    def __init__(self):
        self.auth = None
        self.bucket = None
        self.bucket_name = None

    def __str__(self):
        return f"阿里云对象存储{self.bucket_name}"
    
    def initialize(self, access_id: str, access_key: str, region: str, bucket_name: str):
        """
        初始化阿里云 OSS 认证和存储桶信息

        Args:
            access_id (str): 阿里云账号的 Access ID
            access_key (str): 阿里云账号的 Access Key
            region (str): 存储桶所在的地域
            bucket_name (str): 存储桶的名称
        """
        self.auth = oss2.Auth(access_id, access_key)
        self.bucket = oss2.Bucket(self.auth, region, bucket_name)
        self.bucket_name = bucket_name

    def upload_file(self, file_path: str, object_name: str) -> str:
        if not self.auth or not self.bucket:
            raise ValueError("UploaderOss not initialized. Call initialize() before uploading files.")
        
        response = self.bucket.put_object_from_file(object_name, file_path)
        if response.status == 200 and response.etag:
            logging.info(f"File '{file_path}' uploaded successfully as '{object_name}'.")
        else:
            # 获取错误信息
            error_message = response.headers.get('x-oss-request-id')
            raise Exception(f"Error occurred while uploading file '{file_path}': {error_message}")
        
        return object_name