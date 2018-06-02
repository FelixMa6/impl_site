from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from .models import VectorIssue,Comment,Category,DailyReport
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.views.decorators.cache import never_cache
from django.utils.translation import ugettext as _, ugettext_lazy
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from itertools import chain
import socket,datetime
import re

import sys,random,os,subprocess
from collections import OrderedDict

from django.contrib.admin import FieldListFilter
from django.contrib.admin.exceptions import (
    DisallowedModelAdminLookup, DisallowedModelAdminToField,
)
from django.contrib.admin.options import (
    IS_POPUP_VAR, TO_FIELD_VAR, IncorrectLookupParameters,
)
from django.contrib.admin.utils import (
    get_fields_from_path, lookup_needs_distinct, prepare_lookup_value, quote,
)
from django.core.exceptions import (
    FieldDoesNotExist, ImproperlyConfigured, SuspiciousOperation,
)
from django.core.paginator import InvalidPage
from django.db import models
from django.urls import reverse
from django.utils import six
from django.utils.encoding import force_text
from django.utils.http import urlencode
from django.utils.translation import ugettext

# Changelist settings
ALL_VAR = 'all'
ORDER_VAR = 'o'
ORDER_TYPE_VAR = 'ot'
PAGE_VAR = 'p'
SEARCH_VAR = 'q'
ERROR_FLAG = 'e'

IGNORED_PARAMS = (
    ALL_VAR, ORDER_VAR, ORDER_TYPE_VAR, SEARCH_VAR, IS_POPUP_VAR, TO_FIELD_VAR)



class Owner():
    def __init__(self,user,number=0):
        self.name = user.username
        self.number = number
        self.id = user.id
    def add(self):
        self.number = self.number + 1

class Info():
    def __init__(self,name,content):
        self.name = name
        self.content = content



    
def getOwners(vectors,date_create,owners):
    results = list(map(lambda a :[a.strftime('%d-%b-%Y')] + (len(owners))*[0],date_create))
    results[-1][0] = "Earlier"
    for vector in vectors:
        owner_id = vector.bugowner_id
        date_add = vector.add_time
        index = [-1,-1]
        for i in range(len(owners)):
            if owners[i].id==owner_id:
                index[1]=i+1
                break
        for i in range(len(date_create)):
            if date_create[i]<=date_add:
                index[0]=i
                break
        results[index[0]][index[1]] += 1

    return results

def get_report_info(items):
    def get_list(report):
        if report is None:
            return None
        def handle_item(item):
            attr = getattr(report,item)
            if callable(attr):
                attr = attr()
            if item == 'pass_rate':
                item = format_html('<a href={0}>{1}</a>'.format(reverse('regression:passrate'),item))
                attr = format_html('<a href={0}>{1}</a>'.format(reverse('regression:passrate'),attr))
            
            #2017-03-30 Felix : try to update item.name
            if item == 'pass_number_prj1': 
                item = 'p_prj2'
                #print('find pass_number_prj1', item)
            return Info(item,attr)
        return list(map(handle_item,items))
    return get_list

class FailType():
    def __init__(self,name,counter):
        self.name = name
        self.counter = counter
        self.color = '#' +  format(random.randint(0x100000,0xFFFFFF),'X')


def index(request):
    """
    Displays a list of User information.
    """
    vectors = VectorIssue.objects.filter(active=True)
    max_show = 13

    reports = list(DailyReport.objects.all())
    daily_temp = reports[:]
    daily_temp.reverse()
    daily_temp = daily_temp[0:max_show]
    #daily_header =  ['create_time','pass_number','fail_number','pass_rate','pass_number_prj2','fail_number_prj2','pass_rate_prj2']
    daily_header =  ['create_time','pass_number','fail_number']
    daily_reports = list(map(get_report_info(daily_header),daily_temp))

    #2017-03-30 Felix : gen chx002 project pass rate, but no pass case saved
    #last_item = DailyReport.objects.last()
    
    date_create = list(map(lambda a:a.add_time,daily_temp))


    o_resolved = User.objects.filter(id=18)
    exclude_resolved = User.objects.exclude(id=18)
    #print('o_resolved is', o_resolved)
    all_owner = chain(exclude_resolved, o_resolved)
    #print ('all_owner is ',all_owner)
    owners =  list(filter(lambda user:(user.id!=1),all_owner)) #delete admin
    owner_list = getOwners(vectors,date_create,owners)

    #delet bug item
    #start = 1
    #end = 33400
    #for i in range(start, end):
    #    need_delete = VectorIssue.objects.filter(id=i)
    #    for j in need_delete:
    #        j.bugowner = get_object_or_404(User,pk=15)#Send to Zhongmin
    #        j.save()
            #if j.bugowner != get_object_or_404(User,pk=18):
            #    print('need delete: ', j)#R1 stage result 
            #    j.delete()

    #need_delete = VectorIssue.objects.filter(bugowner='allenjin')
    #need_delete = VectorIssue.objects.filter(bugowner=get_object_or_404(User,pk=11), content__contains='XXXXXX', add_time__contains='25')
    #need_delete = VectorIssue.objects.filter(bugowner=get_object_or_404(User,pk=7), add_time__contains='Aug')
    #need_delete = VectorIssue.objects.filter(bugowner=get_object_or_404(User,pk=11), content__contains='viction exeed mementy limi')
    #need_delete = VectorIssue.objects.filter(bugowner=get_object_or_404(User,pk=7), content__contains='No ID found for delet')
    #need_delete = VectorIssue.objects.filter(bugowner=get_object_or_404(User,pk=5), content__contains='sys-afs', set_top=False) #felix
    #need_delete = VectorIssue.objects.filter(bugowner=get_object_or_404(User,pk=5), content__contains='initL2-pli-fail')
    #need_delete = VectorIssue.objects.filter(bugowner=get_object_or_404(User,pk=18))
    #need_delete = VectorIssue.objects.filter(pk=31848)
    #need_delete = VectorIssue.objects.filter(content__contains='bcL2Snoop_P with key')
    #need_delete = VectorIssue.objects.filter(content__contains='no id match for response infor', vector__contains='2017519')
    #need_delete = VectorIssue.objects.filter(content__startswith='fsbc', add_time__contains='04')
    #need_delete = VectorIssue.objects.filter(add_time__month='March')
    #print('need delete: ', need_delete)#R1 stage result 
    #for i in need_delete: i.delete()
    #for i in need_delete: 
    #    print('owner is : ', i.bugowner)#R1 stage result 
    #    i.bugowner = get_object_or_404(User,pk=18)#Send to Resolved
    #    i.bugowner = get_object_or_404(User,pk=4)#Send to SimonZhang
    #    i.bugowner = get_object_or_404(User,pk=5)#Send to Felix
    #    i.bugowner = get_object_or_404(User,pk=10)#Send to Johnny
    #    i.bugowner = get_object_or_404(User,pk=16)#Send to Grace
    #    i.bugowner = get_object_or_404(User,pk=7)#Send to Cheryl
    #    i.bugowner = get_object_or_404(User,pk=21)#Send to Phil
    #    i.bugowner = get_object_or_404(User,pk=22)#Send to Matthew
    #    i.bugowner = get_object_or_404(User,pk=1)#Send to Bert
    #    i.bugowner = get_object_or_404(User,pk=11)#Send to Rena
    #    i.bugowner = get_object_or_404(User,pk=20)#Send to Lane
    #    i.bugowner = get_object_or_404(User,pk=15)#Send to Zhongmin
    #    i.set_top = False
    #    i.save()

    
    categories = filter(lambda a: not a.isEmpty(), Category.objects.all())
    distribution = map(lambda a:FailType(a.title,a.counter),categories)
    print('categories is ', Category.objects.all())
    print('distribution is ', distribution)


    report = DailyReport.objects.last()
    transactions_name = [
            'c2m',
            'c2p',
            'p2c',
            ]
    c2p_name = [
            'io',
            'mem',
            'special',
            ]
    int_name = [
            'ipi',
            'msi',
            'sb',
            ]
    other_name = [
            #'cl0_l2_hit',
            #'cl0_l2_miss',
            #'cl1_l2_hit',
            #'cl1_l2_miss',
            #'cl0_msr_read',
            #'cl0_msr_write',
            #'cl1_msr_read',
            #'cl1_msr_write',
            #'fsbc_request',
            #'fsbc_trigger',
            'hotwire',
            'vpi_s0_s1',
            'jtag',
            ]
    s1_transactions_name = [
            'c2m_s1',
            'c2p_s1',
            'p2c_s1',
            'c2p_io_s1',
            'c2p_mem_s1',
            'c2p_special_s1',
            'interrupt_ipi_s1',
            'interrupt_msi_s1',
            'interrupt_sb_s1',
            'cl0_l2_hit_s1',
            'cl0_l2_miss_s1',
            'cl1_l2_hit_s1',
            'cl1_l2_miss_s1',
            'cl0_msr_read_s1',
            'cl0_msr_write_s1',
            'cl1_msr_read_s1',
            'cl1_msr_write_s1',
            'fsbc_request_s1',
            'fsbc_trigger_s1',
            'hotwire_s1',
            'vpi_s1_s0',
            ]

    def get_show(name):
        return  lambda item : {
            'name'    : item,
            'counter' : getattr(report,name + item),
                }
 
    get_item = get_show('')
    get_c2ps = get_show('c2p_')
    get_interrupt = get_show('interrupt_')
    transactions = list(map(get_item,transactions_name))
    c2ps = list(map(get_c2ps,c2p_name))
    ints = list(map(get_interrupt,int_name))
    others = list(map(get_item,other_name))
    s1_transactions = list(map(get_item,s1_transactions_name))
    other = report.total_request - sum(map(lambda i:i['counter'],transactions))
    transactions.append({'name':'other','counter':other})

    all = transactions_name
    #all += list(map(lambda a:'c2p_'+a,c2p_name))
    #all += list(map(lambda a:'interrupt_'+a,int_name))
    #all += other_name
    #all += s1_transactions_name



    return render(request, 'regression/index.html', {
	    'title':'Regression status',
        'owners':owners,
	    'owner_list' : owner_list,
        'daily_reports':daily_reports,
        'daily_header':daily_header,
        'distribution':distribution,
        'reports':reports[-max_show:],
         'transactions':transactions,
         'c2ps':c2ps,
         'ints':ints,
         'others':others,
         #felix's1_transactions':s1_transactions,
         'lengends': transactions_name + c2p_name + int_name + other_name,
         'daily_report':list(map(get_item,all)),


            })

def get_header(list_display):
    for item in list_display:
        yield {
            'text':item,
                }

def get_localattr(item,attr):
    if attr == 'reason':
        attr = 'get_reason_display'
    if attr == 'vector':
        id = item.id
        name = getattr(item,attr)
        myurl = '/regression/{}/vector/'.format(id)
        return format_html('<td><a href={}>{}</a></td>',myurl,name)
    a = getattr(item,attr)
    if callable(a):
        a = a()
    if a is None:
        a = '-'
    if hasattr(a,'strftime'):
        a = (a+datetime.timedelta(hours=8)).strftime(' %H:%M %d-%b')
    return format_html('<td>{}</td>',format_html(str(a).strip().replace('\n','<br>')))

def get_results(list_object,list_display):
    return map(lambda item : map(lambda a : get_localattr(item,a),list_display),list_object)

def user(request,user_id):
    #return HttpResponse('show user infomation : %s' % user_id)
    user = get_object_or_404(User,pk=user_id)
    #vectors = VectorIssue.objects.filter(active=True,bugowner_id=user_id)
    #vectors = vectors.order_by('id')
    #print('new: ',vectors)
    #inv = vectors.reverse()
    #vectors = inv
#-------------------------------------------------------------------------------------------
    vectors_no_top = VectorIssue.objects.filter(set_top=False,active=True,bugowner_id=user_id)
    vectors_no_top = vectors_no_top.order_by('id')
    vectors_no_top_inv = vectors_no_top.reverse()
    vectors_set_top = VectorIssue.objects.filter(set_top=True,active=True,bugowner_id=user_id)
    vectors_set_top = vectors_set_top.order_by('id')
    vectors_set_top_inv = vectors_set_top.reverse()

    if str(user_id) == '18': 
        vectors_for_resolved = VectorIssue.objects.filter(active=True,bugowner_id=18)
        vectors_for_resolved = vectors_for_resolved.order_by('id')
        vectors_for_resolved_inv = vectors_for_resolved.reverse()
        vectors = vectors_for_resolved_inv
        print('user is resolved, user id is', user_id)
    else : 
        vectors = chain(vectors_set_top_inv, vectors_no_top_inv)

#-------------------------------------------------------------------------------------------
    #print('inv: ',inv)
    #list_display = ['id','vector','set_top','category','project','content','reason','last_comment','add_time','modified_time'] 
    list_display = ['id','vector','modified_time','set_top','category','content','last_comment','project','reason','add_time'] 
    results = get_results(vectors,list_display)

    header = list(get_header(list_display))
    return render(request, 'regression/user.html',{
	'title':'Bugs belong to %s' % user.username,
	'owner':user,
    'result_headers':header,
    'results':results,
	})

def get_content(vector,name):
    if name=='reason':
        name='get_reason_display'
    if name=='owner':
        name='bugowner'
    attr = getattr(vector,name)
    if name=='log_path':
       attr = format_html('<a href={}>{}</a>',reverse('regression:log',args=(vector.id,)),attr)
    if name=='src_path':
       attr = format_html('<a href={}>{}</a>',reverse('regression:src',args=(vector.id,)),attr)
    if name=='wave_path':
       attr = format_html('<a href={}>{}</a>',reverse('regression:wave',args=(vector.id,)),attr)
    return attr

def new_fork(cmd,user):
    pid = os.fork()
    if pid==0:
        name = user.username
        backup = os.getenv('DISPLAY')
        print(os.getenv('DISPLAY'))
        if not os.path.exists('/haydn/{}/.dt/DISPLAY'.format(name)):
            return
        for line in open('/haydn/{}/.dt/DISPLAY'.format(name)):
            os.environ['DISPLAY']=line.strip().split(' ')[-1]
            os.system(cmd)
            break
        print(os.getenv('DISPLAY'))
        os.environ['DISPLAY']=backup
        #subprocess.getoutput('gvim &')
    else:
        print("hello from %s" % user.username)


@login_required
def logshow(request,bug_id):
    vector = get_object_or_404(VectorIssue,pk=bug_id)
    cmd = 'gvim {}&'.format(vector.log_path)
    new_fork(cmd,request.user)
    return HttpResponseRedirect(reverse('regression:vector',args=(bug_id,)))


@login_required
def srcshow(request,bug_id):
    vector = get_object_or_404(VectorIssue,pk=bug_id)
    cmd = 'gvim {}&'.format(vector.src_path)
    new_fork(cmd,request.user)
    return HttpResponseRedirect(reverse('regression:vector',args=(bug_id,)))

@login_required
def waveshow(request,bug_id):
    vector = get_object_or_404(VectorIssue,pk=bug_id)
    cmd = vector.play_fsdb()
    new_fork(cmd,request.user)
    return HttpResponseRedirect(reverse('regression:vector',args=(bug_id,)))

def get_select_option(value,show,choose):
    sel_t  = '<option value="{0}" {2}>{1}</option>'
    choose =  format_html('selected="selected"') if choose else format_html('')
    return format_html(sel_t,value,show,choose)


def get_html_content(vector,mydict):
    if mydict['name'] == "active":
        mydict['is_checkbox'] = False
        sel = [
                get_select_option(0,'In progress',True),
                get_select_option(1,'Resolved',False),
                ]
        mydict['content'] = format_html('\n'.join(sel))
        return
    if mydict['name'] == "set_top":
        mydict['is_checkbox'] = False
        sel = [
                get_select_option(0,'No',vector.set_top==False),
                get_select_option(1,'Yes',vector.set_top==True),
                ]

        mydict['content'] = format_html('\n'.join(sel))
        return
    if mydict['name'] == 'bugowner':
        users = User.objects.all()
        mydict['name'] = 'next_owner'
        users_show = map(lambda user : get_select_option(user.id,user.username,user==vector.bugowner) , users)
        mydict['content'] = format_html('\n'.join(users_show))
    if mydict['name'] == 'reason':
        reasons = VectorIssue.BUG_TYPE
        reason_show = map(lambda reason : get_select_option(reason[0],reason[1],reason[0]==vector.reason),reasons)
        mydict['content'] = format_html('\n'.join(reason_show))

        

def get_fields(vector,fieldsets):
    name_change = {
        'src_path':'vector path',
        'wave_path':'wave path',
        'log_path':'log path',
        'design_git':'design version',
        'env_git':'env version',
            }
    for line in fieldsets:
        if not line['editable']:
            for i in range(len(line['fields'])):
                name = line['fields'][i]
                content = get_content(vector,name)
                if name in name_change.keys():
                    name = name_change[name]
                line['fields'][i] = {
                    'content':content,
                    'name':name,
                        }
        else:
            for i in range(len(line['fields'])):
                name = line['fields'][i]
                mydict = {
                    'name':name,
                        }
                get_html_content(vector,mydict)
                line['fields'][i] = mydict
                
def mail_info(vector):
    vector_path = 'http://' + socket.gethostname() + ":15600" + reverse('regression:vector',args=(vector.id,))
    subject = "[vector %d] %s" % (vector.id,vector.vector)
    last_comment = vector.comment_set.last()
    message = """
        <html>
        <head>the latest comment about vector{id}</head>
        <body>
            <table border="1" cellspacing="0" cellpadding="8">
            <tr><td><TH align=right>FAIL:</td><td>{fail}</td></tr>
            <tr><td><TH align=right>author:</td><td>{author}</td></tr>
            <tr><td><TH align=right>content:</td><td>{content}</td></tr>
            <tr><td><TH align=right>path:</td><td>{path}</td></tr>
            </table>
            <p>You have participated in this bug comments</p>
        </body>
        </html>
    """.format(author=last_comment.Assignee,id=vector.id,content=last_comment.content,path=vector_path,fail=vector.content)
    tos = list(set(map(lambda a:a.Assignee.email,vector.comment_set.all()))|{vector.bugowner.email})
    msg = EmailMessage(subject,message,'marshallliu@zhaoxin.com',tos)
    msg.content_subtype='html'
    msg.send()


def vector(request,bug_id):
    #return HttpResponse('show bug infomation')
    vector = get_object_or_404(VectorIssue,pk=bug_id)
    update = False
    owner_id = vector.bugowner_id

    if 'next_owner' in request.POST:
        bugowner = get_object_or_404(User,pk=request.POST['next_owner'])
        if not bugowner.id == vector.bugowner_id:
            vector.bugowner = bugowner
            update = True

    if 'reason' in request.POST:
        new_reason = request.POST['reason']
        if not new_reason == vector.reason:
            vector.reason = new_reason
            update = True

    if 'active' in request.POST and request.POST['active']=='1':
        #vector.active = False
        bugowner = get_object_or_404(User,pk=18)#Send to Resolved
        vector.bugowner = bugowner
        vector.set_top = False
        update = True

    if 'set_top' in request.POST:
        v = request.POST['set_top']
        #print('-----------------set top is ', v)
        if not v == vector.set_top:
            vector.set_top = v
            #print('-----------------set top to ', vector.set_top)
        #vector.set_top = True
        update = True

    if 'content' in request.POST:
        content = request.POST['content'].strip()
        if not content == "":
            if(re.search('{.*}', content) is not None):
                raise Exception('illegal comment witch "{...}"')
            else:
                author = get_object_or_404(User,pk=request.POST['author'])
                vector.comment_set.create(Assignee=author,content=content)
                update = True

    if 'reason' in request.POST and not update:
        raise Exception('illegal request')


    if update:
        vector.save()
        #mail_info(vector)
        update = False
        return HttpResponseRedirect(reverse('regression:user',args=(owner_id,))) 

    users = User.objects.all()

    fieldsets = [
            #{'name':'BUG INFO', 'editable' : False,  'fields':['vector','content','src_path','wave_path','log_path','play_fsdb','design_git','design_git_date','env_git','env_git_date','owner','reason']},
            {'name':'BUG INFO', 'editable' : False,  'fields':['vector','content','src_path','wave_path','log_path','design_git','design_git_date','env_git','env_git_date','owner','reason']},
	    ]

    actionsets = [
            {
                'name':'BUG FORWARD',
                'editable':True,
                'fields':['bugowner','active','reason','set_top',],
                }
            ]

    get_fields(vector,fieldsets)
    get_fields(vector,actionsets)


    return render(request, 'regression/vector.html',{
	'title':'Vector ID %d' % vector.id,
	'vector':vector,
    'vrg_form':fieldsets,
    'action_form':actionsets,
    'users':users
	})

@never_cache
def login(request,extra_context=None):
    from django.contrib.auth.views import LoginView
    # Since this module gets imported in the application's root package,
    # it cannot import models from other applications at the module level,
    # and django.contrib.admin.forms eventually imports User.
    from django.contrib.admin.forms import AdminAuthenticationForm
    context = dict(
            title=_('Log in'),
            username=request.user.get_username(),
        )

    context[REDIRECT_FIELD_NAME] = reverse('regression:index')
    context.update(extra_context or {})

    defaults = {
            'extra_context': context,
            'authentication_form': AdminAuthenticationForm,
            'template_name': 'regression/login.html',
    }
    return LoginView.as_view(**defaults)(request)

@never_cache
def logout(request,extra_context=None):
    from django.contrib.auth.views import LogoutView
    context = dict()
    context.update(extra_context or {})
    defaults = {
            'extra_context': dict(
                # Since the user isn't logged out at this point, the value of
                # has_permission must be overridden.
                has_permission=False,
                **(context)
            ),
            'next_page' : reverse('regression:index'),
        }
    return LogoutView.as_view(**defaults)(request)

def password_change(request, extra_context=None):
    """
    Handles the "change password" task -- both form display and validation.
    """
    from django.contrib.admin.forms import AdminPasswordChangeForm
    from django.contrib.auth.views import password_change
    url = reverse('regression:password_change_done')
    defaults = {
        'password_change_form': AdminPasswordChangeForm,
        'post_change_redirect': url,
        'extra_context': dict(**(extra_context or {})),
    }
    defaults['template_name'] = 'regression/change_password.html'
    return password_change(request, **defaults)

def password_change_done(request, extra_context=None):
    """
    Displays the "success" page after a password change.
    """
    from django.contrib.auth.views import password_change_done
    defaults = {
        'extra_context': dict( **(extra_context or {})),
    }
    defaults['template_name'] = 'regression/change_password_done.html'
    return password_change_done(request, **defaults)

def report(request):
    #return HttpResponse('show more report infomation')
    report = DailyReport.objects.last()
    transactions_name = [
            'c2m',
            'c2p',
            'p2c',
            ]
    c2p_name = [
            'io',
            'mem',
            'special',
            ]
    int_name = [
            'ipi',
            'msi',
            'sb',
            ]
    other_name = [
            'jtag',
            'hotwire',
            ]

    def get_show(name):
        return  lambda item : {
            'name'    : item,
            'counter' : getattr(report,name + item),
                }
 
    get_item = get_show('')
    get_c2ps = get_show('c2p_')
    get_interrupt = get_show('interrupt_')
    transactions = list(map(get_item,transactions_name))
    c2ps = list(map(get_c2ps,c2p_name))
    ints = list(map(get_interrupt,int_name))
    others = list(map(get_item,other_name))
    other = report.total_request - sum(map(lambda i:i['counter'],transactions))
    transactions.append({'name':'other','counter':other})

    all = transactions_name
    all += list(map(lambda a:'c2p_'+a,c2p_name))
    all += list(map(lambda a:'interrupt_'+a,int_name))
    all += other_name



    return render(request, 'regression/report.html',{
	'title':'Report Show' ,
    'transactions':transactions,
    'c2ps':c2ps,
    'ints':ints,
    'others':others,
    'lengends': transactions_name + c2p_name + int_name + other_name,
    'daily_report':list(map(get_item,all)),
	})


def passrate(request):
    reports = DailyReport.objects.all()
    return render(request,'regression/passrate.html',{
        'title':'Recent Pass Rate',
        'reports':reports,
        })





# Create your views here.
