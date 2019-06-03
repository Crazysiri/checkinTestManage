#/usr/bin/env python
#coding=utf8
 
import httplib
import md5
import urllib
import random
import json

appid = '20190601000303970' #你的appid
secretKey = 'nGFLJErsGa1OODBkOQ35' #你的密钥


def translate_baidu(content):

    httpClient = None
    myurl = '/api/trans/vip/translate'
    q = content
    fromLang = 'zh'
    toLang = 'en'
    salt = random.randint(32768, 65536)

    sign = appid+q+str(salt)+secretKey
    m1 = md5.new()
    m1.update(sign)
    sign = m1.hexdigest()
    myurl = myurl+'?appid='+appid+'&q='+urllib.quote(q)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign
    
    try:
        httpClient = httplib.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)
     
        #response是HTTPResponse对象
        response = httpClient.getresponse()
        result = response.read().decode('utf-8')
        result = json.loads(result)
        return result['trans_result'][0]['dst']
    except Exception, e:
        print(e)
        return content
    finally:
        if httpClient:
            httpClient.close()


if __name__ == "__main__":
    result = translate_baidu('5月优化')
    print(result)
