#!/usr/bin/python
# -*- coding: UTF-8 -*-

import getopt
import sys
import  os

path = os.path.dirname(os.path.realpath(__file__))
path = path+'/framework'
sys.path.append(path)
import requestLenz
from requestLenz import LenzRequest

import ruamel.yaml
from ruamel.yaml.util import load_yaml_guess_indent

#工程配置（git账户密码，邮箱账户密码等等）
class ProjectConfig:
    
    config = None
    
    def read(self):
        path = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(path,'config.yaml')
        yamlContent,ind,bsi = load_yaml_guess_indent(open(path))
        self.config = yamlContent

p_config = ProjectConfig()
p_config.read()

def invite():
    
    requestLenz.request_config_username = p_config.config['git_user']
    requestLenz.request_config_password = p_config.config['git_pass']
    
    request = LenzRequest('ppz_bj','')
    
    repo = raw_input('输入要邀请的项目(LenzBusiness)：')
    members = ['btcxiaowu','zhang_jack','Lenz_ydd']
    for member in members:
        result = request.inviteRepoMember(member,repo)
        print(str(result))


def main(argv):
    invite()

if __name__ == "__main__":
    main(sys.argv[1:])

