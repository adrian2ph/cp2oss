from .uploader_interface import UploaderInterface
from .cos import UploaderCos
from .oss import UploaderOss

class UploaderFactory:
    @staticmethod
    def create_uploader(cfg) -> UploaderInterface:
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
            raise Exception('配置错误', cfg)
        return uploader
