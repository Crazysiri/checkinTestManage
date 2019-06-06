#!/usr/bin/python
# -*- coding: UTF-8 -*-

#sudo pip install pyyaml
#sudo pip install requests
#pip install ruamel.yaml

import requests

import sys
import  os
import getopt
import yaml
import time

#此参数需要外部配置，授权获取token的，其中username password为 gitee账户密码
request_config_username = ''
request_config_password = ''
request_config_clientid = '4af0cd03a89df6c632efe70fe90623d94b4ee1a385ec147e0ff6c2d16ff42ff4'
request_config_clientsecret = 'f5211dc8261cf0c0d997eef6c8c3bce6adf65cab69a3d65d30cf32993c89161e'

class LenzRequest:
    
    token = ''
    owner = ''
    repo = ''
    
    def __init__(self,owner,repo):
        self.owner = owner
        self.repo = repo
    
        self.getToken()
    
    def getTokenInDisk(self):
        path = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(path,"configs/token.yaml")
    
        if not os.path.isfile(path):
            os.system("touch " + path)
        f = open(path,'r')
        
        content = f.read()
    
        content_yaml = yaml.load(content)
        
        try:
            token = content_yaml['token']
            date = int(content_yaml['date'])
        except TypeError:
            token = ''
            date = 0
        
        current_date = int(time.time())
        
        #12小时
        if current_date - date > 60 * 60 *12:
            self.token = None
        else:
            self.token = token
        f.close()

    def saveTokenToDisk(self):

        path = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(path,"configs/token.yaml")
        
        f = open(path,'r')
        content = f.read()

        content_yaml = {}
        
        f = open(path,'w')
        current_date = int(time.time())
        content_yaml['token'] = self.token
        content_yaml['date'] = current_date

        yaml.dump(content_yaml, f)

 
    #获取 授权token
    def getToken(self):
        
        self.getTokenInDisk()
        
        if not self.token:
            
            post_headers = {
                "Content-Type":'application/x-www-form-urlencoded'
            }

            params = {
                "grant_type":"password",
                "username":request_config_username,
                "password":request_config_password,
                "client_id":request_config_clientid,
                "client_secret":request_config_clientsecret,
#                    "scope":"user_info projects pull_requests issues notes keys hook groups gists enterprises"
                    "scope":"user_info projects pull_requests issues notes keys hook groups gists"

            }

            url = "https://gitee.com/oauth/token"
            req =  requests.post(url,params=params,headers=post_headers)
            result = req.json()
            print(str(result))
            self.token = result["access_token"]
            self.saveTokenToDisk()


                    
                    
    
#邀请 加入 某个库
    def inviteRepoMember(self,member,repo):
        url = 'https://gitee.com/api/v5/repos/'+self.owner+'/'+repo+'/collaborators/'+member
        
        post_headers = {
            "Content-Type":'application/json'
        }
        
        params = {
            "access_token":self.token,
            "owner":self.owner,
            "repo":repo,
            "username":member,
            "permission":"push"
        }
        
        
        result = requests.put(url,params=params,headers=post_headers)
        return result.json()


    def getAllPRS(self):
        url = 'https://gitee.com/api/v5/repos/'+self.owner+'/'+self.repo+'/pulls'

        post_headers = {
            "Content-Type":'application/json'
        }

        params = {
            "access_token":self.token,
            "owner":self.owner,
            "repo":self.repo,
            "state":"open",
            "sort":"created",
            "direction":"desc",
            "page":1,
            "per_page":20
        }

        req = requests.get(url,params=params,headers=post_headers)

        result = req.json()
        return result
            
                    
            
    #获取pr提交记录
    def getPRCommits(self,number):
        url = 'https://gitee.com/api/v5/repos/%s/%s/pulls/%s/commits' % (self.owner,self.repo,number)

        post_headers = {
            "Content-Type":'application/json'
        }

        params = {
            "access_token":self.token,
            "owner":self.owner,
            "repo":self.repo,
            "number":number
        }

        req = requests.get(url,params=params,headers=post_headers)

        return req.json()
    """
    {
        "sha": "2a94be825ce1ea2cd8d22f2aa10fac23ba19167d",
            "filename": "LenzBusiness/App部分逻辑说明文档",
            "status": null,
            "additions": "82",
            "deletions": "25",
            "blob_url": "https://gitee.com/ppz_bj/LenzBusiness/blob/2a94be825ce1ea2cd8d22f2aa10fac23ba19167d/LenzBusiness/App部分逻辑说明文档",
            "raw_url": "https://gitee.com/ppz_bj/LenzBusiness/raw/2a94be825ce1ea2cd8d22f2aa10fac23ba19167d/LenzBusiness/App部分逻辑说明文档",
            "patch": {
                "diff": "",
                "new_path": "LenzBusiness/App部分逻辑说明文档",
                "old_path": "LenzBusiness/App部分逻辑说明文档",
                "a_mode": "100644",
                "b_mode": "100644",
                "new_file": false,
                "renamed_file": false,
                "deleted_file": false,
                "too_large": false
    }
        }
    """
    #获取pr diff
    def getPRDiffs(self,number):
        
        url = 'https://gitee.com/api/v5/repos/%s/%s/pulls/%s/files' % (self.owner,self.repo,number)

        post_headers = {
            "Content-Type":'application/json'
        }
        
        params = {
            "access_token":self.token,
            "owner":self.owner,
            "repo":self.repo,
            "number":number
        }

        req = requests.get(url,params=params,headers=post_headers)
        return req.json()


    #创建pr
    def createPR(self,branch,title):
        
        url = 'https://gitee.com/api/v5/repos/'+self.owner+'/'+self.repo+'/pulls'

        post_headers = {
            "Content-Type":'application/json'
        }

        params = {
            "access_token":self.token,
            "title":title,
            "head":branch,
            "base":"master"
        }


        req = requests.post(url,params=params,headers=post_headers)
        result = req.json()
        success = False
        number = 0
        try:
            id = result['id']
            number = result['number']
            success = True
        except KeyError:
            success = False
        print('createPR'+str(result))
        return success,number


    
    #返回所有的评论 和 pr url
    def getPRByAllProcesses(self,branch,title):
        
        #first creat pr
        success,number = self.createPR(branch,title)
        if not success:
            #second if created get pr number in listlist
            result = self.getAllPRS()

            for pr in result:
                number = pr["number"]
                b = pr["head"]["ref"]
                if branch == b:
                    success = True
                    break

        result = self.getPRCommits(number)
        
        list = []
        
        for commit in result:
            list.append(commit['commit']['message'])
#            print('message:'+commit['commit']['message'])
        pr_url = 'https://gitee.com/%s/%s/pulls/%s' %(self.owner,self.repo,number)
        return list,pr_url



import ruamel.yaml
from ruamel.yaml.util import load_yaml_guess_indent




def main(argv):
    if sys.getdefaultencoding() != 'utf-8':
        reload(sys)
        sys.setdefaultencoding('utf-8')
    
    print ('\n')

    branch_for_pr = "feature/2019_05_14_吕博涧_时间打点"

    title = "pr:" + branch_for_pr

    request = LenzRequest('ppz_bj','LenzBusiness')
    request.getPRByAllProcesses(branch_for_pr,title)

    #btcxiaowu,zhang_jack,Lenz_ydd
#    result = request.inviteRepoMember('zhang_jack','LenzPictureQuestionModule')

#    result = getAllPRS(token,"LenzBusiness")




if __name__ == "__main__":
    main(sys.argv[1:])


