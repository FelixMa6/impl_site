#+!/usr/local/bin/python3
import os
import sys,re
import socket
os.chdir(sys.path[0])
os.environ.setdefault("DJANGO_SETTINGS_MODULE","impl_site.settings")
import django
django.setup()

from configparser import ConfigParser
from socketserver import BaseRequestHandler,ThreadingTCPServer
from release_check.models import OwnerCase, BaseItem
from release_check.models import unit, case
from signoff_check.models import TOwnerCase, TBaseItem, TPathGroup, TCheckCase
from regression.models import VectorIssue,Category,DailyReport
from django.contrib.auth.models import User
from queue import Queue
#import logger
from django.core.mail import EmailMessage
import socket
from django.urls import reverse
from itertools import chain

#-----------------------------------------------------------------------------------------
#send mail
def mail_create(vector):
    vector_path = socket.gethostname() + ":17500" + reverse('regression:vector',args=(vector.id,))
    subject = "[vector %d] %s" % (vector.id,vector.vector)
    message = """
        <html>
        <head>hi {name} ! You have got a new bug{id}</head>
        <body>
            <table border="1" cellspacing="0" cellpadding="8">
            <tr><td><TH align=right>category:</td><td>{category}</td></tr>
            <tr><td><TH align=right>content:</td><td>{content}</td></tr>
            </table>
            <p>Please login Deephi IC web for more details</p>
        </body>
        </html>
    """.format(id=vector.id,name=vector.bugowner,content=vector.content,category=vector.category)
    tos = list(set([vector.bugowner.email,'@.com']))
    msg = EmailMessage(subject,message,'zhongminchen@.com',tos)
    msg.content_subtype='html'
    msg.send()

def add_basic(cfg):
    basic = OwnerCase()
    basic.project = cfg.get('design','project')
    basic.check_item = cfg.get('design','check_item')
    basic.partition = cfg.get('design','partition')
    basic.fail_total_number = cfg.get('design','fail_total_number')
    basic.design_git_number = cfg.get('design','design_git_number')
    basic.design_git_date = cfg.get('design','design_git_date')
    basic.summit_time = cfg.get('design','summit_time')
    basic.fail_owner_count= cfg.get('design','fail_owner_count')
    print('base fail_owner_count is:', basic.fail_owner_count)
    return basic

def add_case(cfg,cfg_file):
    print('add case flag')
    total_case = []
    i = 0
    while True:
        i = i + 1
        try:
            new_case = add_basic(cfg)
            print('fail_owner_count is:', new_case.fail_owner_count)
            print('debug flag after new case:')
            print('owner 1 is:', cfg.get('owner','1'))

            if str(new_case.fail_owner_count) == "0":
                print('debug flag judge:')
                new_case.owner = 'null'
                new_case.fail_number = 0
                new_case.log_path = 'null'
                new_case.save()
                total_case.append(str(new_case))
                return total_case
                break
            else:
                case_item = cfg.get('owner',str(i))
                print('case item is:', case_item)
                print('debug flag after get:')
                item_list = case_item.split(', ')
                print('item list is:', item_list)
                new_case.owner = item_list[0]
                new_case.fail_number = item_list[1]
                if new_case.check_item == "check_lint":
                    new_case.warn_number = item_list[2]
                    new_case.info_number = item_list[3]
                    new_case.log_path = item_list[4]
                else:
                    new_case.log_path = item_list[2]
                new_case.save()
                total_case.append(str(new_case))
        except:
            print('invalid key:', i)
            break

    return total_case
#-----------------------------------------------------------------------------------------
def add_signoff_basic(cfg,i,type):
    #basic = OwnerCase(pk=i)
    if type == 'owner':
        basic = TOwnerCase()
        #print('debug info: add new TOwnerCase')
    elif type == 'path_group':
        basic = TPathGroup()
    else:
        basic = TCheckCase()
        #print('debug info: add new TPathGroup')

    basic.project = cfg.get('design','project')
    basic.stage = cfg.get('design','stage')
    basic.check_item = cfg.get('design','check_item')
    basic.partition = cfg.get('design','partition')
    basic.corner = cfg.get('design','corner')
    basic.signoff_mode = cfg.get('design','signoff_mode')
    basic.check_mode = cfg.get('design','check_mode')
    basic.database_version = cfg.get('design','database_version')
    basic.summit_time = cfg.get('design','summit_time')

    basic.vio_total_number  = '1'
    basic.database_date = '1'

    print('debug info: corner is ', basic.corner)
    if type != 'check':
        try: 
            basic.setup_wns = cfg.get('summary','setup_wns')
            basic.setup_tns = cfg.get('summary','setup_tns')
            basic.setup_nvp = cfg.get('summary','setup_nvp')
        except:
            basic.setup_wns = '0' 
            basic.setup_tns = '0' 
            basic.setup_nvp = '0' 

        try: 
            basic.hold_wns  = cfg.get('summary','hold_wns')
            basic.hold_tns  = cfg.get('summary','hold_tns')
            basic.hold_nvp  = cfg.get('summary','hold_nvp')
        except:
            basic.hold_wns  = '0' 
            basic.hold_tns  = '0' 
            basic.hold_nvp  = '0' 

    try: basic.fn = cfg.get('design','fn')
    except: basic.fn = '-'

    return basic
#--------------------------------------------------------------------------------
def add_signoff_case(cfg,case,type,stage_value):
    total_case = []
    i = 0
    while True:
        i = i + 1
        print('debug add_signoff_path_group info: loop ',i)
        try:
            #process owner case
            new_case = add_signoff_basic(cfg,i,case)
        #print('debug info: add new TPathGroup')

            case_item = cfg.get(case+'_'+type,str(i))  

            list = case_item.split(", ")
        #print('debug add_signoff_path_group info:',list[0])
            if(case == 'path_group'):
                new_case.group= list[0]
            elif(case == 'owner'):
                new_case.owner= list[0]
            new_case.wns= list[1]
            new_case.tns= list[2]
            new_case.nvp= list[3]
            #if new_case.partition == 'core_only':
            new_case.log_path= list[4]
        #print('debug add_signoff_path_group info: log path is ',new_case.log_path)
            new_case.type  = type
            new_case.stage  = stage_value
            #new_case.nvp= list[3]
            #new_case.freq= list[4]
            #new_case.wns_h= list[5]
            #new_case.tns_h= list[6]
            #new_case.nvp_h= list[7]
            new_case.save()
            total_case.append(str(new_case))
        except:
            print('invalid key:', i)
            if i==1:
                new_case.group= 'null'
                new_case.wns= 'null'
                new_case.tns= 'null'
                new_case.nvp= 'null'
                new_case.log_path= 'null'
                new_case.type  = type
                new_case.stage  = stage_value
                new_case.save()
                total_case.append(str(new_case))
            break

    return total_case

#-----------------------------------------------------------------------------------------
#for submit regression result

def saveCategory(type):
    admin = User.objects.get(username='felix')
    #l2_sva_fail = re.compile("l2-sva-fail")
    #if l2_sva_fail.search(type) is not None:
    #    type = 'l2-sva-fail'
    if Category.objects.filter(title=type) :
        category = Category.objects.filter(title=type)[0]
    else:
        category = Category(title=type,owner=admin)
    category.save(flag=True)
    return category

def add_fail(cfg):
    status = cfg.get('vector','status')
    if status != 'FAIL':
        return None
    name = cfg.get('vector','name')
    content = cfg.get('fail','info')
    issue = VectorIssue(vector=name,content=content)

    issue.project = cfg.get('vector','project')

    issue.src_path  = cfg.get('path','vector')
    issue.wave_path = cfg.get('path','waveform')
    issue.log_path  = cfg.get('path','log')
    issue.set_top = False

    issue.design_git      = cfg.get('git','design_version')
    issue.env_git         = cfg.get('git','env_version')
    issue.design_git_date = cfg.get('git','design_date')
    issue.env_git_date    = cfg.get('git','env_date')

    type = cfg.get('fail','type')
    issue.category = saveCategory(type)
    owner = issue.category.owner
    issue.bugowner = owner

    issue.save()
    #mail_create(issue)
    return issue


def add_report(cfg,cfg_file):
    report = DailyReport.objects.last()
    if report is None:
        report = DailyReport()
    elif not report.is_same_work_day():
        report = DailyReport()

    status = cfg.get('vector','status')
    project = cfg.get('vector','project')
    name = cfg.get('vector','name')
    print ('name is ', name)
    if status == 'FAIL':
        report.add_fail()
        #if re.search('CHX002_A0', project): report.add_fail_prj1()
        #if(project == 'CHX002_A0'): report.add_fail_prj1()
        #if(project == 'CHX002_A0_PVRG'): report.add_fail_prj1()
    else:
        #if(cfg.getint('transactions','total_request')==0):
        if cfg.getint('transactions','total_request')==0 and not re.search('top', name):
            raise Exception("pass vector total request cannot be 0 : %s" % cfg_file)
        report.add_pass()
        #if re.search('CHX002_A0', project): report.add_pass_prj1()
        #if(project == 'CHX002_A0'): report.add_pass_prj1()
        #if(project == 'CHX002_A0_PVRG'): report.add_pass_prj1()


    items = [
            'total_request',
            'c2m',
            'c2p',
            'p2c',
            ]
    for item in items:
        sum = getattr(report,item) + cfg.getint('transactions',item)
        setattr(report,item,sum)

    report.save()
    return report

#-----------------------------------------------------------------------------------------
def add_selfdefine_basic(cfg):
    basic = case()
    basic.project = cfg.get('design','project')
    basic.check_item = cfg.get('design','check_item')
    basic.partition = cfg.get('design','partition')
    basic.fail_total_number = cfg.get('design','fail_total_number')
    basic.design_git_number = cfg.get('design','design_git_number')
    basic.design_git_date = cfg.get('design','design_git_date')
    basic.summit_time = cfg.get('design','summit_time')
    basic.fail_owner_count= cfg.get('design','fail_owner_count')
    print('base fail_owner_count is:', basic.fail_owner_count)
    return basic

	
#-----------------------------------------------------------------------------------------
def add_selfdefine_case(cfg):
    total_case = []
    case_num = cfg.get('table','case_num')
    attr = cfg.get('table','attr')
    attr_list = attr.split(', ')
    print('flag for unit case')

    i = 0
    while(i<=int(case_num) - 1):
        i= i + 1
        try:
            new_case = add_selfdefine_basic(cfg)
            new_case.table_title = cfg.get('table','table_title')
            new_case.case_type = cfg.get('table','case_type')
            new_case.column_num = cfg.get('table','column_num')

            case_item = cfg.get('table',str(i))
            item_list = case_item.split(', ')
            print('item list is:', item_list)
			
            j = 1

            for a in attr_list:
                if attr_list[j-1] == 'link': link_id = j
                if j == 1: new_case.c1_key = attr_list[j-1]
                if j == 2: new_case.c2_key = attr_list[j-1]
                if j == 3: new_case.c3_key = attr_list[j-1]
                if j == 4: new_case.c4_key = attr_list[j-1]
                if j == 5: new_case.c5_key = attr_list[j-1]
                if j == 6: new_case.c6_key = attr_list[j-1]
                j = j + 1

            k = 1

            for b in item_list:
                if k == 1: new_case.c1_val = item_list[k-1]
                if k == 2: new_case.c2_val = item_list[k-1]
                if k == 3: new_case.c3_val = item_list[k-1]
                if k == 4: new_case.c4_val = item_list[k-1]
                if k == 5: new_case.c5_val = item_list[k-1]
                if k == link_id: new_case.link = item_list[k-1]
                k = k + 1

            new_case.save()
            total_case.append(str(new_case))
        except:
            print('Erro: encounter exception when create self define table')

    return total_case


#-----------------------------------------------------------------------------------------
def add_selfdefine_table1_case(cfg):
    total_case = []
    case_num = cfg.get('table_1','case_num')
    attr = cfg.get('table_1','attr')
    attr_list = attr.split(', ')
    print('flag for unit case')

    i = 0
    while(i<=int(case_num) - 1):
        i= i + 1
        try:
            new_case = add_selfdefine_basic(cfg)
            new_case.table_title = cfg.get('table_1','table_title')
            new_case.table_order= cfg.get('table_1','table_order')
            new_case.case_type = cfg.get('table_1','case_type')
            new_case.column_num = cfg.get('table_1','column_num')

            case_item = cfg.get('table_1',str(i))
            item_list = case_item.split(', ')
            print('item list is:', item_list)
			
            j = 1

            for a in attr_list:
                if attr_list[j-1] == 'link': link_id = j
                if j == 1: new_case.c1_key = attr_list[j-1]
                if j == 2: new_case.c2_key = attr_list[j-1]
                if j == 3: new_case.c3_key = attr_list[j-1]
                if j == 4: new_case.c4_key = attr_list[j-1]
                if j == 5: new_case.c5_key = attr_list[j-1]
                if j == 6: new_case.c6_key = attr_list[j-1]
                j = j + 1

            k = 1

            for b in item_list:
                if k == 1: new_case.c1_val = item_list[k-1]
                if k == 2: new_case.c2_val = item_list[k-1]
                if k == 3: new_case.c3_val = item_list[k-1]
                if k == 4: new_case.c4_val = item_list[k-1]
                if k == 5: new_case.c5_val = item_list[k-1]
                if k == link_id: new_case.link = item_list[k-1]
                k = k + 1

            new_case.save()
            print ('add table 1 new case',new_case)
            total_case.append(str(new_case))
        except:
            print('Erro: encounter exception when create self define table')

    return total_case


#-----------------------------------------------------------------------------------------
def add_selfdefine_table2_case(cfg):
    total_case = []
    case_num = cfg.get('table_2','case_num')
    attr = cfg.get('table_2','attr')
    attr_list = attr.split(', ')
    print('flag for unit case')

    i = 0
    while(i<=int(case_num) - 1):
        i= i + 1
        try:
            new_case = add_selfdefine_basic(cfg)
            new_case.table_title = cfg.get('table_2','table_title')
            new_case.table_order= cfg.get('table_2','table_order')
            new_case.case_type = cfg.get('table_2','case_type')
            new_case.column_num = cfg.get('table_2','column_num')

            case_item = cfg.get('table_2',str(i))
            item_list = case_item.split(', ')
            print('item list is:', item_list)
			
            j = 1

            for a in attr_list:
                if attr_list[j-1] == 'link': link_id = j
                if j == 1: new_case.c1_key = attr_list[j-1]
                if j == 2: new_case.c2_key = attr_list[j-1]
                if j == 3: new_case.c3_key = attr_list[j-1]
                if j == 4: new_case.c4_key = attr_list[j-1]
                if j == 5: new_case.c5_key = attr_list[j-1]
                if j == 6: new_case.c6_key = attr_list[j-1]
                j = j + 1

            k = 1

            for b in item_list:
                if k == 1: new_case.c1_val = item_list[k-1]
                if k == 2: new_case.c2_val = item_list[k-1]
                if k == 3: new_case.c3_val = item_list[k-1]
                if k == 4: new_case.c4_val = item_list[k-1]
                if k == 5: new_case.c5_val = item_list[k-1]
                if k == link_id: new_case.link = item_list[k-1]
                k = k + 1

            new_case.save()
            total_case.append(str(new_case))
        except:
            print('Erro: encounter exception when create self define table')

    return total_case


#-----------------------------------------------------------------------------------------
def add_selfdefine_table3_case(cfg):
    total_case = []
    case_num = cfg.get('table_3','case_num')
    attr = cfg.get('table_3','attr')
    attr_list = attr.split(', ')
    print('flag for unit case')

    i = 0
    while(i<=int(case_num) - 1):
        i= i + 1
        try:
            new_case = add_selfdefine_basic(cfg)
            new_case.table_title = cfg.get('table_3','table_title')
            new_case.table_order= cfg.get('table_3','table_order')
            new_case.case_type = cfg.get('table_3','case_type')
            new_case.column_num = cfg.get('table_3','column_num')

            case_item = cfg.get('table_3',str(i))
            item_list = case_item.split(', ')
            print('item list is:', item_list)
			
            j = 1

            for a in attr_list:
                if attr_list[j-1] == 'link': link_id = j
                if j == 1: new_case.c1_key = attr_list[j-1]
                if j == 2: new_case.c2_key = attr_list[j-1]
                if j == 3: new_case.c3_key = attr_list[j-1]
                if j == 4: new_case.c4_key = attr_list[j-1]
                if j == 5: new_case.c5_key = attr_list[j-1]
                if j == 6: new_case.c6_key = attr_list[j-1]
                j = j + 1

            k = 1

            for b in item_list:
                if k == 1: new_case.c1_val = item_list[k-1]
                if k == 2: new_case.c2_val = item_list[k-1]
                if k == 3: new_case.c3_val = item_list[k-1]
                if k == 4: new_case.c4_val = item_list[k-1]
                if k == 5: new_case.c5_val = item_list[k-1]
                if k == link_id: new_case.link = item_list[k-1]
                k = k + 1

            new_case.save()
            total_case.append(str(new_case))
        except:
            print('Erro: encounter exception when create self define table')

    return total_case


#-----------------------------------------------------------------------------------------
def add_selfdefine_table4_case(cfg):
    total_case = []
    case_num = cfg.get('table_4','case_num')
    attr = cfg.get('table_4','attr')
    attr_list = attr.split(', ')
    print('flag for unit case')

    i = 0
    while(i<=int(case_num) - 1):
        i= i + 1
        try:
            new_case = add_selfdefine_basic(cfg)
            new_case.table_title = cfg.get('table_4','table_title')
            new_case.table_order= cfg.get('table_4','table_order')
            new_case.case_type = cfg.get('table_4','case_type')
            new_case.column_num = cfg.get('table_4','column_num')

            case_item = cfg.get('table_4',str(i))
            item_list = case_item.split(', ')
            print('item list is:', item_list)
			
            j = 1

            for a in attr_list:
                if attr_list[j-1] == 'link': link_id = j
                if j == 1: new_case.c1_key = attr_list[j-1]
                if j == 2: new_case.c2_key = attr_list[j-1]
                if j == 3: new_case.c3_key = attr_list[j-1]
                if j == 4: new_case.c4_key = attr_list[j-1]
                if j == 5: new_case.c5_key = attr_list[j-1]
                if j == 6: new_case.c6_key = attr_list[j-1]
                j = j + 1

            k = 1

            for b in item_list:
                if k == 1: new_case.c1_val = item_list[k-1]
                if k == 2: new_case.c2_val = item_list[k-1]
                if k == 3: new_case.c3_val = item_list[k-1]
                if k == 4: new_case.c4_val = item_list[k-1]
                if k == 5: new_case.c5_val = item_list[k-1]
                if k == link_id: new_case.link = item_list[k-1]
                k = k + 1

            new_case.save()
            total_case.append(str(new_case))
        except:
            print('Erro: encounter exception when create self define table')

    return total_case


#-----------------------------------------------------------------------------------------
def cfg_info(cfg_file):
    cfg = ConfigParser()
    cfg.read(cfg_file)

    print ('in cfg_info flag')
    try:
        if cfg.get('vector','status'):
            vector_flag = 1
    except: 
        vector_flag = 0

    try:
        if cfg.get('table_1','case_type'):
            table_flag = 1
    except: 
        table_flag = 0

    if vector_flag:
#delete the old same name
        vec_delete = VectorIssue.objects.filter(vector=cfg.get('vector','name'))
        vec_delete.delete()
#
        fail = add_fail(cfg)
        report = add_report(cfg,cfg_file)
        output = []
        if fail is not None:
            output.append(str(fail))
        output.append(str(report))
        print ('output is ', output)
        return "\n".join(output)                


    if table_flag:
        print ('in table flag')
        #vec_delete = case.objects.filter(case_type=cfg.get('table_1','case_type'))
        case_delete = case.objects.all()
        case_delete.delete()

        output = []
        table_1 = add_selfdefine_table1_case(cfg)
        if table_1 is not None: output.append(str(table_1))
        table_2 = add_selfdefine_table2_case(cfg)
        if table_2 is not None: output.append(str(table_2))
        table_3 = add_selfdefine_table2_case(cfg)
        if table_3 is not None: output.append(str(table_3))
        table_4 = add_selfdefine_table2_case(cfg)
        if table_4 is not None: output.append(str(table_4))
        print ('output is ', output)
        return "\n".join(output)                

    try: check_item_value = cfg.get('design','check_item')
    except: check_item_value = 'check_lint'
    try: partition_value = cfg.get('design','partition')
    except: partition_value = 'processor'
    try: stage_value = cfg.get('design','stage')
    except: stage_value = 'FSO'
    try: corner_value = cfg.get('design','corner')
    except: corner_value = 'typical'
    try: signoff_mode_value = cfg.get('design','signoff_mode')
    except: signoff_mode_value = 'normal'
    try: check_mode_value = cfg.get('design','check_mode')
    except: check_mode_value = 'setup'

    if(check_item_value == 'signoff_timing'):
        #delete old ownercase and pathgroup
        need_delete_owner = TOwnerCase.objects.filter(check_item=check_item_value, partition=partition_value, corner=corner_value, stage=stage_value, check_mode=check_mode_value, signoff_mode=signoff_mode_value)
        need_delete_owner.delete()
        print ('need_delete_owner is ', need_delete_owner)
        need_delete_path_group = TPathGroup.objects.filter(check_item=check_item_value, partition=partition_value, corner=corner_value, stage=stage_value, check_mode=check_mode_value, signoff_mode=signoff_mode_value)
        #print ('check_item='+check_item_value +'partition='+partition_value+'corner='+corner_value+'stage='+stage_value+ 'check_mode='+check_mode_value+ 'signoff_mode='+signoff_mode_value)
        print ('need_delete_path_group is ', need_delete_path_group)
        need_delete_path_group.delete()
        sf_owner_setup = add_signoff_case(cfg,'owner','setup',stage_value)
        sf_owner_hold = add_signoff_case(cfg,'owner','hold',stage_value)
        #print ('got sf owner case', sf_owner)
        #print('type is', type(sf_owner))
        sf_path_setup = add_signoff_case(cfg,'path_group','setup',stage_value)
        sf_path_hold  = add_signoff_case(cfg,'path_group','hold',stage_value)
        #print ('got sf path case', sf_path_setup)
        #print('type is', type(sf_path_setup))
        #sf_check = add_signoff_check_case(cfg,cfg_file,stage_value)
        #output = "\n".join(sf_owner)
        sf_owner_setup.extend(sf_owner_hold)
        sf_owner_setup.extend(sf_path_setup)
        sf_owner_setup.extend(sf_path_hold)
        output = sf_owner_setup
        #print('add info: got added case', output)
        #print('type is', type(output))
    else:
        need_delete = OwnerCase.objects.filter(check_item=check_item_value, partition=partition_value)
        need_delete.delete()
        output = add_case(cfg,cfg_file)

    return "\n".join(output)

#-----------------------------------------------------------------------------------------

class InfoHandler(BaseRequestHandler):
    def handle(self):
        print('Got connection from', self.client_address)
        while(True):
            msg = self.request.recv(8192)
            if not msg:
                break
            cfg_file = str(msg,encoding='utf8')
            if not os.path.exists(cfg_file):
                error = "db-add-fail: No such ini file: %s" % cfg_file
                #logger.log_info(error)
                self.request.send(bytes(error,encoding="utf8"))
                print(error)
                continue
            try:
                #print('debug flag before output:')
                output = bytes(cfg_info(cfg_file),encoding="utf8")
                #print('debug flag after output:')
                self.request.send(output)
                #logger.log_info("success add %s" % cfg_file)
            except Exception as e:
                error = "db-add-fail Ex: " + str(e)
                print(error)
                #logger.log_info(error)
                #logger.log_debug(cfg_file)
                self.request.send(bytes(error,encoding="utf8"))
			

if __name__ == '__main__':
    serv = ThreadingTCPServer(('',17500), InfoHandler)
    serv.serve_forever()


