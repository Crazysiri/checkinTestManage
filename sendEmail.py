#!/usr/bin/python
# -*- coding: UTF-8 -*-


import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
import time
import  os
import getopt
import sys
import io

import ruamel.yaml
from ruamel.yaml.util import load_yaml_guess_indent


import git
from git import Repo

sys.path.append('./framework')
import requestLenz
from requestLenz import LenzRequest
from requestLenz import request_config_username
from requestLenz import request_config_password

sys.path.append('./template')
from templateManager import TemplateConfig



class ProjectConfig:

    config = None
    
    def read(self):
        path=os.getcwd()
        path = os.path.join(path,'config.yaml')
        yamlContent,ind,bsi = load_yaml_guess_indent(open(path))
        self.config = yamlContent

p_config = ProjectConfig()
p_config.read()

#第三方 smtp 服务
mail_host="smtp.exmail.qq.com"
mail_user=p_config.config['mail_user']
mail_pass=p_config.config['mail_pass']

sender = p_config.config['mail_sender']
to_receivers = p_config.config['to_receivers']
copy_receivers = p_config.config['copy_receivers']

#to_receivers = ['lisijie@ppznet.com','liyapei@lenztechretail.com','wangsong@lenztechretail.com','yinjianzhuo@lenztechretail.com']
#copy_receivers = ['dev_all@lenztechretail.com','cpz@lenztechretail.com']
receivers = to_receivers + copy_receivers

#git相关
#获取代码开发者:name就是目录的名字 类似。LenzBusiness，远程clone下来的和本地一样的名字
#暂时名字写死 回头如果可以 会写成配置文件
def getDevelopers(name,branch):
    dev_array = []
    g = git.Git('~/'+name)
    commitMessages = g.log('%s...%s' % (branch,'master'),'--pretty=format:%ad %an - %s','--abbrev-commit').split('\n')
    for msg in commitMessages:
        print(msg)
        if 'zero' in msg:
            if '仇友博' not in dev_array:
                dev_array.append('仇友博')
        elif 'wudeliang' in msg:
            if '武得亮' not in dev_array:
                dev_array.append('武得亮')
        elif 'yuandongdong' in msg:
            if '袁冬冬' not in dev_array:
                dev_array.append('袁冬冬')
        elif 'Jack_199010177098' in msg:
            if '张杰林' not in dev_array:
                dev_array.append('张杰林')
    return ','.join(dev_array)

#文本转html
def textToHtml(text):
    if text == '':
        newText = '<br class="">'
    else:
        list = text.split('\n')
        
        if len(list) == 1:
            newText = text
        else:
            newText = '<br class="">'.join(list)
    return newText;

def email_row(title,content,highlighted):
    bg = 'background-color: rgb(246, 248, 250);'
    if not highlighted:
        bg = ''
    row_msg="""
        <tr style="box-sizing: border-box; border-top-width: 1px; border-top-style: solid; border-top-color: rgb(198, 203, 209);"""+bg+""" " class="">
        <td style="box-sizing: border-box; padding: 6px 13px; border: 1px solid rgb(223, 226, 229);" class="">"""+title+"""</td>
        <td align="left" style="box-sizing: border-box; padding: 6px 13px; border: 1px solid rgb(223, 226, 229);" class="">"""+content+"""
            </td>
        </tr>
    """
    return row_msg

def email_content(config):
    
    list = [{'title':'项目名称','content':textToHtml(config.project_name)},
            {'title':'项目编号','content':textToHtml(config.project_number)},
            {'title':'Git工程','content':textToHtml(config.git_project_name)},
            {'title':'提测分支','content':textToHtml(config.git_branch)},
            {'title':'研发是否已自测/自测环境','content':textToHtml(config.self_is_test)},
            {'title':'提测功能项','content':textToHtml(config.test_options)},
            {'title':'代码Review人员','content':textToHtml(config.review_members)},
            {'title':'产品','content':textToHtml(config.project_pm)},
            {'title':'开发','content':textToHtml(config.project_developers)},
            {'title':'数据库表变更sql','content':''}
            ,{'title':'UI','content':textToHtml(config.project_ui)}
            ,{'title':'提测内容pr diff','content':textToHtml(config.project_pr_diff)}
            ,{'title':'备注','content':textToHtml(config.poject_comment)}
            ,{'title':'预计上线时间','content':'未知'}
            ,{'title':'部署发布顺序','content':''}
            ,{'title':'上线发布的分支名称（qa填写）','content':''}
            ,{'title':'上线时间（qa填写）','content':''}
            ,{'title':'测试报告（qa填写）','content':''}

            ]
    
    content = ''
    count = 0
    for row in list:
        count += 1
        if count % 2 == 1:
            highlighted = False
        else:
            highlighted = True
        
        content += email_row(row['title'],row['content'],highlighted)
    
    mail_msg="""
    <div style="position:relative;">
        <div class="">
            <div style="  ;; font-size: 14px; " class="">
                <div style="  ; ; ; " class="">
                    <table style="box-sizing: border-box; border-collapse: collapse; border-spacing: 0px; max-width: 100%; margin-top: 0px; display: block; width: 1170.2px; overflow: auto; color: rgb(64, 72, 91);" class="">
                        <thead style="box-sizing: border-box;" class=""><tr style="box-sizing: border-box; border-top-width: 1px; border-top-style: solid; border-top-color: rgb(198, 203, 209);" class=""><th style="box-sizing: border-box; padding: 6px 13px; border: 1px solid rgb(223, 226, 229);" class="">提测申请/发布申请</th><th align="left" style="box-sizing: border-box; padding: 6px 13px; border: 1px solid rgb(223, 226, 229);" class=""></th></tr>
                        </thead>
                        <tbody style="box-sizing: border-box;" class="">
                            """+content+"""
                        </tbody>
                    </table>
                </div>
                <div style="  ; ; ; " class=""></div>
        </div>
    </div>
    <br class="">

    ------------------</span></div><div><includetail><div style="font:Verdana normal 14px;color:#000;"><div style="position:relative;"><div class=""><div dir="auto" style="caret-color: rgb(0, 0, 0); color: rgb(0, 0, 0); letter-spacing: normal; text-align: start; text-indent: 0px; text-transform: none; white-space: normal; word-spacing: 0px; -webkit-text-stroke-width: 0px; text-decoration: none; word-wrap: break-word; -webkit-nbsp-mode: space; line-break: after-white-space;" class=""><div dir="auto" style="word-wrap: break-word; -webkit-nbsp-mode: space; line-break: after-white-space;" class=""><div style="caret-color: rgb(0, 0, 0); color: rgb(0, 0, 0); font-family: Helvetica; font-size: 12px; font-style: normal; font-variant-caps: normal; font-weight: normal; letter-spacing: normal; text-align: start; text-indent: 0px; text-transform: none; white-space: normal; word-spacing: 0px; -webkit-text-stroke-width: 0px; text-decoration: none;">朗镜科技成立于2015年，是新零售时代消费品领域AI图像识别技术的领航者。致力于运用世界领先的计算机视觉技术和大数据挖掘与分析服务帮助品牌商实时获取渠道终端商品信息，实现消费决策场景可视化、数据化、实时化。辅以全国百万会员的人人终端众包业务，辐射600+城市。拥有权威的技术专家和研发团队，均来自清华、北大、复旦等高等院校和世界500强企业。经过不断的深耕与创新，已成功服务了全球上百家大型企业，覆盖快消、医药、家电、连锁等行业。<br class="">------------------<br class="">Best Regards<br class=""><br class="">姓名:仇友博<br class="">职位：iOS工程师<br class="">Cel :17600406668<br class=""><a href="mailto:qiuyoubo@lenztechretail.com" class="">E-mail:qiuyoubo@lenztechretail.com</a></div></div></div>
    </div>

    <br class="">
    """
    return mail_msg



def sendEmail(config):
    message = MIMEText(email_content(config),'html','utf-8')
    message['From'] = Header("仇友博<"+sender+">",'utf-8')
    message['To'] = Header(";".join(to_receivers),'utf-8')
    message['Cc'] = Header(";".join(copy_receivers),'utf-8')
    
    subject = '【提测申请】'+ config.project_name
    
    message['Subject'] = Header(subject,'utf-8')
    
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host,25)
        smtpObj.login(mail_user,mail_pass)
        smtpObj.sendmail(sender,receivers,message.as_string())
        print "邮件发送成功"
    except smtplib.SMTPException:
        print"Error:无法发送邮件"

#过滤 从 pr中读取的 数据
def handle_comment_msg(list):
    dict = {}
    for row in list:

        if '**提交者：袁冬冬 提交内容：' in row:
            row.replace('**提交者：袁冬冬 提交内容:','')
        elif '**提交者：袁冬冬 提交内容:' in row:
            row.replace('**提交者：袁冬冬 提交内容:','')
        elif 'jack_提交' in row:
            row.replace('jack_提交','')
        elif 'Jack_提交' in row:
            row.replace('Jack_提交','')

        if 'Merge branch' in row:
            continue
        elif 'Merge remote-tracking branch' in row:
            continue
        elif ('pod' in row or 'Pod' in row) and '同步' in row:
            continue
        elif len(row) < 5:
            continue
        try:
            value = dict[row]
        except Exception,e:
            dict[row] = '1'

        
    return dict.keys

def main(argv):
    
    requestLenz.request_config_username = p_config.config['git_user']
    requestLenz.request_config_password = p_config.config['git_pass']

    if sys.getdefaultencoding() != 'utf-8':
        reload(sys)
        sys.setdefaultencoding('utf-8')

    path=os.getcwd()

    configs_path = os.path.join(path,'configs/configs')

    print('请选择要提测的项目:')
    with io.open(configs_path,'r') as f:
        num = 0
        contents = f.readlines()
        for line in contents:
            num += 1
            print(str(num)+'.'+line)
    index = int(raw_input(''))
    project_config = contents[index-1]
    project_config = project_config.split('\n')[0]

    yamlPath = os.path.join(path,'configs/'+project_config)


    config = TemplateConfig()
    config.readConfig(yamlPath)

    
    #自动获取 开发者
    if config.project_developers == '':
        config.project_developers = getDevelopers(config.git_project_name,config.git_branch)

    if config.git_project_name == 'LenzBusiness':
        config.project_name = '朗镜通iOS ' + config.project_name
    elif config.git_project_name == 'LenzMember':
        config.project_name = '拍拍赚iOS ' + config.project_name

    
    request = LenzRequest('ppz_bj','LenzBusiness')
    msg_list,pr_url = request.getPRByAllProcesses(config.git_branch,'pr:'+config.project_name)
    config.poject_comment = ''.join(handle_comment_msg(msg_list))
    config.project_pr_diff = pr_url

    config.save(yamlPath)
    config.log()

    raw_input('如果现在需要修改请前往 %s 去修改，修改完后回到这里按任意键继续:' % (yamlPath))
    config.readConfig(yamlPath)
    config.log()

    sendEmail(config)



if __name__ == "__main__":
    main(sys.argv[1:])


"""
    print "__file__=%s" % __file__
    print "os.path.realpath(__file__)=%s" % os.path.realpath(__file__)
    print "os.path.dirname(os.path.realpath(__file__))=%s" % os.path.dirname(os.path.realpath(__file__))
    print "os.path.split(os.path.realpath(__file__))=%s" % os.path.split(os.path.realpath(__file__))[0]
    print "os.path.abspath(__file__)=%s" % os.path.abspath(__file__)
    print "os.getcwd()=%s" % os.getcwd()
    print "sys.path[0]=%s" % sys.path[0]
    print "sys.argv[0]=%s" % sys.argv[0]
"""
