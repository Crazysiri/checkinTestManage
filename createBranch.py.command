#!/usr/bin/python
# -*- coding: UTF-8 -*-

import getopt
import sys
import  os
import time

path = os.path.dirname(os.path.realpath(__file__))
path = path+'/framework'
sys.path.append(path)
import requestLenz
from requestLenz import LenzRequest

def create():
    if sys.getdefaultencoding() != 'utf-8':
        reload(sys)
        sys.setdefaultencoding('utf-8')
    requestLenz.request_config_username = 'qiuyoubo@lenztechretail.com'
    requestLenz.request_config_password = 'zxcv12'
    
    repo = ''
    type = int(raw_input('请输入要创建分支的工程(1-LenzBusiness 2-LenzMember):'))
    if type == 1:
        repo = 'LenzBusiness'
    elif type == 2:
        repo = 'LenzMember'

    input_branch = raw_input('输入要创建的分支：')

    request = LenzRequest('ppz_bj',repo)

    date_string = time.strftime("%Y%m%d",time.localtime())

    branch = 'rtag/'+date_string+'_'+input_branch
    request.createNewBranch(branch,'master')

    json = request.getAllBranches()
    list = []
    for dict in json:
        list.append(dict['name'])

    for item in list:
        if item == branch:
            print('创建成功:'+item)

def main(argv):
    create()

if __name__ == "__main__":
    main(sys.argv[1:])
