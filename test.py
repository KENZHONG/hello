import requests


print 'test'
print 'ok'
print 'yan'


html = requests.get('https://www.baidu.com')
print html.content.decode('utf8')