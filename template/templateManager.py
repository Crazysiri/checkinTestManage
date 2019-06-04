#!/usr/bin/python
# -*- coding: UTF-8 -*-

import ruamel.yaml
from ruamel.yaml.util import load_yaml_guess_indent

import os
import sys


class TemplateConfig:
    
    yamlContent = None
    ind = None
    bsi = None
    
    project_name="" #项目名称
    project_number=""              #项目标号
    git_project_name=""  #git工程
    git_branch="" #提测分支
    self_is_test="""是 / dev环境"""            #研发是否自测
    test_options=""                                 #提测功能项
    review_members=""#代码Review人员
    project_pm=""#产品
    project_developers=""#开发
    project_pr_diff=""#提测内容pr
    project_ui=""#ui人员
    poject_comment=""#备注
    online_time=""#预计上线时间
    
    #部署发布顺序
    #上线发布的分支
    #上线时间
    #测试报告
    
    def readConfig(self,path):
        yamlContent,ind,bsi = load_yaml_guess_indent(open(path.decode('utf-8')))
        
        self.git_project_name  = yamlContent['git_project_name']
        self.project_name = yamlContent['project_name']
        self.git_branch  = yamlContent['git_branch']
        self.test_options  = yamlContent['test_options']
        self.review_members  = yamlContent['review_members']
        self.project_pm  = yamlContent['project_pm']
        self.project_developers  = yamlContent['project_developers']
        self.poject_comment  = yamlContent['poject_comment']
        self.project_ui  = yamlContent['project_ui']
        self.project_pr_diff = yamlContent['project_pr_diff']
    
        self.yamlContent = yamlContent
        self.ind = ind
        self.bsi = bsi
  
    def readConfigFromTemplate(self):

        path = os.path.dirname(os.path.realpath(__file__))
    
        configs_path = os.path.join(path,'template.yaml')
        
        self.readConfig(configs_path)

    def save(self,path):
        
        self.yamlContent['git_project_name'] = self.git_project_name
        self.yamlContent['project_name'] = self.project_name
        self.yamlContent['git_branch'] = self.git_branch
        self.yamlContent['test_options'] = self.test_options
        self.yamlContent['review_members'] = self.review_members
        self.yamlContent['project_pm'] = self.project_pm
        self.yamlContent['project_developers'] = self.project_developers
        self.yamlContent['poject_comment'] = self.poject_comment
        self.yamlContent['project_ui'] = self.project_ui
        self.yamlContent['project_pr_diff'] = self.project_pr_diff
        ruamel.yaml.round_trip_dump(self.yamlContent,open(path,'w'),indent=self.ind,block_seq_indent=self.bsi)

    def log(self):
        print('项目名称:'+self.project_name)
        print('提测分支:'+self.git_branch)
        print('测试项:'+self.test_options)
        print('代码review人员:'+self.review_members)
        print('pm:'+self.project_pm)
        print('开发者:'+self.project_developers)
        print('备注:'+self.poject_comment)
        print('git工程:'+self.git_project_name)
        print('ui:'+self.project_ui)
        print('pr:'+self.project_pr_diff)




if __name__ == "__main__":
    
    if sys.getdefaultencoding() != 'utf-8':
        reload(sys)
        sys.setdefaultencoding('utf-8')
    
    config = TemplateConfig()
    config.readConfigFromTemplate()
    config.log()
