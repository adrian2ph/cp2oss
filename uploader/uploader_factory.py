# -*- coding: utf-8 -*-
from .uploader_interface import UploaderInterface
from .cos import UploaderCos
from .oss import UploaderOss
from typing import TypedDict

class UploaderConfigOss(TypedDict):
    """
    阿里云oss配置参数
    """
    type: str
    access_id: str
    access_key: str
    region: str
    bucket: str

class UploaderConfigCos(TypedDict):
    """
    腾讯云cos配置参数
    """
    type: str
    secret_id: str
    secret_key: str
    region: str
    bucket: str

class UploaderFactory:
    """
    工厂模式创建上传实例
    """
    @staticmethod
    def create_uploader(cfg: UploaderConfigCos | UploaderConfigOss) -> UploaderInterface:
        uploader = None
        bucket_type = cfg.get('type')
        if bucket_type == 'oss':
            uploader = UploaderOss()
            uploader.initialize(cfg['access_id'], cfg['access_key'], 
                cfg['region'], cfg['bucket'])
        elif bucket_type == 'cos':
            uploader = UploaderCos()
            uploader.initialize(
                cfg['secret_id'], cfg['secret_key'], 
                cfg['region'], cfg['bucket'])
        else:
            raise Exception('对象存储配置错误', cfg)
        return uploader
