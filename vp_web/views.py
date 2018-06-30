from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.cache import never_cache
from django.utils.translation import ugettext as _, ugettext_lazy
from django.contrib.auth.models import User
from django.contrib.auth import REDIRECT_FIELD_NAME
from .models import CComponent,CFeature,CVerification
from django.shortcuts import render,get_object_or_404
from django.utils.html import format_html
import socket,datetime
from django.contrib.auth.decorators import login_required
import re
from django.db.models import Q
from itertools import chain
from django.forms.models import model_to_dict
import os

def index(request):

    #return HttpResponse('hello tracking')
    #common_components = CComponent.objects.filter(name__contains='special')
    #common_components = CComponent.objects.exclude(pk=437)
    #special_components = CComponent.objects.filter(pk=437)
    common_components = ''
    special_components = ''
    all_components = CComponent.objects.all()
    #print('felix debug-------------------')
    #all_components = model_to_dict(all_components)
    #print('all components is ', all_components)

    com_status = []

    for com in all_components:
        #print('com is ', com)
        all_task = 0
        finished_task = 0
        finished_status = 0

        f = com.cfeature_set.filter(component=com)
        #print('feature type is: ', f)
        features = CVerification.objects.filter(pk=0)
        #print('feature point is: ', features)
    
        all_points = CVerification.objects.filter(pk=0)
        for i in f:
            a = CVerification.objects.filter(feature=i)
            all_points = chain(all_points, a)
        #print('feature point is: ', all_points)

        #got task finished status
        for i in all_points:
            #print('current owner is : ', owner)

            #print('current point is : ', i.name)
            all_task = all_task + 4
            if i.feature_status == CFeature.STATUS[-1][0] or i.feature_status == CFeature.STATUS[-2][0]: finished_task = finished_task + 1
            if i.coverage_status == CFeature.STATUS[-1][0] or i.coverage_status == CFeature.STATUS[-2][0]: finished_task = finished_task + 1
            if i.stimulus_status == CFeature.STATUS[-1][0] or i.stimulus_status == CFeature.STATUS[-2][0]: finished_task = finished_task + 1
            if i.check_way_status == CFeature.STATUS[-1][0] or i.check_way_status == CFeature.STATUS[-2][0]: finished_task = finished_task + 1

            if all_task != 0:
                finished_status = round(finished_task*100/all_task)
            else:
                finished_status = 0
            finished_status = str(finished_status)+ '%'
            #print(owner, 'finished status is ', finished_task, '/', all_task, finished_status)
        #------------------------------------------------------------------------------------
        element = {'component':str(com.name), 'pk':str(com.pk), 'owner':str(com.owner),'owner_id':str(com.owner.id),'all_task':all_task, 'finished_task':finished_task, 'finished_status':finished_status}
        com_status.append(element)

    #print(com_status)

    com_status_header = ['component','all_task','finished_task','finished_status','']

    return render(request,'vp_web/index.html',{
        #'title':'verfication tracking',
        'components':CComponent.objects.all(),
        'com_status':com_status,
        'com_status_header':com_status_header,
        #'components':common_components,
        #'special_components':special_components,
        })
def index_status(request, pk):

    #return HttpResponse('hello tracking')
    #common_components = CComponent.objects.filter(name__contains='special')
    #common_components = CComponent.objects.exclude(pk=437)
    #special_components = CComponent.objects.filter(pk=437)
    common_components = ''
    special_components = ''
    all_components = CComponent.objects.all()
    #print('felix debug-------------------')
    #all_components = model_to_dict(all_components)
    #print('all components is ', all_components)

    com_status = []

    for com in all_components:
        #print('com is ', com)
        all_task = 0
        finished_task = 0
        finished_status = 0

        f = com.cfeature_set.filter(component=com)
        #print('feature type is: ', f)
        features = CVerification.objects.filter(pk=0)
        #print('feature point is: ', features)
    
        all_points = CVerification.objects.filter(pk=0)
        for i in f:
            a = CVerification.objects.filter(feature=i)
            all_points = chain(all_points, a)
        #print('feature point is: ', all_points)

        #got task finished status
        for i in all_points:
            #print('current owner is : ', owner)

            #print('current point is : ', i.name)
            all_task = all_task + 4
            if i.feature_status == CFeature.STATUS[-1][0] or i.feature_status == CFeature.STATUS[-2][0]: finished_task = finished_task + 1
            if i.coverage_status == CFeature.STATUS[-1][0] or i.coverage_status == CFeature.STATUS[-2][0]: finished_task = finished_task + 1
            if i.stimulus_status == CFeature.STATUS[-1][0] or i.stimulus_status == CFeature.STATUS[-2][0]: finished_task = finished_task + 1
            if i.check_way_status == CFeature.STATUS[-1][0] or i.check_way_status == CFeature.STATUS[-2][0]: finished_task = finished_task + 1

            if all_task != 0:
                finished_status = round(finished_task*100/all_task)
            else:
                finished_status = 0
            finished_status = str(finished_status)+ '%'
            #print(owner, 'finished status is ', finished_task, '/', all_task, finished_status)
        #------------------------------------------------------------------------------------
        element = {'component':str(com.name), 'pk':str(com.pk), 'owner':str(com.owner),'owner_id':str(com.owner.id),'all_task':all_task, 'finished_task':finished_task, 'finished_status':finished_status}
        com_status.append(element)

    #print(com_status)

    com_status_header = ['component','all_task','finished_task','finished_status','']
        #------------------------------------------------------------------------------------
    user = get_object_or_404(User,pk=pk)
    #features = CFeature.objects.filter(owner=user)
    features = CVerification.objects.filter(owner=user)
    coverage = CVerification.objects.filter(coverage_owner=user)
    stimuluses = CVerification.objects.filter(stimulus_owner=user)
    check_ways = CVerification.objects.filter(check_way_owner=user)

    #not_ready = lambda item:item.feature_status!=CFeature.STATUS[-1][0] and item.feature_status!=CFeature.STATUS[-2][0]
    not_ready = lambda item:item.feature_status!=CFeature.STATUS[-1][0]
    features = list(filter(not_ready,features))

    #not_ready = lambda item:item.coverage_status!=CFeature.STATUS[-1][0] and item.coverage_status!=CFeature.STATUS[-2][0]
    not_ready = lambda item:item.coverage_status!=CFeature.STATUS[-1][0]
    coverage = list(filter(not_ready,coverage))

    #not_ready = lambda item:item.stimulus_status!=CFeature.STATUS[-1][0] and item.stimulus_status!=CFeature.STATUS[-2][0]
    not_ready = lambda item:item.stimulus_status!=CFeature.STATUS[-1][0]
    #stimuluses = list(filter(not_ready,stimuluses))

    #not_ready = lambda item:item.check_way_status!=CFeature.STATUS[-1][0] and item.check_way_status!=CFeature.STATUS[-2][0]
    not_ready = lambda item:item.check_way_status!=CFeature.STATUS[-1][0]
    check_ways = list(filter(not_ready,check_ways))
	
    for i in coverage: 
        if i not in features: features.append(i)
    for i in stimuluses: 
        if i not in features: features.append(i)
    for i in check_ways: 
        if i not in features: features.append(i)
	
    #features.sort()

    for i in features: 
    #for i in coverage: 
    #for i in stimuluses: 
    #for i in check_ways: 
        #print("feature status is  ", i.feature_status)
        #print(i.name, "cover sva owner is  ", i.coverage_owner)
        #if i.feature_status == CFeature.STATUS[-1][0] or i.feature_status == CFeature.STATUS[-2][0] or i.owner != user : 
        if i.feature_status == CFeature.STATUS[-1][0] or i.owner != user : 
            i.feature_status = "-"
        if i.coverage_status == CFeature.STATUS[-1][0] or i.coverage_owner != user : 
            i.coverage_status = "-"
        if i.stimulus_status == CFeature.STATUS[-1][0] or i.stimulus_owner != user: 
            i.stimulus_status = "-"
        if i.check_way_status == CFeature.STATUS[-1][0] or i.check_way_owner != user : 
            i.check_way_status = "-"


    return render(request,'vp_web/index_status.html',{
        #'title':'verfication tracking',
        'components':CComponent.objects.all(),
        'com_status':com_status,
        'com_status_header':com_status_header,
        #'components':common_components,
        #'special_components':special_components,
        #'title':format_html('{}\'s worksapce :  ',user.username),
        'user_name':user.username,
        'features':features,
        })

def get_select_option(value,show,choose=False):
    sel_t  = '<option value="{0}" {2}>{1}</option>'
    choose =  format_html('selected="selected"') if choose else format_html('')
    return format_html(sel_t,value,show,choose)


def getAttr(item,attr,next_url):
    if attr == 'feature_status' or attr == 'status' or attr == 'stimulus_status' or attr == 'coverage_status' or attr == 'check_way_status':
        attr='get_%s_display' % attr
    a = getattr(item,attr)
    if attr == 'name':
        name = getattr(item,attr)
        next = "vp_web:%s" % next_url
        myurl = reverse(next,args=(item.id,))
        a = format_html('<a href={}>{}</a>',myurl,name)
    if callable(a) : a = a()
    if hasattr(a,'strftime'):
        a = (a+datetime.timedelta(hours=8)).strftime(' %H:%M %d-%b')
    if a == '':
        a='-'
    return format_html('<td>{}</td>',format_html(str(a).replace('\n','<br>')))

def feature(request,feature_id):

    t_feature = get_object_or_404(CFeature,pk=feature_id)
    #list_display = ['name','owner','coverage','stimulus','stimulus_other','check_way','add_time','modified_time']
    list_display = ['name','owner','coverage_status','stimulus_status','check_way_status','add_time','modified_time']
    items = list(t_feature.cverification_set.all())

    fieldsets = [
            {
            'name'  : 'Action',
            'editable' : True,
            'fields': ['name','description','owner'],
                }
            ]
    get_fields(t_feature,fieldsets)  
    
    component_id = t_feature.component.id

    def get_item(item):
        return list(map(lambda a:getAttr(item,a,'point'),list_display))

    u = str(request.user)
    delete_enable = request.user == t_feature.owner or u == "admin"
    #-------------------------------------------------------------------------------------
    if "_delete" in request.POST:
        try:
            if delete_enable:
                t_feature.delete()
            else:
                print('Sorry, you cant delete for you are not the feaeture owner or administer')

            return HttpResponseRedirect(reverse('vp_web:component', kwargs = {"pk":component_id}))
        except Exception as e:    
            errornote = str(e)+"debug"
    #-------------------------------------------------------------------------------------

    return render(request,'vp_web/feature.html',{
        'title':t_feature.name,
        'description':t_feature.description,
        'heads':list_display,
        'feature':t_feature,
        'infos':fieldsets,
        'delete_enable':delete_enable,
        'results':list(map(get_item,items)),
        })


def component(request,pk):

    com = get_object_or_404(CComponent,pk=pk)
    f = com.cfeature_set.filter(component=com)

    features = CVerification.objects.filter(pk=0)
    
    owner_status = []
    #all_points = CVerification.objects.filter(pk=0)
    for j in f:
        all_points = CVerification.objects.filter(feature=j)
        owner = j.owner

        all_feature_task = 0
        finished_feature_task = 0
        all_coverage_task = 0
        finished_coverage_task = 0
        all_stimulus_task = 0
        finished_stimulus_task = 0
        all_check_way_task = 0
        finished_check_way_task = 0

        all_feature_status = 0
        all_coverage_status = 0
        all_stimulus_status = 0
        all_check_way_status = 0

        for i in all_points:
                #print('current point is : ', i.name)
        #------------------------------------------------------------------------------------
            all_feature_task = all_feature_task + 1
            if i.feature_status == CFeature.STATUS[-1][0] or i.feature_status == CFeature.STATUS[-2][0]:
                finished_feature_task = finished_feature_task + 1
                all_feature_status = all_feature_status + 100
            else:
                all_feature_status = all_feature_status + int(i.feature_status) * 10
        #------------------------------------------------------------------------------------
            all_coverage_task = all_coverage_task + 1
            if i.coverage_status == CFeature.STATUS[-1][0] or i.coverage_status == CFeature.STATUS[-2][0]:
                finished_coverage_task = finished_coverage_task + 1
                all_coverage_status = all_coverage_status + 100
            else:
                all_coverage_status = all_coverage_status + int(i.coverage_status) * 10
        #------------------------------------------------------------------------------------
            all_stimulus_task = all_stimulus_task + 1
            if i.stimulus_status == CFeature.STATUS[-1][0] or i.stimulus_status == CFeature.STATUS[-2][0]: 
                finished_stimulus_task = finished_stimulus_task + 1
                all_stimulus_status = all_stimulus_status + 100
            else:
                all_stimulus_status = all_stimulus_status + int(i.stimulus_status) * 10
        #------------------------------------------------------------------------------------
            all_check_way_task = all_check_way_task + 1
            if i.check_way_status == CFeature.STATUS[-1][0] or i.check_way_status == CFeature.STATUS[-2][0]: 
                finished_check_way_task = finished_check_way_task + 1
                all_check_way_status = all_check_way_status + 100
            else:
                all_check_way_status = all_check_way_status + int(i.check_way_status) * 10

        if all_feature_task == 0 : all_feature_task = 1
        finished_feature_status = round(finished_feature_task*100/all_feature_task)
        finished_feature_status = str(finished_feature_status)+ '%'
        all_feature_status = round(all_feature_status/all_feature_task)
        all_feature_status = str(int(all_feature_status))+ '%'

        if all_coverage_task == 0 : all_coverage_task = 1
        finished_coverage_status = round(finished_coverage_task*100/all_coverage_task)
        finished_coverage_status = str(finished_coverage_status)+ '%'
        all_coverage_status = round(all_coverage_status/all_coverage_task)
        all_coverage_status = str(int(all_coverage_status))+ '%'

        if all_stimulus_task == 0 : all_stimulus_task = 1
        finished_stimulus_status = round(finished_stimulus_task*100/all_stimulus_task)
        finished_stimulus_status = str(finished_stimulus_status)+ '%'
        all_stimulus_status = round(all_stimulus_status/all_stimulus_task)
        all_stimulus_status = str(int(all_stimulus_status))+ '%'

        if all_check_way_task == 0 : all_check_way_task = 1
        finished_check_way_status = round(finished_check_way_task*100/all_check_way_task)
        finished_check_way_status = str(finished_check_way_status)+ '%'
        all_check_way_status = round(all_check_way_status/all_check_way_task)
        all_check_way_status = str(int(all_check_way_status))+ '%'

        #print(owner, 'finished status is ', finished_task, '/', all_task, finished_status)
        element = {'feature':str(j.name), 
                    'owner':str(owner), 
                    'pk':str(j.pk), 
                    'all_feature_status':all_feature_status,
                    'all_coverage_status':all_coverage_status,
                    'all_stimulus_status':all_stimulus_status,
                    'all_check_way_status':all_check_way_status,
                    }
        owner_status.append(element)

    #print(owner_status)

    owner_status_header = ['feature', 'owner', 'feature', 'coverage', 'stimulus', 'check_way']

#delete
#    d= com.cfeature_set.filter(name__startswith='Packet')
#    print('need delete', d)
#    for i in d: i.delete()
#end

    #add vp from list
    #print('pk is', pk)
    #if(pk=='437'): add_vp('/ctwrk/users/felixm/vrg_web/release/vrg_site/vp_web/summit_test')
    #if(pk=='437'): add_vp('/ctwrk/users/robinz/chx002/verification/vp_list_2')
    #if(pk=='437'): add_vp('/haydn/felixm-h/vp_list_2')
    
    #if(pk=='437'): output_vp('/haydn/felixm-h/vp_output')
    #if(pk=='437'): output_class('/haydn/felixm-h/vp_output_class')
    #if(pk=='437'): output_checker('/haydn/felixm-h/vp_output_checker')
    #if(pk=='437'): output_checker('/haydn/felixm-h/vp_output_checker')
    #if(pk=='437'): cross_check_checker('/haydn/felixm-h/vp_output_checker')
    #if(pk=='437'): cross_check_coverage('/haydn/felixm-h/vp_output_coverage')
    #if(pk=='437'): cross_check_stimulus('/haydn/felixm-h/vp_output_stimulus', 0)
    #if(pk=='437'): cross_check_stimulus('/haydn/felixm-h/vp_output_stimulus_other', 1)
    #if(pk=='437'): display_cross_check_result()

    #if(pk=='437'): modification_stimulus()
    #if(pk=='437'): modification_register()
    #if(pk=='437'): modification_coverage()
    #if(pk=='437'): modification_check_way()
    #if(pk=='437'): delete_item()
    #if(pk=='437'): query_item()

    def get_item(item):
        return list(map(lambda a:getAttr(item,a,'feature'),list_display))

    u = str(request.user)
    #delete_enable = request.user == com.owner or u == "admin"
    delete_enable = u == "admin"
    print('delete_enable is', delete_enable)
    #-------------------------------------------------------------------------------------
    if "_delete" in request.POST:
        try:
            if delete_enable:
                com.delete()
            else:
                print('Sorry, you cant delete for you are not the feaeture owner or administer')

            return HttpResponseRedirect(reverse('vp_web:index', args = ()))
        except Exception as e:    
            errornote = str(e)+"debug"
    #-------------------------------------------------------------------------------------

    return render(request,'vp_web/component.html',{
        'title':com.name,
        'description':com.description,
        #'heads':list_display,
        'component':com,
        'owner_status':owner_status,
        'owner_status_header':owner_status_header,       
        'delete_enable':delete_enable,
        })

# Create your views here.
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

    context[REDIRECT_FIELD_NAME] = reverse('vp_web:index')
    context.update(extra_context or {})

    defaults = {
            'extra_context': context,
            'authentication_form': AdminAuthenticationForm,
            'template_name': 'vp_web/login.html',
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
            'next_page' : reverse('vp_web:index'),
        }
    return LogoutView.as_view(**defaults)(request)

def password_change(request, extra_context=None):
    """
    Handles the "change password" task -- both form display and validation.
    """
    from django.contrib.admin.forms import AdminPasswordChangeForm
    from django.contrib.auth.views import password_change
    url = reverse('vp_web:password_change_done')
    defaults = {
        'password_change_form': AdminPasswordChangeForm,
        'post_change_redirect': url,
        'extra_context': dict(**(extra_context or {})),
    }
    defaults['template_name'] = 'vp_web/change_password.html'
    return password_change(request, **defaults)

def password_change_done(request, extra_context=None):
    """
    Displays the "success" page after a password change.
    """
    from django.contrib.auth.views import password_change_done
    defaults = {
        'extra_context': dict( **(extra_context or {})),
    }
    defaults['template_name'] = 'vp_web/change_password_done.html'
    return password_change_done(request, **defaults)

def get_html_content(item,mydict,review):
    input_list = ['name','stimulus','stimulus_other','feature_tag','vector','coverage','check_way','msr_info']

    if mydict['name'] == 'owner':
        users = User.objects.all()
        users_show = map(lambda user : get_select_option(user.id,user.username,user==item.owner) , users)
        content = '\n'.join(users_show)
        mydict['is_select'] = True

    if mydict['name'] == 'coverage_owner':
        users = User.objects.all()
        users_show = map(lambda user : get_select_option(user.id,user.username,user==item.coverage_owner) , users)
        content = '\n'.join(users_show)
        mydict['is_select'] = True

    if mydict['name'] == 'stimulus_owner':
        users = User.objects.all()
        users_show = map(lambda user : get_select_option(user.id,user.username,user==item.stimulus_owner) , users)
        content = '\n'.join(users_show)
        mydict['is_select'] = True

    if mydict['name'] == 'check_way_owner':
        users = User.objects.all()
        users_show = map(lambda user : get_select_option(user.id,user.username,user==item.check_way_owner) , users)
        content = '\n'.join(users_show)
        mydict['is_select'] = True

    if mydict['name'] == 'description' or mydict['name'] == 'coverage_description' or mydict['name'] == 'stimulus_description' or mydict['name'] == 'check_way_description' or mydict['name'] == 'feature_description':
        #style="word-break:break-all;word-wrap:break-word" <pre>{1}</pre>
        content = '<textarea class="vLargeTextField" cols="40" id="id_{0}" maxlength="2000" name="{0}" rows="10">{1}</textarea>'.format(mydict['name'],getattr(item,mydict['name']))

    if mydict['name'] in input_list:
        content = '<input class="vTextField" id="id_{0}" maxlength="500" name="{0}" type="text" value="{1}" required />'.format(mydict['name'],getattr(item,mydict['name']))

    if mydict['name'] == 'effort':
        feature_status_show = map(lambda item : get_select_option(item[0],item[1]),CVerification.EFFORT)
        content = format_html('\n'.join(feature_status_show))
        mydict['is_select'] = True

    if mydict['name'] == 'status' or mydict['name'] == 'verify_status' or mydict['name'] == 'feature_status' or mydict['name'] == 'coverage_status'  or mydict['name'] == 'stimulus_status' or mydict['name'] == 'check_way_status'  :
        if review:
            feature_status_show = map(lambda status : get_select_option(status[0],status[1],choose=status[0]==getattr(item,mydict['name'])),CVerification.STATUS) #not include done staus
        else:
            feature_status_show = map(lambda status : get_select_option(status[0],status[1],choose=status[0]==getattr(item,mydict['name'])),CVerification.STATUS[0:11]) #not include done staus
        content = format_html('\n'.join(feature_status_show))
        mydict['is_select'] = True

    if mydict['name'] == 'into_regression'  :
        if review:
            feature_status_show = map(lambda status : get_select_option(status[0],status[1],choose=status[0]==getattr(item,mydict['name'])),CVerification.VRG_STATUS) #not include done staus
        else:
            feature_status_show = map(lambda status : get_select_option(status[0],status[1],choose=status[0]==getattr(item,mydict['name'])),CVerification.VRG_STATUS[0:11]) #not include done staus
        content = format_html('\n'.join(feature_status_show))
        mydict['is_select'] = True

    #print('content is : ',content)
    #re.sub(r"\n", "<br/>", content)
    #if(content.find('faf') != -1):
    #    print('get: ',content)
    #else:
    #    print('not get: ',content.find('faf'))

    mydict['content'] = format_html(content)

    #gen comment
    color = '#873422'
    if mydict['name'] == 'name':
        comment = '<font color={1}>Please fill feature point\'s name</font>'.format(mydict['name'],color)
    elif mydict['name'] == 'description':
        comment = '<font color={1}>Please fill feature point\'s description, or the verification requeirement</font>'.format(mydict['name'],color)
    elif mydict['name'] == 'msr_info':
        comment = '<font color={1}>Please fill related msr info, like "0x1234[5]" or "no msr"</font>'.format(mydict['name'],color)
    elif mydict['name'] == 'feature_tag':
        comment = '<font color={1}>Please fill feature tag, like "DATA_LOAD"</font>'.format(mydict['name'],color)
    elif mydict['name'] == 'coverage':
        comment = '<font color={1}>Please fill coverage file name, format is "c_xxx", like "c_DATA_lOAD"</font>'.format(mydict['name'],color)
    elif mydict['name'] == 'coverage_description':
        comment = '<font color={1}>Please descripe how to confirm this feature point is happened</font>'.format(mydict['name'],color)
    elif mydict['name'] == 'stimulus':
        comment = '<font color={1}>Please fill class/vector file name, like "dataload.sv" </font>'.format(mydict['name'],color)
    elif mydict['name'] == 'stimulus_other':
        comment = '<font color={1}>Please fill class/vector file name, it can be same as class for single socket</font>'.format(mydict['name'],color)
    elif mydict['name'] == 'stimulus_description':
        comment = '<font color={1}>Please descripe how to tigger this feature point in class or user vector, can indicate weigth variable name if need</font>'.format(mydict['name'],color)
    elif mydict['name'] == 'check_way':
        comment = '<font color={1}>Please fill checker name/error sva name/vector name, like "xxx checker" or "a_xxx" or "xxx.src"</font>'.format(mydict['name'],color)
    elif mydict['name'] == 'check_way_description':
        comment = '<font color={1}>Please descripe how to capture bug when this feature point works wrong</font>'.format(mydict['name'],color)
    elif mydict['name'] in input_list:
        comment = '<font color={1}>Please fill {0} file name</font>'.format(mydict['name'],color)
    else:
        comment = ''

    mydict['comment'] = format_html(comment)
    

def get_content(item,name):
    if name == 'feature_status' or name == 'status' or name == 'into_regression' or name == 'coverage_status' or name == 'stimulus_status' or name == 'check_way_status':
        name='get_%s_display' % name
    attr = getattr(item,name)
    return attr

def get_fields(item,fieldsets,review=0):
    if not fieldsets : return 
    name_change = {}
    for line in fieldsets:
        if not line['editable']:
            for i in range(len(line['fields'])):
                name = line['fields'][i]
                content = get_content(item,name)
                #print('name is : ',name)
                if(re.search('description', name)):
                #    print('find desc: ',name)
                    #content = re.sub("<br/>", "\\n", content)
                    content = re.sub("{", "(", content)
                    content = re.sub("}", ")", content)
                #print('content is : ',content)
                if content == '' : content = '-'
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
                get_html_content(item,mydict,review)
                #mydict = mydict.replace('<br/>', '\\n')
                #mydict = mydict.replace('\n', '<br/>')
                #mydict = mydict.replace('faf', '<br/>')
                #mydict = mydict.replace('<br/>', 'faf')
                #re.sub(r"faf", "br", mydict)
                line['fields'][i] = mydict


def point(request,pk):
    item = get_object_or_404(CVerification,pk=pk)
    update = False

    #if '_save' in request.POST and 'user' in request :
    if '_save' in request.POST :
        content = request.POST['comment'].strip()
        if not content == "":
            author = request.user
            item.pointcomment_set.create(Author=author,content=content)
            item.save()

    fieldsets = [
            {
                'name'     : 'Feature point',
                'editable' : False,
                'fields'   : ['name','description','feature_tag','owner','feature_status']
                },
			{
                'name'     : 'Coverage',
                'editable' : False,
                'fields'   : ['coverage','coverage_description','coverage_owner','coverage_status']
                },
			{
                'name'     : 'Stimulus',
                'editable' : False,
                'fields'   :
				['stimulus','stimulus_description','stimulus_owner','into_regression','stimulus_status']
                },
            {
                'name'     : 'Check way',
                'editable' : False,
                'fields'   : ['check_way','check_way_description','check_way_owner','check_way_status']
                }
            ]

    csd = item.coverage_description
    csd = re.sub("{", "[", csd)
    csd = re.sub("}", "]", csd)
    item.coverage_description = csd
    item.save()

    get_fields(item,fieldsets)
    #print("************Felix point debug ", item.coverage_description)

    feature_id = item.feature.id

    u = str(request.user)
    delete_enable = request.user == item.owner or u == "admin"
    #-------------------------------------------------------------------------------------
    if "_delete" in request.POST:
        try:
            if delete_enable:
                item.delete()
            else:
                print('Sorry, you cant delete for you are not the feaeture owner or administer')
            return HttpResponseRedirect(reverse('vp_web:feature', kwargs = {"feature_id":feature_id}))
        except Exception as e:    
            errornote = str(e)+"debug"
    #-------------------------------------------------------------------------------------

    return render(request,'vp_web/point.html',{
        'title': item.name,
        #'description': item.description,
        'description': '',
        'point':item,
        'infos':fieldsets,
        'delete_enable':delete_enable,
        })

def addFeature(request,com):
    if 'name' not in request.POST or request.POST['name']=='':
        raise Exception('Please input Feature Name')
    name = request.POST['name']
    if CFeature.objects.filter(name=name):
        raise Exception('The Feature cannot be the same in Database. Please Modified the name')
    if 'description' not in request.POST or request.POST['description']=='':
        raise Exception('Please input Some descriptions. Thanks')
    description = request.POST['description']
    if 'owner' not in request.POST:
        raise Exception('Please Choose a Owner')
    owner = User.objects.get(id=int(request.POST['owner']))

    feature = CFeature(name=name,description=description,owner=owner,component=com)
    feature.save()



@login_required
def add_feature(request,pk):
    com = get_object_or_404(CComponent,pk=pk)
    errornote = ""
    feature = CFeature(name='',description='',owner=com.owner,component=com)

    if "_save" in request.POST:
        try:
            addFeature(request,com)
            return HttpResponseRedirect(reverse('vp_web:component', kwargs = {"pk":com.id}))
        except Exception as e:    
            errornote = str(e)

    fieldsets = [
            {
            'name'  : 'Feature type',
            'editable' : True,
            'fields': ['name','description','owner'],
                }
            ]
    get_fields(feature,fieldsets)
    
    #if request.user != com.owner:
    if not (request.user == com.owner or get_edit_ownership(request.user)):
        errornote = "You are not the component owner"
        print("************Felix add_verification debug ", request.user)
        fieldsets = None

    return render( request, 'vp_web/add_feature.html',{
                'title':format_html('Add feature type to <font color="#8B1010">{}</font> ',com.name),
                'infos':fieldsets,
                'errornote':errornote,

        }
            )

@login_required
def change_feature(request,pk):
    feature = get_object_or_404(CFeature,pk=pk)
    errornote = ""
    
    if "_save" in request.POST:
        try:
            feature.name = request.POST['name']
            feature.description = request.POST['description']
            owner = User.objects.get(id=int(request.POST['owner']))
            feature.owner = owner 
            feature.save()
            return HttpResponseRedirect(reverse('vp_web:feature',args = (feature.id,)))
        except Exception as e:    
            errornote = str(e)

    base_field = ['name','description','owner',]

    #if request.user == feature.component.owner:
    #    base_field.append('status')

    fieldsets = [
            {
            'name'  : 'Basic',
            'editable' : True,
            'fields': base_field,
                }
            ]

    #if request.user != feature.owner and request.user != feature.component.owner and not get_edit_ownership(request.user):
    if not (request.user == feature.owner or request.user == feature.component.owner or get_edit_ownership(request.user)):
        errornote = "You are not the feature or component owner"
        fieldsets = None


    get_fields(feature,fieldsets)


    return render( request, 'vp_web/add_feature.html',{
        'title':format_html('Modified feature : {} ',feature.name),
                'infos':fieldsets,
                'errornote':errornote,

        }
)

@login_required
def add_verification(request,pk):
    feature = get_object_or_404(CFeature,pk=pk)
    #item = CVerification(name='',feature_description='',owner=feature.owner,feature=feature)
    #item = CVerification(feature_name=feature.name, description=feature.description, owner=feature.owner, feature=feature, coverage_owner=feature.owner, stimulus_owner=feature.owner, check_way_owner=feature.owner)
    item = CVerification(name='', description='', owner=feature.owner, feature=feature, coverage_owner=feature.owner, stimulus_owner=feature.owner, check_way_owner=feature.owner)
    errornote = ""
    #print("************Felix add_verification debug flag 1*******************")
    #print("************Felix add_verification debug ", item.owner, item.feature, item.feature.description)
    
    if "_save" in request.POST:
        try:
            owner = User.objects.get(id=int(request.POST['owner']))
            item.owner = owner 
            item.reviewer = feature.owner 
            item.name = request.POST['name']
            #item.feature_name = request.POST['name']
            #item.feature_description = 'xx'
            item.description = request.POST['description']
            #item.msr_info = request.POST['msr_info']
            #if item.msr_info == "":
            #    raise Exception('Please fill msr info')
            item.feature_tag = request.POST['feature_tag']
            if item.feature_tag == "":
                raise Exception('Please fill feature tag')
            item.feature_status = request.POST['feature_status']
            item.coverage_owner  = User.objects.get(id=int(request.POST['coverage_owner']))
            item.cover_sva_owner  = User.objects.get(id=int(request.POST['coverage_owner']))
            item.stimulus_owner  = User.objects.get(id=int(request.POST['stimulus_owner']))
            item.check_way_owner  = User.objects.get(id=int(request.POST['check_way_owner']))
            #item.check_way = ''
            #item.check = ''
            #item.coverage = ''
            item.save()
            return HttpResponseRedirect(reverse('vp_web:feature',args = (feature.id,)))
        except Exception as e:    
            errornote = str(e)

    fieldsets = [
			#{
            #'name'  : 'Feature type',
            #'editable' : False,
            #'fields': ['feature.name'],
            #    },
            {
            'name'  : 'Verification point',
            'editable' : True,
            #'fields': ['feature_owner','feature_name','feature_description','msr_info','feature_tag','coverage_owner','feature_status'],
            'fields': ['name','owner','description','feature_tag','coverage_owner','feature_status'],
                },
            {
            'name'  : 'Verification',
            'editable' : True,
            'fields' : ['stimulus_owner', 'check_way_owner']
            },
            ]

   # if request.user != feature.owner and request.user != feature.component.owner:
    if not (request.user == feature.owner or request.user != feature.component.owner or get_edit_ownership(request.user)):
        errornote = "You are not the feature or component owner"
        fieldsets = None

    get_fields(item,fieldsets)

    return render( request, 'vp_web/add_feature.html',{
		'title':format_html('Add Verification Point to Feature Type => {} ',feature.name),
                'infos':fieldsets,
                'errornote':errornote,

        }
)


@login_required
def change_verification(request,pk):
    item = get_object_or_404(CVerification,pk=pk)
    errornote = ""

    base_field = ['owner','name','description','feature_tag']
    if request.user == item.owner or request.user == item.reviewer or request.user == item.feature.component.owner or get_edit_ownership(request.user):
        #base_field.append('status')
        base_field.append('feature_status')
        base_editable = True
    else : 
        base_editable = False

    coverage_field = ['coverage','coverage_description','coverage_owner']
    if request.user == item.coverage_owner or request.user == item.reviewer or request.user == item.feature.component.owner or get_edit_ownership(request.user):
        coverage_field.append('coverage_status')
        coverage_editable = True
    else : 
        coverage_editable = False

    stimulus_field = ['stimulus','stimulus_description','stimulus_owner']
    if request.user == item.stimulus_owner or request.user == item.reviewer or request.user == item.feature.component.owner or get_edit_ownership(request.user):
        stimulus_field.append('into_regression')
        stimulus_field.append('stimulus_status')
        stimulus_editable = True
    else : 
        stimulus_editable = False

    check_way_field = ['check_way','check_way_description','check_way_owner']
    if request.user == item.check_way_owner or request.user == item.reviewer or request.user == item.feature.component.owner or get_edit_ownership(request.user):
        check_way_field.append('check_way_status')
        check_way_editable = True
    else : 
        check_way_editable = False
    #print("************Felix change_verification debug flag 1*******************")

    if '_save' in request.POST and 'user' in request :
        content = request.POST['comment'].strip()
        if not content == "":
            author = request.user
            item.pointcomment_set.create(Author=author,content=content)
            #item.save()    
		
    if "_save" in request.POST:
        try:
            if(base_editable):
                owner = User.objects.get(id=int(request.POST['owner']))
                item.owner = owner 
                item.name = request.POST['name']
                item.description = request.POST['description']
                #item.msr_info = request.POST['msr_info']
                #if item.msr_info == "":
                #    raise Exception('Please fill msr info')
                item.feature_tag = request.POST['feature_tag']
                if item.feature_tag == "":
                    raise Exception('Please fill feature tag')
                item.feature_status = request.POST['feature_status']

            if(coverage_editable):
                item.coverage  = request.POST['coverage']
                item.coverage_owner  = User.objects.get(id=int(request.POST['coverage_owner']))
                csd = request.POST['coverage_description']
                csd = re.sub("{", "[", csd)
                csd = re.sub("}", "]", csd)
                item.coverage_description = csd
                item.coverage_status = request.POST['coverage_status']

            if(stimulus_editable):
                temp = request.POST['stimulus']
                if(request.POST['stimulus']):
                    item.stimulus  = request.POST['stimulus']
                #item.stimulus_other = request.POST['stimulus_other']
                item.stimulus_owner  = User.objects.get(id=int(request.POST['stimulus_owner']))
                #item.stimulus_description = request.POST['stimulus_description']
                sd = request.POST['stimulus_description']
                sd = re.sub("{", "[", sd)
                sd = re.sub("}", "]", sd)
                item.stimulus_description = sd
                #print('sd is : ',sd)
                item.into_regression = request.POST['into_regression']
                item.stimulus_status = request.POST['stimulus_status']

            if(check_way_editable):
                item.check_way  = request.POST['check_way']
                item.check_way_owner  = User.objects.get(id=int(request.POST['check_way_owner']))
                cd = request.POST['check_way_description']
                cd = re.sub("{", "[", cd)
                cd = re.sub("}", "]", cd)
                item.check_way_description = cd
                item.check_way_status = request.POST['check_way_status']

            item.save()
            return HttpResponseRedirect(reverse('vp_web:point',args = (item.id,)))
        except Exception as e:    
            errornote = str(e)+"debug"

    #base_field = ['owner','name','description','feature_tag','coverage',]



    #print("************Felix change_verification debug flag 2*******************")
    fieldsets = [
            {
				'name'  : 'Feature point',
            	'editable' : base_editable,
            	'fields': base_field,
                },
			{
                'name'     : 'Coverage',
                'editable' : coverage_editable,
                'fields'   : coverage_field
                },
			{
                'name'     : 'Stimulus',
                'editable' : stimulus_editable,
                'fields'   : stimulus_field
                },
            {
                'name'     : 'Check way',
                'editable' : check_way_editable,
                'fields'   : check_way_field
                }
            ]

    if request.user != item.owner \
        and request.user != item.feature.component.owner \
        and request.user != item.coverage_owner \
        and request.user != item.stimulus_owner \
        and request.user != item.check_way_owner \
		and not get_edit_ownership(request.user):
        errornote = "You are not the verification or component owner"
        fieldsets = None

    #u = '%s' % request.user
    #review_enable = u == 'felixm-h'
    #review_enable = request.user == item.feature.component.owner
    review_enable = request.user == item.reviewer

    #print("************Felix change_verification debug flag 3*******************")
    get_fields(item,fieldsets,review_enable)
    #print("************Felix change_verification debug flag 4*******************")
    return render( request, 'vp_web/change_point.html',{
        'title':format_html('Change verification point : {} ',item.name),
                'point':item,
                'infos':fieldsets,
                'errornote':errornote,
        }
)

def workspace(request,pk):
    user = get_object_or_404(User,pk=pk)
    #features = CFeature.objects.filter(owner=user)
    features = CVerification.objects.filter(owner=user)
    coverage = CVerification.objects.filter(coverage_owner=user)
    stimuluses = CVerification.objects.filter(stimulus_owner=user)
    check_ways = CVerification.objects.filter(check_way_owner=user)

    #not_ready = lambda item:item.feature_status!=CFeature.STATUS[-1][0] and item.feature_status!=CFeature.STATUS[-2][0]
    not_ready = lambda item:item.feature_status!=CFeature.STATUS[-1][0]
    features = list(filter(not_ready,features))

    #not_ready = lambda item:item.coverage_status!=CFeature.STATUS[-1][0] and item.coverage_status!=CFeature.STATUS[-2][0]
    not_ready = lambda item:item.coverage_status!=CFeature.STATUS[-1][0]
    coverage = list(filter(not_ready,coverage))

    #not_ready = lambda item:item.stimulus_status!=CFeature.STATUS[-1][0] and item.stimulus_status!=CFeature.STATUS[-2][0]
    not_ready = lambda item:item.stimulus_status!=CFeature.STATUS[-1][0]
    #stimuluses = list(filter(not_ready,stimuluses))

    #not_ready = lambda item:item.check_way_status!=CFeature.STATUS[-1][0] and item.check_way_status!=CFeature.STATUS[-2][0]
    not_ready = lambda item:item.check_way_status!=CFeature.STATUS[-1][0]
    check_ways = list(filter(not_ready,check_ways))
	
    for i in coverage: 
        if i not in features: features.append(i)
    for i in stimuluses: 
        if i not in features: features.append(i)
    for i in check_ways: 
        if i not in features: features.append(i)
	
    #features.sort()

    for i in features: 
    #for i in coverage: 
    #for i in stimuluses: 
    #for i in check_ways: 
        #print("feature status is  ", i.feature_status)
        #print(i.name, "cover sva owner is  ", i.coverage_owner)
        #if i.feature_status == CFeature.STATUS[-1][0] or i.feature_status == CFeature.STATUS[-2][0] or i.owner != user : 
        if i.feature_status == CFeature.STATUS[-1][0] or i.owner != user : 
            i.feature_status = "-"
        if i.coverage_status == CFeature.STATUS[-1][0] or i.coverage_owner != user : 
            i.coverage_status = "-"
        if i.stimulus_status == CFeature.STATUS[-1][0] or i.stimulus_owner != user: 
            i.stimulus_status = "-"
        if i.check_way_status == CFeature.STATUS[-1][0] or i.check_way_owner != user : 
            i.check_way_status = "-"

    return render( request, 'vp_web/workspace.html',{
        'title':format_html('{}\'s worksapce :  ',user.username),
        'features':features,
        }
)

def review(request,pk):
    user = get_object_or_404(User,pk=pk)
    features = CVerification.objects.filter(owner=user)
    need_review = CVerification.objects.filter(reviewer=user)
    coverage = CVerification.objects.filter(coverage_owner=user)
    stimuluses = CVerification.objects.filter(stimulus_owner=user)
    check_ways = CVerification.objects.filter(check_way_owner=user)

    not_close = lambda item:item.feature_status==CFeature.STATUS[-2][0] 
    features = list(filter(not_close,features))

    not_close = lambda item:item.coverage_status==CFeature.STATUS[-2][0]
    coverage = list(filter(not_close,coverage))

    not_close = lambda item:item.stimulus_status==CFeature.STATUS[-2][0]
    stimuluses = list(filter(not_close,stimuluses))

    not_close = lambda item:item.check_way_status==CFeature.STATUS[-2][0]
    check_ways = list(filter(not_close,check_ways))

    for i in coverage: 
        if i not in features: features.append(i)
    for i in stimuluses: 
        if i not in features: features.append(i)
    for i in check_ways: 
        if i not in features: features.append(i)

    #for i in features: 
    for i in need_review: 
        #print("feature status is  ", i.feature_status)
        if i.feature_status != CFeature.STATUS[-2][0] : 
            i.feature_status = "-"
        if i.coverage_status != CFeature.STATUS[-2][0] : 
            i.coverage_status = "-"
        if i.stimulus_status != CFeature.STATUS[-2][0] : 
            i.stimulus_status = "-"
        if i.check_way_status != CFeature.STATUS[-2][0] : 
            i.check_way_status = "-"

    return render( request, 'vp_web/review.html',{
        'title':format_html('Need {} Review:  ',user.username),
        'features':need_review,
        }
)

def status_list(request,pk):
    user = get_object_or_404(User,pk=pk)
    u = '%s' % user
    features = CVerification.objects.filter(reviewer=user)
    #if u == "FelixMa" : features = CVerification.objects.filter(pk__gt=50)
                
    #for i in features:
    #    sd = i.stimulus_description
    #    #if(re.search('<br/>', sd) is not None): 
    #    #    print('find br: ',name)
    #    #sd = re.sub("{", "(", sd)
    #    #sd = re.sub("}", ")", sd)
    #    sd = re.sub("\r\n", "\n", sd)
    #    sd = re.sub("\n", "</br>/|safe", sd)
    #    #sd = re.sub("safd", "\\n", sd)
    #    i.stimulus_description = sd
    #    i.save()

    #if u == "FelixMa" :
    #    l2_features = CVerification.objects.filter(reviewer=get_object_or_404(User,pk=9))
    #    for i in l2_features:
    #        if(i.coverage_owner== User.objects.get(id=8)):
    #            i.coverage_owner = User.objects.get(id=2)
    #        if(i.stimulus_owner== User.objects.get(id=2)):
    #            i.stimulus_owner= User.objects.get(id=8)
    #        i.save()

    #if u == "FelixMa" :
    #    sys_features = CVerification.objects.filter(reviewer=get_object_or_404(User,pk=13))
    #    for i in sys_features:
    #        if(re.match('^(P-State|MCA)', i.feature.name) is None):
    #            print('Find SYS related: ', i.feature.name)
    #            i.coverage_owner = User.objects.get(id=13)
    #            i.stimulus_owner = User.objects.get(id=13)
    #            i.check_way_owner = User.objects.get(id=13)
                #i.save()

    #if u == "FelixMa" :
    #    sys_features = CVerification.objects.filter(reviewer=get_object_or_404(User,pk=13))
    #    for i in sys_features:
    #        print('Find SYS related: ', i.feature.name)
    #        if(re.match('^(MCA_SMI)', i.feature.name) is not None):
    #            print('Find SMI related: ', i.feature.name)
            #i.save()

    #change apic reviewer from Dorian to Cheryl
    #if u == "FelixMa" :
        #apic_features = CVerification.objects.filter(reviewer=get_object_or_404(User,pk=3))
        #com = get_object_or_404(CComponent,pk=10)
        #f = com.cfeature_set.filter(component=com)
        #apic_features = CVerification.objects.filter(pk=0)
        #for i in f:
        #    new = CVerification.objects.filter(feature=i)
        #    apic_features = chain(apic_features, new)
        #for i in apic_features:
        #    print('Find APIC related: ', i.feature.name)
        #    i.reviewer=get_object_or_404(User,pk=22)
        #    i.save()

    #change sys owner from Jason to Bert
    #if u == "FelixMa" :
    #    sys_features = CVerification.objects.filter(reviewer=get_object_or_404(User,pk=13))
    #    for i in sys_features:
    #        print('Find SYS related: ', i.name)
    #        print('Find SYS owner: ', i.owner)
    #        i.feature.owner = User.objects.get(id=20)
    #        i.owner = User.objects.get(id=20)
    #        i.coverage_owner = User.objects.get(id=20)
    #        i.stimulus_owner = User.objects.get(id=20)
    #        i.check_way_owner = User.objects.get(id=20)
    #        i.save() 
            
    #if u == "FelixMa" :
    #    com = get_object_or_404(CComponent,pk=12)
    #    f = com.cfeature_set.filter(component=com)
    #    for i in f:
    #         i.owner = User.objects.get(id=20)
    #         print('Find SYS owner: ', i.owner)
    #         i.save()

    return render( request, 'vp_web/status_list.html',{
		'title':format_html('All status list for {} : ',user.username),
        'features':features,
        }
    )

def component_status_list(request,pk):
    com = get_object_or_404(CComponent,pk=pk)
    f = com.cfeature_set.filter(component=com)
    #print('feature type is: ', f)
    features = CVerification.objects.filter(pk=0)
    #print('feature point is: ', features)
    for i in f:
        new = CVerification.objects.filter(feature=i)
        features = chain(features, new)
    #print('feature point is: ', features)
    
    all_points = CVerification.objects.filter(pk=0)
    for i in f:
        a = CVerification.objects.filter(feature=i)
        all_points = chain(all_points, a)

   # if str(com.owner) == "FelixMa" :
    owner_list = []
    #print('got felix feature: ', com.name)
    #got all task owner
    for i in all_points:
        if i.owner not in owner_list: owner_list.append(i.owner)
        if i.coverage_owner not in owner_list: owner_list.append(i.coverage_owner)
        if i.stimulus_owner not in owner_list: owner_list.append(i.stimulus_owner)
        if i.check_way_owner not in owner_list: owner_list.append(i.check_way_owner)
    #print('got owner list: ', owner_list)



    #got task finished status
    owner_status = []
    for owner in owner_list:
        all_task = 0
        finished_task = 0
        #print('current owner is : ', owner)
        
        #repeat again, for it will disapper after used
        all_points = CVerification.objects.filter(pk=0)
        for i in f:
            a = CVerification.objects.filter(feature=i)
            all_points = chain(all_points, a)

        for i in all_points:
            #print('current point is : ', i.name)
    #------------------------------------------------------------------------------------
            if owner == i.owner: 
                all_task = all_task + 1
                if i.feature_status == CFeature.STATUS[-1][0] or i.feature_status == CFeature.STATUS[-2][0]: finished_task = finished_task + 1
    #------------------------------------------------------------------------------------
            if owner == i.coverage_owner: 
                all_task = all_task + 1
                if i.coverage_status == CFeature.STATUS[-1][0] or i.coverage_status == CFeature.STATUS[-2][0]: finished_task = finished_task + 1
    #------------------------------------------------------------------------------------
            if owner == i.stimulus_owner: 
                all_task = all_task + 1
                if i.stimulus_status == CFeature.STATUS[-1][0] or i.stimulus_status == CFeature.STATUS[-2][0]: finished_task = finished_task + 1
    #------------------------------------------------------------------------------------
            if owner == i.check_way_owner: 
                all_task = all_task + 1
                if i.check_way_status == CFeature.STATUS[-1][0] or i.check_way_status == CFeature.STATUS[-2][0]: finished_task = finished_task + 1

        finished_status = round(finished_task*100/all_task)
        finished_status = str(finished_status)+ '%'
        #print(owner, 'finished status is ', finished_task, '/', all_task, finished_status)
        element = {'owner':str(owner), 'all_task':all_task, 'finished_task':finished_task, 'finished_status':finished_status}
        owner_status.append(element)

    #print(owner_status)

    owner_status_header = ['owner','all_task','finished_task','finished_status','']


    return render( request, 'vp_web/status_list.html',{
		'title':format_html('All status list for {} : ',com.name),
        'features':features,
        'owner_status':owner_status,
        'owner_status_header':owner_status_header,
        }
    )

def get_edit_ownership(request_user):
    u = '%s' % request_user
    #if u == "FelixMa":
    if u == "TonyShi" or u == "ZhongminChen" or u == "GeoffreyLiu" or u == "FelixMa":
        #print("************Felix get_edit_ownership debug ", request_user)
        return 1
    else: 
        return 0
    
def add_vp(file):
    f = open(file)
    for line in f.readlines():
        #m = re.match('^(\s*\/)', line)
        #print('first m is ', m.groups())
        if(re.match('^(\s*\/)', line) is not None):
            print('find comment :', line)
            continue
        elif(re.match('(\w+)', line) is None):
            print('find null :', line)
            continue
        
        com = get_object_or_404(CComponent,pk=4)
        print('com owner is ', com.owner)
        
        table = {
                'RobinZheng' : 9,
                'simonzhai' : 8,
                'GeoffreyLiu' : 2,
                'JohnnyWang' : 10,
                }
        print('Robin id is ', table['RobinZheng'])
        slice = line.split(';')
        num = 1
        for i in slice:
            print('slice %d: %s'%(num, i))
            item = i.split(',')
            if num == 1:
                #print('org item 0 is', item[0])
                item[0] = re.sub('\s+', '', item[0])
                print('item 0 is:%s'%item[0])
                existed_feature = CFeature.objects.filter(name=item[0])
                feature = existed_feature.last()
                print('query result is :', feature)
                feature_s = '%s' % feature
                    #pk = existed_feature.object.pk
                    #getattr(existed_feature,'name')
                    #print('pk = ', pk)
                    #feature = get_object_or_404(CFeature,pk=pk)
                try:
                    if(feature_s == 'None'):
                        print('no existed feature, need setup a new')
                        feature = CFeature(owner=com.owner, name=item[0], description=item[0],component=com)
                        feature.save()
                    else:
                        print('find existed feature:', existed_feature)
                        print('feature type is', type(feature))
                except:
                    #feature = CFeature(owner=com.owner, name=item[0], description=item[0])
                    #feature.save()
                    print('not find and save new feature ', feature.name)

            if num == 2:
                print('i is: ', i)
                m = re.match('\s*(\w+),\s+"(.*)",\s+(.*),\s+(\w+),\s+(\w+),\s+(.+)', i)
                print('m is: ', m.groups())
                owner = User.objects.get(id=table[m.group(5)])
                vp = CVerification(name=m.group(1), description=m.group(2), msr_info=m.group(3), feature_tag=m.group(4), feature_status=m.group(6), owner=owner, reviewer=owner)
                vp.feature = feature
                #vp.feature.save()
                print('type is', type(feature))
                #feture_dict = model_to_dict(feature)
                #feature_list = list(feature)
                #print('type is', type(feature_list))
                #print('featue_list is', feature_list)
                #vp.feature = feature_list
                #vp.feature.name=getattr(feature,name)
                print('vp is ', vp)
                #vp.feature.name=item[0]
                #vp.feature.owner=com.owner
                print('m5 is: ', m.group(5))
                print('feature is ', feature)
            if num == 3:
                m = re.match('\s*(.*), (.*), (\w+)', i)
                print('m is: ', m.groups())
                print('m2 is: ', m.group(2))
                vp.coverage_owner = User.objects.get(id=table[m.group(2)])
            if num == 4:
                m = re.match('\s*(.*), (.*), (.*), (\w+)', i)
                print('m is: ', m.groups())
                print('m2 is: ', m.group(2))
                vp.stimulus_owner = User.objects.get(id=table[m.group(2)])
            if num == 5:
                m = re.match('\s*(.*), (.*), (\w+)', i)
                print('m is: ', m.groups())
                print('m2 is: ', m.group(2))
                vp.check_way_owner = User.objects.get(id=table[m.group(2)])
                vp.save()

            num = num + 1


def output_vp(file):
    f = open(file, 'w')
    f.write('Cover sva name is: \n')

    #apic_features = CVerification.objects.filter(reviewer=get_object_or_404(User,pk=3))

    all_com = CComponent.objects.all()
    apic_com = get_object_or_404(CComponent,pk=10)

    for com in all_com:
        feature = com.cfeature_set.filter(component=com)
        vps = CVerification.objects.filter(pk=0)
        for i in feature:
            new = CVerification.objects.filter(feature=i)
            vps = chain(vps, new)
        for i in vps:
            print('Find APIC related: ', i.coverage)
            print('Cover status : ', i.coverage_status)
            
            if i.coverage_status == CFeature.STATUS[-1][0] or i.coverage_status == CFeature.STATUS[-2][0]:
                if(not re.match('c_', i.coverage)):
                    f.write('Find invalid cover sva name: ' + i.name + '->' + i.coverage + ' pk=' + str(i.pk) + 'owner is ' + i.coverage_owner + '\n')
                else:
                    f.write(i.coverage + '\n')

#---------------------------------------------------------------------------------------                 
def output_class(file):
    f = open(file, 'w')
    f.write('Class name is: \n')

    #apic_features = CVerification.objects.filter(reviewer=get_object_or_404(User,pk=3))

    all_com = CComponent.objects.all()
    apic_com = get_object_or_404(CComponent,pk=10)

    for com in all_com:
        feature = com.cfeature_set.filter(component=com)
        vps = CVerification.objects.filter(pk=0)
        for i in feature:
            new = CVerification.objects.filter(feature=i)
            vps = chain(vps, new)
        for i in vps:
            print('Find class single: ', i.stimulus)
            print('Find class dual: ', i.stimulus_other)
            #print('Class status : ', i.stimulus_status)
            
            if i.stimulus_status == CFeature.STATUS[-1][0] or i.stimulus_status == CFeature.STATUS[-2][0]:
                if(not re.match('\s*\w+.sv', i.stimulus)):
                    f.write('Find invalid class name: ' + i.name + ' -> ' + i.stimulus + ' pk=' + str(i.pk) + 'owner is ' + i.stimulus_owner + '\n')
                else:
                    f.write(i.stimulus + '\n')
                    f.write(i.stimulus_other + '\n')

#---------------------------------------------------------------------------------------                 
def output_checker(file):
    f = open(file, 'w')
    f.write('Checker name is: \n')

    #apic_features = CVerification.objects.filter(reviewer=get_object_or_404(User,pk=3))

    all_com = CComponent.objects.all()
    apic_com = get_object_or_404(CComponent,pk=10)

    for com in all_com:
        feature = com.cfeature_set.filter(component=com)
        vps = CVerification.objects.filter(pk=0)
        for i in feature:
            new = CVerification.objects.filter(feature=i)
            vps = chain(vps, new)
        for i in vps:
            print('Find check way: ', i.check_way)
            #print('Class status : ', i.check_way_status)
            
            if i.check_way_status == CFeature.STATUS[-1][0] or i.check_way_status == CFeature.STATUS[-2][0]:
                f.write(i.check_way + ' -> ' + i.name + ' pk=' + str(i.pk) + '-> owner is ' + str(i.check_way_owner) + '\n')
                #if(not re.match('\s*\w+.sv', i.check_way)):
                    #f.write('Find invalid checker name: ' + i.name + ' -> ' + i.check_way + ' pk=' + str(i.pk) + '-> owner is ' + str(i.check_way_owner) + '\n')
                #else:
                #f.write(i.check_way + '\n')

#---------------------------------------------------------------------------------------                 
def cross_check_update(request):
    u = '%s' % request.user
    if u == "FelixMa" : 
        print('it is felix')
        os.system('/ctwrk/users/felixm/vrg_web/release/vrg_site/gen_checker_list.pl')
        print('Gen checker list done')
        os.system('/ctwrk/users/felixm/vrg_web/release/vrg_site/gen_coverage_list.pl')
        os.system('/ctwrk/users/felixm/vrg_web/release/vrg_site/gen_stimulus_list.pl')

        cross_check_checker('/haydn/felixm-h/vp_output_checker')
        cross_check_coverage('/haydn/felixm-h/vp_output_coverage')
        cross_check_stimulus('/haydn/felixm-h/vp_output_stimulus', 0)
        cross_check_stimulus('/haydn/felixm-h/vp_output_stimulus_other', 1)

    common_components = CComponent.objects.exclude(pk=437)
    special_components = CComponent.objects.filter(pk=437)

    return render(request,'vp_web/index.html',{
        'title':'verfication tracking',
        #'components':CComponent.objects.all(),
        'components':common_components,
        'special_components':special_components,
        }) 
#---------------------------------------------------------------------------------------                 
def cross_check_checker(file):
    f = open(file, 'w')
    f.write('Checker name is: \n')

    #apic_features = CVerification.objects.filter(reviewer=get_object_or_404(User,pk=3))

    all_com = CComponent.objects.all()
    apic_com = get_object_or_404(CComponent,pk=10)

    for com in all_com:
        feature = com.cfeature_set.filter(component=com)
        vps = CVerification.objects.filter(pk=0)
        for i in feature:
            new = CVerification.objects.filter(feature=i)
            vps = chain(vps, new)

        #vps = CVerification.objects.filter(pk=734)#FIXME
        for i in vps:
            #print('Find check way: ', i.check_way)
            #print('Class status : ', i.check_way_status)
            
            if i.check_way_status == CFeature.STATUS[-1][0] or i.check_way_status == CFeature.STATUS[-2][0]:

                find = 0

                item = str(i.check_way)
                item_pk = str(i.pk)
                #print('got line: ', line)
                if (re.search('^\s*(\w+)->', item)) :
                    m = re.search('^\s*(\w+)->', item)
                    temp = m.group(1)

                    civ_checker_list = open('/haydn/felixm-h/civ_checker.list')
                    for line in civ_checker_list.readlines():
                        item = temp
                        #print('got line: ', line)
                        if (re.match(item, line)) :
                            #print('match item: ', item)
                            find = 1
                            break

                elif (re.search(',', item)) :
                    total_cov = 0
                    hit_cov = 0
                    #item.split('\s*,\s*')
                    #item.split(', ')
                    #item = item.split(' ')
                    #item = item.replace(', ', ',')
                    item = item.split(',')

                    t = []

                    for j in item:
                        if(re.match('^\s*$', j)):
                            pass
                            #item.remove(j)
                            #print('Need delete -> ', j)
                        else:
                            t.append(j)

                    for j in t:
                        total_cov = total_cov + 1
                        civ_checker_list = open('/haydn/felixm-h/civ_checker.list')
                        j = j.strip()
                        #print('splited item: ', j)

                        for line in civ_checker_list.readlines(): 
                            if (re.match(j, line)) :
                                hit_cov = hit_cov + 1
                                break
                    
                    if hit_cov == total_cov : find = 1

                else:
                    civ_checker_list = open('/haydn/felixm-h/civ_checker.list')
                    for line in civ_checker_list.readlines():
                        item = str(i.check_way)
                        #print('got line: ', line)
                        if (re.match(item, line)) :
                            #print('match item: ', item)
                            find = 1
                            break

                if(find):
                    i.check_way_exist = True
                else:
                    i.check_way_exist = False
                
                i.save()
                f.write(i.check_way + ' -> ' + str(i.check_way_exist) + ' ' + i.name + ' pk=' + str(i.pk) + '-> owner is ' + str(i.check_way_owner) + '\n')

#---------------------------------------------------------------------------------------                 
def cross_check_coverage(file):
    f = open(file, 'w')
    f.write('Cover sva name is: \n')

    #apic_features = CVerification.objects.filter(reviewer=get_object_or_404(User,pk=3))

    all_com = CComponent.objects.all()
    apic_com = get_object_or_404(CComponent,pk=10)

    for com in all_com:
        feature = com.cfeature_set.filter(component=com)
        vps = CVerification.objects.filter(pk=0)

        for i in feature:
            new = CVerification.objects.filter(feature=i)
            vps = chain(vps, new)

        for i in vps:
            #print('Find cover sva: ', i.coverage)
            #print('Class status : ', i.check_way_status)
            if i.coverage_status == CFeature.STATUS[-1][0] or i.coverage_status == CFeature.STATUS[-2][0]:

                find = 0

                item = str(i.coverage)
                item_pk = str(i.pk)
                #print('got line: ', line)
                if (re.search(',', item)) :
                    total_cov = 0
                    hit_cov = 0
                    #item.split('\s*,\s*')
                    #item.split(', ')
                    #item = item.split(' ')
                    item = item.replace(' ', '')
                    item = item.split(',')
                    #print('After split: ', item, '->', item_pk)

                    t = []

                    for j in item:
                        if(re.match('^\s*$', j)):
                            pass
                            #item.remove(j)
                            #print('Need delete -> ', j)
                        else:
                            t.append(j)

                    for j in t:
                        total_cov = total_cov + 1
                        civ_coverage_list = open('/haydn/felixm-h/civ_coverage.list')
                        j = j.strip()
                        #print('splited item: ', j)

                        for line in civ_coverage_list.readlines(): 
                            if (re.match(j, line)) :
                                hit_cov = hit_cov + 1
                                break
                    
                    if hit_cov == total_cov : find = 1

                else:
                    civ_coverage_list = open('/haydn/felixm-h/civ_coverage.list')
                    for line in civ_coverage_list.readlines(): 
                        #print('After split: ', item, dn)
                        if (re.match(item, line)) :
                            #print('match item: ', item)
                            find = 1
                            break

                if(find):
                    i.coverage_exist = True
                else:
                    i.coverage_exist = False
                
                i.save()
                f.write(i.coverage + ' -> ' + str(i.coverage_exist) + ' ' + i.name + ' pk=' + str(i.pk) + '-> owner is ' + str(i.coverage_owner) + '\n')
#---------------------------------------------------------------------------------------                 
def cross_check_stimulus(file, dual):
    f = open(file, 'w')
    f.write('Cover sva name is: \n')

    #apic_features = CVerification.objects.filter(reviewer=get_object_or_404(User,pk=3))

    all_com = CComponent.objects.all()
    apic_com = get_object_or_404(CComponent,pk=10)

    for com in all_com:
        feature = com.cfeature_set.filter(component=com)
        vps = CVerification.objects.filter(pk=0)

        owner = User.objects.get(id=8)
        #simon_vps = CVerification.objects.filter(stimulus_owner=owner)
        #simon_vps = CVerification.objects.filter(pk=218)

        for i in feature:
            new = CVerification.objects.filter(feature=i)
            vps = chain(vps, new)
        for i in vps:
        #for i in simon_vps:
            #print('Find cover sva: ', i.stimulus)
            #print('Class status : ', i.check_way_status)
            if i.stimulus_status == CFeature.STATUS[-1][0] or i.stimulus_status == CFeature.STATUS[-2][0]:

                find = 0

                if dual: item = str(i.stimulus_other)
                else: item = str(i.stimulus)
                #print('got line: ', line)
                if (re.search(',', item)) :
                    total_cov = 0
                    hit_cov = 0
                    #item.split('\s*,\s*')
                    #item.split(', ')
                    re.sub('\s*,\s*w_\w+', '', item)
                    re.sub('\s+', '', item)
                    item = item.replace(' ','')
                    item = item.strip()
                    item = item.split(',')
                    #print('After split: ', item)

                    t = []

                    for j in item:
                        if(re.match('^\s*w_', j)): 
                            pass
                            #item.remove(j)
                            #print('Need delete -> ', j)
                        elif(re.match('^\s*$', j)):
                            pass
                            #item.remove(j)
                            #print('Need delete -> ', j)
                        else:
                            t.append(j)

                    #print('After delete: ', t)

                    for j in t:
                        total_cov = total_cov + 1
                        civ_stimulus_list = open('/haydn/felixm-h/civ_stimulus.list')
                        j = j.strip()
                        #print('splited item: ', j)


                        for line in civ_stimulus_list.readlines(): 
                            if (re.match(j, line)) :
                                hit_cov = hit_cov + 1
                                break
                    
                    if hit_cov == total_cov : find = 1

                else:
                    civ_stimulus_list = open('/haydn/felixm-h/civ_stimulus.list')
                    for line in civ_stimulus_list.readlines(): 
                        #print('After split: ', item, dn)
                        if (re.match(item, line)) :
                            #print('match item: ', item)
                            find = 1
                            break

                if(find):
                    if dual: i.stimulus_other_exist = True
                    else: i.stimulus_exist = True
                else:
                    if dual: i.stimulus_other_exist = False
                    else: i.stimulus_exist = False
                
                i.save()
                #f.write(i.stimulus + ' -> ' + str(i.stimulus_exist) + ' ' + i.name + ' pk=' + str(i.pk) + '-> owner is ' + str(i.stimulus_owner) + '\n')

#---------------------------------------------------------------------------------------                 
def display_cross_check_result(request):

    all_points = CVerification.objects.all()

    owner_list = []
    #got all task owner
    for i in all_points:
        if i.owner not in owner_list: owner_list.append(i.owner)
        if i.coverage_owner not in owner_list: owner_list.append(i.coverage_owner)
        if i.stimulus_owner not in owner_list: owner_list.append(i.stimulus_owner)
        if i.check_way_owner not in owner_list: owner_list.append(i.check_way_owner)

    print('all owner is : ', owner_list)

    #user = get_object_or_404(User,pk=20)#BertChen
    #u = '%s' % user

    checker_check_result_set = []

    for owner in owner_list:
        check_ways = CVerification.objects.filter(check_way_owner=owner)
        
        total_cnt = 0
        miss_cnt = 0

        for i in check_ways:
            if i.check_way_status == CFeature.STATUS[-1][0] or i.check_way_status == CFeature.STATUS[-2][0]:
                #print(i, 'check_way_exist is: ', i.check_way_exist)
                total_cnt = total_cnt + 1
                if not i.check_way_exist:
                    miss_cnt = miss_cnt + 1
        
        if total_cnt == 0: miss_rate = 0
        else: miss_rate = round(miss_cnt*100/total_cnt)
        miss_rate = str(miss_rate)+ '%'

        checker_check_result_element = {'owner':owner, 'total_cnt':total_cnt, 'miss_cnt':miss_cnt, 'miss_rate':miss_rate, 'pk':owner.pk, 'type':'checker'}
        checker_check_result_set.append(checker_check_result_element)

        #print(owner, 'checker miss rate : ', miss_cnt, '/', total_cnt)

#---------------------------------------------------------------------------------------------
    coverage_check_result_set = []

    for owner in owner_list:
        coverages = CVerification.objects.filter(coverage_owner=owner)
        
        total_cnt = 0
        miss_cnt = 0

        for i in coverages:
            if i.coverage_status == CFeature.STATUS[-1][0] or i.coverage_status == CFeature.STATUS[-2][0]:
                #print(i, 'coverage_exist is: ', i.coverage_exist)
                total_cnt = total_cnt + 1
                if not i.coverage_exist:
                    miss_cnt = miss_cnt + 1
        
        if total_cnt == 0: miss_rate = 0
        else: miss_rate = round(miss_cnt*100/total_cnt)
        miss_rate = str(miss_rate)+ '%'

        coverage_check_result_element = {'owner':owner, 'total_cnt':total_cnt, 'miss_cnt':miss_cnt, 'miss_rate':miss_rate, 'pk':owner.pk, 'type':'coverage'}
        coverage_check_result_set.append(coverage_check_result_element)

        #print(owner, 'coverage miss rate : ', miss_cnt, '/', total_cnt)
#---------------------------------------------------------------------------------------------
    stimulus_check_result_set = []

    for owner in owner_list:
        stimuluss = CVerification.objects.filter(stimulus_owner=owner)
        
        total_cnt = 0
        miss_cnt = 0

        for i in stimuluss:
            if i.stimulus_status == CFeature.STATUS[-1][0] or i.stimulus_status == CFeature.STATUS[-2][0]:
                #print(i, 'stimulus_exist is: ', i.stimulus_exist)
                total_cnt = total_cnt + 1
                if not i.stimulus_exist:
                    miss_cnt = miss_cnt + 1
        
        if total_cnt == 0: miss_rate = 0
        else: miss_rate = round(miss_cnt*100/total_cnt)
        miss_rate = str(miss_rate)+ '%'

        stimulus_check_result_element = {'owner':owner, 'total_cnt':total_cnt, 'miss_cnt':miss_cnt, 'miss_rate':miss_rate, 'pk':owner.pk, 'type':'stimulus'}
        stimulus_check_result_set.append(stimulus_check_result_element)

        #print(owner, 'stimulus miss rate : ', miss_cnt, '/', total_cnt)
#---------------------------------------------------------------------------------------------
    stimulus_other_check_result_set = []

    for owner in owner_list:
        stimulus_others = CVerification.objects.filter(stimulus_owner=owner)
        
        total_cnt = 0
        miss_cnt = 0

        for i in stimulus_others:
            if i.stimulus_status == CFeature.STATUS[-1][0] or i.stimulus_status == CFeature.STATUS[-2][0]:
                #print(i, 'stimulus_other_exist is: ', i.stimulus_other_exist)
                total_cnt = total_cnt + 1
                if not i.stimulus_other_exist:
                    miss_cnt = miss_cnt + 1
        
        if total_cnt == 0: miss_rate = 0
        else: miss_rate = round(miss_cnt*100/total_cnt)
        miss_rate = str(miss_rate)+ '%'

        stimulus_other_check_result_element = {'owner':owner, 'total_cnt':total_cnt, 'miss_cnt':miss_cnt, 'miss_rate':miss_rate, 'pk':owner.pk, 'type':'stimulus_other'}
        stimulus_other_check_result_set.append(stimulus_other_check_result_element)

        #print(owner, 'stimulus_other miss rate : ', miss_cnt, '/', total_cnt)
#---------------------------------------------------------------------------------------------
    class_register_check_result_set = []

    for owner in owner_list:
        class_registers = CVerification.objects.filter(stimulus_owner=owner)
        
        total_cnt = 0
        miss_cnt = 0

        for i in class_registers:
            if i.stimulus_status == CFeature.STATUS[-1][0] or i.stimulus_status == CFeature.STATUS[-2][0]:
                #print(i, 'class_register_exist is: ', i.class_register_exist)
                total_cnt = total_cnt + 1
                if i.into_regression == CVerification.VRG_STATUS[0][0] and not (i.stimulus == 'NA' or i.stimulus == 'Cannot cover in civ' or re.search('\.(src|v)', i.stimulus)):
                    miss_cnt = miss_cnt + 1
        
        if total_cnt == 0: miss_rate = 0
        else: miss_rate = round(miss_cnt*100/total_cnt)
        miss_rate = str(miss_rate)+ '%'

        class_register_check_result_element = {'owner':owner, 'total_cnt':total_cnt, 'miss_cnt':miss_cnt, 'miss_rate':miss_rate, 'pk':owner.pk, 'type':'class_register'}
        class_register_check_result_set.append(class_register_check_result_element)

#---------------------------------------------------------------------------------------------
    header =  ['Owner', 'Total', 'Miss', 'Miss Rate']

    return render(request,'vp_web/cross_check.html',{
        'header':header,
        #'errornote':errornote,
        #'cleannote':cleannote,
        'checker_check_result_set':checker_check_result_set,
        'coverage_check_result_set':coverage_check_result_set,
        'stimulus_check_result_set':stimulus_check_result_set,
        'stimulus_other_check_result_set':stimulus_other_check_result_set,
        'class_register_check_result_set':class_register_check_result_set,
        })    
#---------------------------------------------------------------------------------------                 
def display_class_register_result(request):

    all_points = CVerification.objects.all()

    owner_list = []
    #got all task owner
    for i in all_points:
        if i.stimulus_owner not in owner_list: owner_list.append(i.stimulus_owner)

    #print('all owner is : ', owner_list)

    #---------------------------------------------------------------------------------------------
    class_register_check_result_set = []

    for owner in owner_list:
        class_registers = CVerification.objects.filter(stimulus_owner=owner)
        
        total_cnt = 0
        miss_cnt = 0

        for i in class_registers:
            if i.stimulus_status == CFeature.STATUS[-1][0] or i.stimulus_status == CFeature.STATUS[-2][0]:
                #print(i, 'class_register_exist is: ', i.class_register_exist)
                total_cnt = total_cnt + 1
                if i.into_regression == CVerification.VRG_STATUS[0][0] and not (i.stimulus == 'NA' or i.stimulus == 'Cannot cover in civ' or re.search('\.(src|v)', i.stimulus)):
                    miss_cnt = miss_cnt + 1
        
        if total_cnt == 0: miss_rate = 0
        else: miss_rate = round(miss_cnt*100/total_cnt)
        miss_rate = str(miss_rate)+ '%'

        class_register_check_result_element = {'owner':owner, 'total_cnt':total_cnt, 'miss_cnt':miss_cnt, 'miss_rate':miss_rate, 'pk':owner.pk, 'type':'class_register'}
        class_register_check_result_set.append(class_register_check_result_element)

    #---------------------------------------------------------------------------------------------
    header =  ['Owner', 'Total', 'Miss', 'Miss Rate']

    return render(request,'vp_web/register_status.html',{
        'header':header,
        #'errornote':errornote,
        #'cleannote':cleannote,
        'class_register_check_result_set':class_register_check_result_set,
        })    

#---------------------------------------------------------------------------------------                 
def cross_check_result_by_owner(request, pk, type):
    owner = get_object_or_404(User,pk=pk)
    u = '%s' % owner

    print('owner is:', u)
    
    num = 0
    set = []

    if(type == 'checker'):
        check_ways = CVerification.objects.filter(check_way_owner=owner)
        for i in check_ways:
            if i.check_way_status == CFeature.STATUS[-1][0] or i.check_way_status == CFeature.STATUS[-2][0]:
                #print(i, 'check_way_exist is: ', i.check_way_exist)
                if i.check_way_exist:
                    pass
                else:
                    num = num + 1
                    element = {'num':num ,'pk':i.pk, 'name':i.name, 'content':i.check_way}
                    #print('element :', element)
                    set.append(element)

    if(type == 'coverage'):
        coverages = CVerification.objects.filter(coverage_owner=owner)
        for i in coverages:
            if i.coverage_status == CFeature.STATUS[-1][0] or i.coverage_status == CFeature.STATUS[-2][0]:
                #print(i, 'coverage_exist is: ', i.coverage_exist)
                if i.coverage_exist:
                    pass
                else:
                    num = num + 1
                    element = {'num':num ,'pk':i.pk, 'name':i.name, 'content':i.coverage}
                    #print('element :', element)
                    set.append(element)

    if(type == 'stimulus'):
        stimuluss = CVerification.objects.filter(stimulus_owner=owner)
        for i in stimuluss:
            if i.stimulus_status == CFeature.STATUS[-1][0] or i.stimulus_status == CFeature.STATUS[-2][0]:
                #print(i, 'stimulus_exist is: ', i.stimulus_exist)
                if i.stimulus_exist:
                    pass
                else:
                    num = num + 1
                    element = {'num':num ,'pk':i.pk, 'name':i.name, 'content':i.stimulus}
                    #print('element :', element)
                    set.append(element)

    if(type == 'stimulus_other'):
        stimuluss = CVerification.objects.filter(stimulus_owner=owner)
        for i in stimuluss:
            if i.stimulus_status == CFeature.STATUS[-1][0] or i.stimulus_status == CFeature.STATUS[-2][0]:
                #print(i, 'stimulus_exist is: ', i.stimulus_exist)
                if i.stimulus_other_exist:
                    pass
                else:
                    num = num + 1
                    element = {'num':num ,'pk':i.pk, 'name':i.name, 'content':i.stimulus_other}
                    #print('element :', element)
                    set.append(element)

    if(type == 'class_register'):
        stimuluss = CVerification.objects.filter(stimulus_owner=owner)
        for i in stimuluss:
            if i.stimulus_status == CFeature.STATUS[-1][0] or i.stimulus_status == CFeature.STATUS[-2][0]:
                #print(i, 'stimulus_exist is: ', i.stimulus_exist)
                if i.into_regression == CVerification.VRG_STATUS[0][0] and not (i.stimulus == 'NA' or i.stimulus == 'Cannot cover in civ' or re.search('\.(src|v)', i.stimulus)):
                    num = num + 1
                    element = {'num':num ,'pk':i.pk, 'name':i.name, 'content':i.into_regression}
                    #print('element :', element)
                    set.append(element)

    header =  ['No', 'index', 'vp name', type + ' name']

    return render(request,'vp_web/cross_check_by_owner.html',{
        'owner':u,
        'type':type,
        'header':header,
        'set':set,
        })  
 
    
def modification_coverage():
    print('enter modification sub routine ')
    #user = get_object_or_404(User,pk=19)#Sharon, 19
    user = get_object_or_404(User,pk=21)
    #vps = CVerification.objects.filter(coverage_owner=user)
    vps = CVerification.objects.filter(pk=1350)
    for i in vps:
        c = i.coverage
    #    #re.sub('/', ',', i.check_way)
        c = c.replace('c_debug', 'c_fsbc_debug')
        #c = c.replace(',', ', ')
        #c = c.replace('(', '')
        #c = c.replace(')', '')
        i.coverage = c
        print('after modify: ', i.coverage)
        i.save()

def modification_stimulus():
    print('enter modification sub routine ')
    #user = get_object_or_404(User,pk=19)#Sharon, 19
    user = get_object_or_404(User,pk=8)
    vps = CVerification.objects.filter(stimulus_owner=user)
    for i in vps:
        c = i.stimulus
    #    #re.sub('/', ',', i.check_way)
        #if re.match('^\w+.\w+\s*, l2_', c):
        if re.match('^,', c):
            print('before modify: ', c)
            print('pk = ', i.pk)
            #c = c.replace('^\s*, l2', '^l2')
            #c = c.replace('sv.*', 'sv')
            c = re.sub('^\s*, l2', 'l2', c)
        #c = c.replace(',', ', ')
        #c = c.replace('(', '')
        #c = c.replace(')', '')
            i.stimulus = c
            print('after modify: ', i.stimulus)
            #i.save()

def modification_check_way():
    print('enter modification sub routine ')
    #user = get_object_or_404(User,pk=19)#Sharon, 19
    #user = get_object_or_404(User,pk=21)
    #vps = CVerification.objects.filter(check_way_owner=user)
    #vps = CVerification.objects.filter(pk=1349)
    l2_com = get_object_or_404(CComponent,pk=4)
    feature = l2_com.cfeature_set.filter(name__contains='l2_self_snoop')
    vps = CVerification.objects.filter(pk=0)
    for i in feature:
        new = CVerification.objects.filter(feature=i)
        vps = chain(vps, new)
    #vps = CVerification.objects.filter(feature__contains='l2_prefetch')
    for i in vps:
        c = i.check_way
        #c = c.replace('c_debug', 'c_fsbc_debug')
        #c = c.replace(';', ', ')
        #i.check_way = c
        #print('after modify: ', i.name)
        print('check way is: ', i.check_way)
        print('org owner: ', i.check_way_owner)
        owner = User.objects.get(id=8)
        i.check_way_owner = owner
        #print('change to: ', i.owner)
        print('change to: ', i.check_way_owner)
        #print('after modify: ', i.check_way)
        #i.save()

def modification_register():
    print('enter modification sub routine -- vrg register')
    #user = get_object_or_404(User,pk=19)#Sharon, 19
    user = get_object_or_404(User,pk=20)
    vps = CVerification.objects.filter(stimulus_owner=user)
    for i in vps:
        #print('before modify: ', c)
        if(i.stimulus == 'sys_interrupt.sv' and i.into_regression == CVerification.VRG_STATUS[0][0]):
            print('name : ', i.name)
            i.into_regression = CVerification.VRG_STATUS[1][0]
            print('after modify: ', i.into_regression)
            i.save()

def delete_item():
    print('enter modification sub routine ')
    #need_delete = CVerification.objects.filter(name__contains='')
    need_delete = CVerification.objects.filter(pk='608')
    #need_delete = CFeature.objects.filter(name__contains='xx')
    print('delete item: ', need_delete)
    for i in need_delete: print('pk = ', i.pk)
    #need_delete.delete()

def query_item():
    print('enter sub routine query')
    user = get_object_or_404(User,pk=9)
    #vps = CVerification.objects.filter(stimulus_owner=user)
    vps = CVerification.objects.filter(owner=user)
    for i in vps:
        if not i.feature_status == CFeature.STATUS[-1][0] and not i.feature_status == CFeature.STATUS[-2][0]: 
            print('not 100%: ', i.name, i.feature_status, i.pk)
            i.feature_status = CFeature.STATUS[-2][0]
            i.save()
            print('after modify: ', i.name, i.feature_status, i.pk)
#------------------------------------------------------------------------------
def coverage_trace(request):

    u = '%s' % request.user
    if u == "FelixMa" : 
        os.system('/ctwrk/users/felixm/vrg_web/release/vrg_site/gen_feature_tag_list.pl')
        os.system('/ctwrk/users/felixm/vrg_web/release/vrg_site/gen_randomed_feature_tag_list.pl')
        os.system('/ctwrk/users/felixm/vrg_web/release/vrg_site/check_class_covered.pl')

    set = []
    num = 0  

    c_vps = []
    out_vps = []

    #c_vps = CVerification.objects.filter(pk=0)
    all_vps = CVerification.objects.filter(pk=0)
        
    all_com = CComponent.objects.all()

    for com in all_com:
        feature = com.cfeature_set.filter(component=com)
        for i in feature:
            new = CVerification.objects.filter(feature=i)
            all_vps = chain(all_vps, new)
    #all_vp = CVerification.objects.all()
    for j in all_vps:
        c = j.coverage
        if (re.search(',', c)) :
    #        c_vps = chain(c_vps, j)
            c_vps.append(j)

    #print('c_vps is: ', c_vps)

    #for i in c_vps:
    #    cs = i.coverage
    #    print('cs is: ', cs)

    unexisted_coverage_list = []
    status_list = []
    vps = CVerification.objects.filter(pk=0)
    num = 0
    cnt = 0

    coverage_result = open('/haydn/felixm-h/cov_feature/cov_feature_a0.rpt')
    for line in coverage_result.readlines(): 
        if (re.search('%', line)):
            cnt = cnt + 1
            m = re.match('\s*(\w+)\s+(\S+)\s+(\S+)', line)
            #print('m1 is: ', m.group(1))
            #print('m2 is: ', m.group(2))
            #print('m3 is: ', m.group(3))
            status_element = {'num':cnt, 'module':m.group(1), 'coverage':m.group(2), 'status':m.group(3), }
            status_list.append(status_element)

        elif (re.search('date:', line)):
            date = line
        elif (re.search('->\s+0', line)):
            #print('not coveraged: ', line)
            m = re.match('\s*(\w+)\s+->', line)
            #print('m1 is: ', m.group(1))
            coverage_name = m.group(1)
            vp = CVerification.objects.filter(coverage=coverage_name)

            if(vp):
                #print('vp is: ', vp)
                vps = chain(vps, vp)
                for i in vp:
                    new = i
                vp = new    
                num = num + 1

                #check whether stimulus is randomed in VRG
                update_stimulus_covered_status(vp)

                info_element = {'coverage_name':coverage_name, 'vp':vp}
                set.append(info_element)
                
                
            else:
                #print('vp not found: ', vp)

#-----------------------------------------------------------------------------
                has_added = 0
                for i in c_vps:
                    find = 0
                    cs = i.coverage
                    cs = cs.split(',')

                    for j in cs:
                        j = j.strip()
                        if(re.match(coverage_name, j)):
                            #print('found j: ', j)
                            find = 1
                            break

                    if find:
                        update_stimulus_covered_status(i)
                        matched_vp = CVerification.objects.filter(pk=i.pk)
                        vps = chain(vps, matched_vp)
                        has_added = 1

                        for m in matched_vp:
                            vp = m
                        info_element = {'coverage_name':coverage_name, 'vp':vp}
                        set.append(info_element)
                        break

#-----------------------------------------------------------------------------
                if has_added == 0:
                    num = num + 1
                    element = {'num':num, 'coverage_name':coverage_name}
                    unexisted_coverage_list.append(element)

    status_header =  ['No', 'module', 'coverage', 'status']
    header =  ['No', 'cover sva name']
    
    #------------------------------------------------------------------------------
    return render( request, 'vp_web/coverage_trace.html',{
        'publish_date':date,
        'features':vps,
        'set':set,
        'header':header,
        'unexisted_coverage_list':unexisted_coverage_list,
        'status_header':status_header,
        'status_list':status_list,
        }
    )

#------------------------------------------------------------------------------
def coverage_count(request):
    c_vps = []

    all_vps = CVerification.objects.filter(pk=0)
        
    all_com = CComponent.objects.all()

    for com in all_com:
        feature = com.cfeature_set.filter(component=com)
        for i in feature:
            new = CVerification.objects.filter(feature=i)
            all_vps = chain(all_vps, new)

    for j in all_vps:
        c = j.coverage
        if (re.search(',', c)) :
            c_vps.append(j)

    vps = CVerification.objects.filter(pk=0)

    coverage_result = open('/haydn/felixm-h/cov_feature/cov_feature_a0.rpt')
    for line in coverage_result.readlines():    
        if (re.search('->\s+(\d+)', line)):
            #print('not coveraged: ', line)
            m = re.match('\s*(\w+)\s+->\s+(\d+)', line)
            #print('m1 is: ', m.group(1))
            coverage_name = m.group(1)
            cover_count = m.group(2)
            if cover_count != 0:
                vp = CVerification.objects.filter(coverage=coverage_name)
                if(vp):
                    for i in vp:
                        i.vp_cover_count = cover_count
                        i.save()
                    #print('cover count is: ', vp.vp_cover_count) 
                    vps = chain(vps, vp)
                else:
                    for i in c_vps:
                        find = 0
                        cs = i.coverage
                        cs = cs.split(',')

                        for j in cs:
                            j = j.strip()
                            if(re.match(coverage_name, j)):
                                #print('found j: ', j)
                                find = 1
                                break

                        if find:
                            matched_vp = CVerification.objects.filter(pk=i.pk)
                            for u in matched_vp:
                                u.vp_cover_count = cover_count
                                u.save()
                            vps = chain(vps, matched_vp)
                            break

    return render( request, 'vp_web/coverage_count.html',{
        'features':vps,
        }
    )
#----------------------------------------------------------------------------------
def update_stimulus_covered_status(vp):
    stimulus_covered = 0
    vp_feature_tag = vp.feature_tag
    vp_feature_tag = vp_feature_tag.strip()
    vp_stimulus = vp.stimulus
    vp_stimulus = vp_stimulus.strip()

    randomed_feature_tag = open('/haydn/felixm-h/randomed_feature_tag.list')
    for line in randomed_feature_tag.readlines(): 
        line = line.strip()
        if vp_feature_tag == line:
            stimulus_covered = 1
            break
            
    if stimulus_covered == 0:
        covered_class = open('/haydn/felixm-h/covered_class.list')
        for line in covered_class.readlines(): 
            line = line.strip()
            if vp_stimulus == line:
                stimulus_covered = 1
                break

    if(stimulus_covered): 
        vp.stimulus_covered_status = CVerification.COVER_STATUS[-1][0]
        vp.stimulus_covered = True
    else:
        vp.stimulus_covered_status = CVerification.COVER_STATUS[0][0]
        vp.stimulus_covered = False

    vp.save()

def vrg_app(request):
    return HttpResponseRedirect('http://ct1510:15900/vrg_app/')

def lint_app(request):
    return HttpResponseRedirect('http://ct1510:15800/lint_app/')

def signoff_app(request):
    return HttpResponseRedirect('http://ct1510:15800/signoff_app/')

def gazer(request):
    return render(request,'vp_web/gazer.html', {})

def about(request):
    return render(request,'vp_web/about.html',{})


