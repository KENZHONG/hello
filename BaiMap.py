#!/usr/bin/env python
#-*-coding:utf8-*-

import json
import requests





print 'aa'
def getlnglat(address):
    url = 'http://api.map.baidu.com/geocoder/v2/'
    headers = { 'Connection':'close'}
    params = {
        'address':address,
        'output' : 'json',
        'ak' : 'R1k39PI3LVP2XjHI2PLe8dwhp1KQUCZV'
    }
    requests.adapters.DEFAULT_RETRIES = 5 # 增加重连次数
    s = requests.session()
    s.keep_alive = False # 关闭多余连接
    #s.proxies = {"https": "47.100.104.247:8080", "http": "36.248.10.47:8080", }
    #print address
    html = s.get(url,headers = headers, params = params)
    return html

def main():
    with open ('C:\Users\Administrator\Desktop\pgone\location.txt', 'a+') as fw:
        with open('C:\\Users\\Administrator\\aa.txt') as f:
            line = f.readline()
            while line:
                line = f.readline()
                print line
                area_no,area_name = line.split('|')
                location =  getlnglat(area_name).text
                print type(location), type(area_name)
                tmp = '%s|%s|%s|\n' % (area_no, area_name.strip(), location.encode('utf-8'))
                fw.writelines(tmp)
                #print('{0}|{1}|{2}|' .format(area_no,area_name,location))



if __name__ == '__main__':
    print getlnglat('广州市天河区荟雅苑幼儿园').text
    #main()

#print getlnglat('广东河源市源城区').text