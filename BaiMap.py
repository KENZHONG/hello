# -*- coding: utf-8 -*-
"""
Created on Fri Dec 21 11:11:46 2018

@author: kenneth
"""

import json
import requests

print 'aa'
def getlnglat(address):
    url = 'http://api.map.baidu.com/geocoder/v2/'
    params = {
        'address':address,
        'output' : 'json',
        'ak' : 'R1k39PI3LVP2XjHI2PLe8dwhp1KQUCZV'
    }
    html = requests.get(url, params = params)
    return html
    
print getlnglat('GUANGZHOU').text