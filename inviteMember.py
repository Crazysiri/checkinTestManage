#!/usr/bin/python
# -*- coding: UTF-8 -*-

import getopt
import sys
import  os

sys.path.append('./framework')
from requestLenz import LenzRequest



def main(argv):

    request = LenzRequest('ppz_bj','')

    repo = raw_input('输入要邀请的项目(LenzBusiness)：')
    members = ['btcxiaowu','zhang_jack','Lenz_ydd']
    for member in members:
        result = request.inviteRepoMember(member,repo)
        print(str(result))

if __name__ == "__main__":
    main(sys.argv[1:])
