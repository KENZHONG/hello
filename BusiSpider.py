#!/usr/bin/env python
#-*-coding:utf8-*-

import requests
import re
from requests.exceptions import RequestException

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


#browser =  webdriver.PhantomJS(executable_path = r'D:\tool\phantomjs-2.1.1-windows\phantomjs-2.1.1-windows\bin\phantomjs.exe')
# chrome_options = Options()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
# browser =  webdriver.Chrome('D:\\tool\\chromedriver_win32\\chromedriver.exe',chrome_options=chrome_options)

base_url = u'http://gd.122.gov.cn'
detail_url = u'http://gd.122.gov.cn/publicitypage?size=20&page=1&tjyf=201810&fzjg=%E7%B2%A4E&fwdmgl=6003'

def search(url):
    browser =  webdriver.Chrome('D:\\tool\\chromedriver_win32\\chromedriver.exe')
    wait =  WebDriverWait(browser, 10)
    browser.get(url)
    print browser.page_source.encode('utf8')
    browser.close()
    #input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR),'body > div > div:nth-child(3) > table'))
    return


###抓取网页
def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def get_list_link(html):
    pattern = re.compile('<iframe id="staticresult".*?src\="(.*?)".*?holdsrc',re.S)
    result = pattern.search(html)
    ret =  base_url+result.group(1)
    return str(ret)


def get_onepage_count(html):
    num = 0
    #pattern = re.compile('<td>(\d+)</td>',re.S)
    pattern = re.compile('<td title.*?</td>.*?<td>(.*?)</td>',re.S)
    result = pattern.findall(html)
    for x in result :
        if len(x) == 8 or x =='--':
            pass
        else:
            num += int(x)
    #print num
    return num

def get_page_num(html):
    num = 1
    pattern = re.compile(u'条记录.*?/(\d+)页',re.S)
    result = pattern.search(html)
    num = result.group(1)
    return int(num)

def gen_url(time_ym, page_index):
    #url = u'http://gd.122.gov.cn/publicitypage?size=20&page=1&tjyf=201810&fzjg=%E7%B2%A4E&fwdmgl=6003'
    url = u'http://gd.122.gov.cn/publicitypage?size=20&page='+str(page_index)+u'&tjyf='+time_ym+u'&fzjg=%E7%B2%A4E&fwdmgl=6003'
    #print url
    return url

def get_ym_count(time_ym):
    total_count = 0
    url = gen_url(time_ym,'1')
    html = get_one_page(url)
    page_num = get_page_num(html)
    total_count = get_onepage_count(html)
    print page_num
    page_count = 0
    for i in range(2,page_num):
        url = gen_url(time_ym, i)
        html = get_one_page(url)
        page_count = get_onepage_count(html)
        #print page_count
        total_count += page_count
    print time_ym,total_count
    return total_count

def main():
    #url = u'http://gd.122.gov.cn/views/noticestatic.html?fzjg=粤E&tjyf=201811&fwdmgl=6003'
    #url = u'http://gd.122.gov.cn/group1/M01/2E/FB/ra0KC1wBpN2ANo8CAAAYaBXK8hg83.html'

    # html = get_one_page(url)
    # list_url = get_list_link(html)
    # html = get_one_page(list_url)
    # num = get_onepage_count(html)

    #html = get_one_page(u'http://gd.122.gov.cn/publicitypage?size=20&page=1&tjyf=201810&fzjg=粤E&fwdmgl=6003')

    # total_count = 0
    # url = gen_url('201810','1')
    # html = get_one_page(detail_url)
    # page_num = get_page_num(html)
    # total_count = get_onepage_count(html)
    # print page_num
    # page_count = 0
    # for i in range(2,page_num):
    #     url = gen_url('201810', i)
    #     html = get_one_page(url)
    #     page_count = get_onepage_count(html)
    #     print page_count
    #     total_count += page_count
    # print total_count
    #print html.encode('utf8')

    ym_count = 0
    ym_2018 = ['201801','201802','201803','201804','201805','201806','201807','201808','201809','201810','201811','201812']
    ym_2017 = ['201701','201702','201703','201704','201705','201706','201707','201708','201709','201710','201711','201712']
    ym_2016 = ['201601','201602','201603','201604','201605','201606','201607','201608','201609','201610','201611','201612']
    ym_2015 = ['201501','201502','201503','201504','201505','201506','201507','201508','201509','201510','201511','201512']
    for x in ym_2018 :
        ym_count += get_ym_count(x)
        print x,ym_count
    print ym_count

    # pattern = re.compile('<td title.*?</td>.*?<td>(.*?)</td>',re.S)
    # result = pattern.findall(html)
    # print result

    return


if __name__=='__main__':
    main()