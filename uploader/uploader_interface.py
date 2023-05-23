# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod


class UploaderInterface(ABC):

    @abstractmethod
    def upload_file(self, file_path: str, object_name: str) -> str:
        """
        上传本地文件到对象存储

        Args:
            file_path (str): 文件本地路径名
            object_name (str): 对象存储路径
        """
        pass