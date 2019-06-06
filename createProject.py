#!/usr/bin/python
# -*- coding: UTF-8 -*-

#import urllib.request
#from urllib import request,parse
# pip install ruamel.yaml

import sys
import  os
import getopt
import time
import io

import git
from git import Repo

import ruamel.yaml
from ruamel.yaml.util import load_yaml_guess_indent


path = os.path.dirname(os.path.realpath(__file__))

sys.path.append(path+'/framework')
from translate import translate_baidu
sys.path.append(path+'/template')
from templateManager import TemplateConfig

#log = master.log()

#currentCommit = repo.commit(currentBranch)
#compareCommit = repo.commit(compareBranch)

#diffed = repo.log(currentBranch,compareBranch)
#print(currentCommit+currentCommit)


#commits = list(repo.iter_commits(currentBranch))[:5]
#for commit in commits:
#    print('author:%s email:%s' % (commit.author.name,commit.author.email))

def getGitBranchNameFromTaskName(taskName):

    content = translate_baidu(taskName)

    return handleTranslateStr(content)

#首字母大写然后拼接
def handleTranslateStr(content):

    comps = content.split(' ')
    comps_new = []
    for com in comps:
        com = com.capitalize()
        comps_new.append(com)
    return ''.join(comps_new)


def create():
    if sys.getdefaultencoding() != 'utf-8':
        reload(sys)
        sys.setdefaultencoding('utf-8')
    
    path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(path,'config.yaml')
    yamlContent,ind,bsi = load_yaml_guess_indent(open(path))
    
    
    print ('\n')
    print ('\n')
    #    'LenzBusiness' 'LenzMember'
    print('-----------------------------------')
    print('工程列表:')
    count = 0
    for p in yamlContent['project_list']:
        count += 1
        print(str(count)+'.'+p['prefix'])
    print('-----------------------------------')
    repo_index = int(raw_input('请输入工程名称索引:'))
    print('-----------------------------------')
    repo_name = yamlContent['project_list'][repo_index - 1]['repo_name']
    prefix = yamlContent['project_list'][repo_index - 1]['prefix']

    pm_name = ''
    task_name = ''

    print ('\n')
    print('-----------------------------------')
    print('生成 feature/时间_任务名称')
    print('例子 feature/20190516_时间打点')
    print('-----------------------------------')
    print('-----------------------------------')
    print('pm列表：')
    count = 0
    for p in yamlContent['pm_list']:
        count += 1
        print(str(count)+'.'+p)
    pm_index = int(raw_input('请输入PM名字索引:'))
    pm_name = yamlContent['pm_list'][pm_index-1]
    print('-----------------------------------')

    
    print ('\n')
    print('-----------------------------------')
    while task_name == '':
        task_name = raw_input('请输入任务名称(不要带空格)：')
    print('-----------------------------------')


    taskName = getGitBranchNameFromTaskName(task_name)

    date_string = time.strftime("%Y%m%d",time.localtime())

    just_test_branch = date_string + '_' + taskName #用作文件名

    test_branch = 'feature/' + date_string + '_' + taskName
    print ('\n')
    print ('\n')

    in_text = ''
    
    test_options = ''
    
    print('-----------------------------------')
    print('项目测试项：---------一行一个---------')
    print('相机优化 ')
    print('主任务列表优化 ')
    print('最后输入 q 回车 结束输入')
    print('-----------------------------------')
    print('请输入项目测试项:')

    count = 0

    while in_text != 'q':
        count += 1
        in_text = raw_input()
        if in_text != 'q':
            test_options += str(count) + '.' + in_text
            test_options += '\n'
    print('-----------------------------------')

    print ('\n')



    
#git 打新分支 默认 feature/xxx

    repo = Repo('~/' + repo_name)
    master = repo.heads.master
    currentBranch = repo.head.reference
    if currentBranch != master:
        master.checkout()
    git = repo.git
    git.checkout('master',b=test_branch)

    print('切分支成功：')
    print(test_branch)

#yaml文件更新

    config = TemplateConfig()
    config.readConfigFromTemplate()
    
    config.git_branch = test_branch
    config.git_project_name = repo_name
    config.test_options = test_options
    config.project_pm = pm_name
    config.project_name = prefix + ' ' + task_name

    yaml_name = just_test_branch+'_config.yaml'
    path = os.path.dirname(os.path.realpath(__file__))
    yamlPath = os.path.join(path,'configs/' + yaml_name)

    if not os.path.isfile(yamlPath):
        os.system("touch " + yamlPath)

    path = os.path.dirname(os.path.realpath(__file__))
    with io.open(path+'/configs/configs','a',encoding='utf-8') as f:
        f.write(yaml_name)
        f.write(u'\n')

    config.save(yamlPath)

    print('存储到本地配置成功：')
    print(test_options)

def main(argv):
    create()

if __name__ == "__main__":
    main(sys.argv[1:])

#可优化：1.项目名称和产品通过配置文件 2.自动抓取上一次对应项目的模版
