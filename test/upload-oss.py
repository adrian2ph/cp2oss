# -*- coding: utf-8 -*-
import oss2
import os
# 阿里云账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM用户进行API访问或日常运维，请登录RAM控制台创建RAM用户。
auth = oss2.Auth('LTAI5tEHNr4ZsDRpbPM2yutT', 'yourAccessKeySecret')
# yourEndpoint填写Bucket所在地域对应的Endpoint。以华东1（杭州）为例，Endpoint填写为https://oss-cn-hangzhou.aliyuncs.com。
# 填写Bucket名称。
bucket = oss2.Bucket(auth, 'yourEndpoint', 'examplebucket')

# 必须以二进制的方式打开文件。
# 填写本地文件的完整路径。如果未指定本地路径，则默认从示例程序所属项目对应本地路径中上传文件。
with open('D:\\localpath\\examplefile.txt', 'rb') as fileobj:
    # Seek方法用于指定从第1000个字节位置开始读写。上传时会从您指定的第1000个字节位置开始上传，直到文件结束。
    fileobj.seek(1000, os.SEEK_SET)
    # Tell方法用于返回当前位置。
    current = fileobj.tell()
    # 填写Object完整路径。Object完整路径中不能包含Bucket名称。
    bucket.put_object('exampleobject.txt', fileobj)