
## 使用示例

* 上传本地dist文件夹到名字为test01存储的`h5`路径下

    ./cp2oss.py  -d ./dist -b test01 -p h5

* 指定配置文件

    ./cp2oss.py -c ./config.yml  -d ./dist -b test01 -p h5


  ./cp2oss.py  -d /Users/adrian/Downloads/dist -b test01 -p h5


* 使用帮助

```
adrian@adriandeMacBook-Pro oss4cmd % ./cp2oss.py -h

usage: cp2oss.py [-h] [-c CONFIG] -d DIR -b BUCKET [-p PREFIX]

把本地文件夹复制到阿里云oss/腾讯云cos.

options:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        配置文件, 默认是当前目录的config.yml
  -d DIR, --dir DIR     本地文件夹路径
  -b BUCKET, --bucket BUCKET
                        配置文件里的bucket名字
  -p PREFIX, --prefix PREFIX
                        对象存储目录，默认空
```



## 配置文件 config.yml

配置文件记录了对象存储到密钥信息，其中type指定类型，只能是oss或者cos.

./cp2oss.py -c ./config2.yml -d /Users/adrian/Downloads/dist   -b test01 -p h5 -h

```
buckets:
  test01:
    type: oss
    access_id: LTAI5tEHNr4ZsDRpbPM2yutT
    access_key: VJyWHbShpAQ1yOVALbKGets7Vgi56y
    region: oss-cn-hongkong.aliyuncs.com
    bucket: adriandemo

  demo01:
    type: cos
    secret_id: 'AKIDuR9lALHE9EGDA5ze5ymNn5C94rdEahru'
    secret_key: '4vundQ2TuBGKE3e2T4WyGKFzY3bHo9RZ'
    region: 'ap-hongkong'
    bucket: 'adriandemo-1309875009'
```

## install requirements

    pip3 install -r requirements.txt

