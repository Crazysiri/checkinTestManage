#!/usr/bin/python
# -*- coding: UTF-8 -*-

import inviteMember
import createProject
import sendEmail
import sys



def main(argv):

    print('功能list:')
    print('1.创建提测任务（master切分支，创建提测邮件一部分）.')
    print('2.提测(选任务)')
    print('3.邀请人员进指定库（目前只有iOS的可以用，其它可忽略）')
    type = int(raw_input('输入选择项：'))
    if type == 1:
        createProject.create()
    elif type == 2:
        sendEmail.send()
    elif type == 3:
        inviteMember.invite()

if __name__ == "__main__":
    main(sys.argv[1:])
