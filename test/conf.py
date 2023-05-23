import yaml

with open('config.yml', 'r') as ymlFile:
    conf = yaml.safe_load(ymlFile)
    print(conf['oss']['test001'])

