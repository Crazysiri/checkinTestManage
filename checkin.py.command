#!/usr/bin/python
# -*- coding: UTF-8 -*-

import inviteMember
import createProject
import sendEmail
import sys



def main(argv):
    print('\n')
    print('-------------------------------------------------------')
    print('-------------------------------------------------------')
    print('                       功能list                         ')
    print('-------------------------------------------------------')
    print('1.创建提测任务（master切分支，创建提测邮件一部分）.')
#    print('\n')
    print('2.发提测邮件(选提测任务)')
#    print('\n')
    print('3.邀请人员进指定库（目前只有iOS的可以用）')
    print('-------------------------------------------------------')
    print('-------------------------------------------------------')
    type = int(raw_input('输入选择项：'))
    if type == 1:
        createProject.create()
    elif type == 2:
        sendEmail.send()
    elif type == 3:
        inviteMember.invite()

if __name__ == "__main__":
    main(sys.argv[1:])
