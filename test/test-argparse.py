#!/usr/bin/env python3
import argparse

# ./cp2oss.py -d localdir test01 demo01
parser = argparse.ArgumentParser(description='把本地文件夹复制到阿里云oss/腾讯云cos.')
parser.add_argument('-d', '--dir', help = '本地文件夹路径', required = True)
parser.add_argument('targets',
            metavar = 'TARGET',                   # var name used in help msg
            nargs = '+',                            # require one or more targets
            help = '目标存储名字')       # help msg explanation

args = parser.parse_args()
print('上传本地目录 {} 到 {}'.format(args.dir, ' '.join(args.targets)))
