from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.cache import never_cache
from django.utils.translation import ugettext as _, ugettext_lazy
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.shortcuts import render,get_object_or_404
from django.utils.html import format_html
import socket,datetime
from django.contrib.auth.models import User
import re
from .models import TBaseItem, TOwnerCase, TPathGroup, TCheckCase
import os

def index(request):

    #list all partion
    #partition_set = ['full_chip','processor_only','core_cluster','hif_only','fsl_only',]
    partition_set = ['processor_only']
    signoff_mode_set = ['normal', 'afs', 'atpg',]
    #signoff_mode_set = ['afs']
    check_mode_set = ['setup', 'hold']
    #partition_set = ['fsl_only']
    #partition_set = ['core_only','processor_only']

    #others = TPathGroup.objects.all()
    #others = TPathGroup.objects.filter(partition='fsl_only')
    #print ('others is : ',others)

    dict_fast = { #need update
            'hold_ff0p65v0c_cbest_ccbest' : 'fast',
            'hold_ff0p65v0c_cworst_ccworst' : 'non_fast',
            }

    #
    display_set = []

    #header = ['Parition', 'corner', 'fn', 'check_mode', 'setup wns', 'setup tns', 'setup nvp', 'hold wns', 'hold tns', 'hold nvp', 'add time', 'database_version']
    header = ['Parition', 'corner', 'check mode', 'setup wns', 'setup tns', 'setup nvp', 'hold wns', 'hold tns', 'hold nvp', 'summit time', 'database version']

    for p in partition_set:
        
        #find all corner of this partition
        #others = TOwnerCase.objects.filter(partition=p)
        #if others:
        #    pass
        #else:
        others = TPathGroup.objects.filter(partition=p).order_by('id')

        #if this partition object not exit, continue
        if not others:
            element = {'partition':p, 'corner':'null', 'setup_wns':'null', 'setup_tns':'null', 'setup_nvp':'null', 'hold_wns':'null', 'hold_tns':'null', 'hold_nvp':'null', 'summit_time':'null'}
            display_set.append(element) 
            continue

        #Got corner set
        #print ('Group case is : ',others)
        corner_set = []
        i = 0
        #while others:
        while i != 100:
            item_last = others.last()
            item_last_corner = item_last.corner
            #print ('item_last_corner is : ',item_last_corner)
            
            corner_set.append(item_last_corner)
            others = others.exclude(corner=item_last_corner)
            if not others: break
            i = i + 1      

        #print ('corner set is : ',corner_set)

        i = 0
        for sm in signoff_mode_set:
            i = i + 1
            #print ('p is : ',p)
            #print ('c is : ',c)

            for cm in check_mode_set:
                for c in corner_set:
                    #print ('cm is : ',cm)

                    item0 = TPathGroup.objects.filter(partition=p, corner=c, check_mode=cm, signoff_mode=sm).last()
                    
                    if item0:
                        pass
                    else:
                        item0 = TOwnerCase.objects.filter(partition=p, corner=c, check_mode=cm, signoff_mode=sm).last()
                    
                    if item0:
                        pass
                    else:
                        #print('item0 not exit')
                        continue


                    try:
                        signoff_mode = item0.signoff_mode
                    except:
                        signoff_mode = 'xxnull'

                    try:
                        check_mode = item0.check_mode
                    except:
                        check_mode = 'xxnull'

                    try:
                        summit_time = item0.summit_time
                    except:
                        summit_time = 'xxnull'

                    if item0.setup_wns != 'null':
                        setup_wns = item0.setup_wns
                        setup_tns = item0.setup_tns
                        setup_nvp = item0.setup_nvp
                    else:
                        setup_wns = 'xxnull'
                        setup_tns = 'xxnull'
                        setup_nvp = 'xxnull'

                    if item0.hold_wns != 'null':
                        hold_wns = item0.hold_wns
                        hold_tns = item0.hold_tns
                        hold_nvp = item0.hold_nvp
                        #print ('item0 setup wns is : ',item0.setup_wns)
                    else:
                        hold_wns  = 'xxnull'
                        hold_tns  = 'xxnull'
                        hold_nvp  = 'xxnull'
                    
                    try:
                        database_version = item0.database_version
                    except:
                        database_version = '-'

                    #gen fast/non-fast
                    try:
                        key = str(check_mode) + '_' + str(c)
                        fn = dict_fast[key]
                        #print('corner is ', str(c))
                        #print('got fn is ', fn)
                    except:
                        fn = '-'
                    
                    element = {'partition':p, 'signoff_mode':signoff_mode, 'check_mode':check_mode, 'corner':c, 'setup_wns':setup_wns, 'setup_tns':setup_tns, 'setup_nvp':setup_nvp, 'hold_wns':hold_wns, 'hold_tns':hold_tns, 'hold_nvp':hold_nvp, 'summit_time':summit_time, 'database_version':database_version, 'fn':fn}
                    display_set.append(element) 


    #delete
    #this_stage = 'FSO'
    this_stage = 'R0'
    #this_corner = 'ss0p9v125c_cworst_CCworst_T'
    this_corner = 'tt1p0v100c'
    #this_partition = 'full_chip'
    this_partition = 'processor_only'
    #this_signoff_mode = 'afs'
    this_signoff_mode = 'normal'
    #ownercase_delete = TOwnerCase.objects.filter(check_item='signoff_timing', partition=this_partition, corner=this_corner, stage=this_stage)
    #ownercase_delete = TOwnerCase.objects.filter(check_item='signoff_timing', partition=this_partition, corner=this_corner)
    #ownercase_delete = TOwnerCase.objects.filter(stage=this_partition)
    #for i in ownercase_delete: 
    #    i.check_mode = 'setup'
    #    i.save()
    #    print ('ownercase_delete is: ', i)
    #    i.delete()
    #pathgroup_delete = TPathGroup.objects.filter(check_item='signoff_timing', corner=this_corner, partition=this_partition, stage=this_stage, signoff_mode=this_signoff_mode)
    #pathgroup_delete = TPathGroup.objects.filter(check_item='signoff_timing', partition=this_partition, stage=this_stage)
    #pathgroup_delete = TPathGroup.objects.filter(check_item='signoff_timing', stage=this_stage)
    #pathgroup_delete = TPathGroup.objects.filter(partition=this_partition)
    #for i in pathgroup_delete: 
    #    i.check_mode = 'setup'
    #    i.save()
    #    print ('pathgroup_delete is: ', i)
    #    i.delete()

    #debug_log = open('/haydn/felixm-h/signoff_check_debug.log', 'w')
    #for i in pathgroup_delete:
    #    debug_log.writelines('i corner is ' + i.corner + ' check mode is ' + i.check_mode + ' stage is ' + i.stage + '\n')
    #debug_log.writelines('x')
    #debug_log.close()

    #pathgroup_last = TPathGroup.objects.last()
    #pathgroup_first = TPathGroup.objects.first()
    #print ('check mode of pathgroup_last is: ', pathgroup_last.signoff_mode)
    #print ('check mode of pathgroup_first is: ', pathgroup_first.signoff_mode)
    
    #print ('check_item='+item.check_item +'partition='+item.partition+'corner='+item.corner+'stage='+item.stage+ 'check_mode='+item.check_mode+ 'signoff_mode='+item.signoff_mode)

    
    
    #return render(request,'signoff_check/test.html',{
    return render(request,'signoff_check/index.html',{
        'header':header,
        'display_set':display_set,
        'corner_set':corner_set,
        'partition_set':partition_set,
        'signoff_mode_set':signoff_mode_set,
        }) 

def parition_status(request, partition, corner, signoff_mode, check_mode):
    
    #if partition == 'processor_only':
    #    this_stage = 'R1'
    #else:
    #    this_stage = 'R0'
    #this_stage = 'FSO'
    this_corner= corner

    ownercase_all = TOwnerCase.objects.filter(check_item='signoff_timing', partition=partition, corner=this_corner, signoff_mode=signoff_mode, check_mode=check_mode)
    ownercase_last = ownercase_all.last()

    ownercase_all_setup = TOwnerCase.objects.filter(check_item='signoff_timing', partition=partition, corner=this_corner, signoff_mode=signoff_mode, check_mode=check_mode, type='setup')
    ownercase_all_hold = TOwnerCase.objects.filter(check_item='signoff_timing', partition=partition, corner=this_corner, signoff_mode=signoff_mode, check_mode=check_mode, type='hold')

    pathgroup_all = TPathGroup.objects.all()
    pathgroup_all_setup = TPathGroup.objects.filter(check_item='signoff_timing', partition=partition, corner=this_corner, signoff_mode=signoff_mode, check_mode=check_mode, type='setup')
    pathgroup_all_hold  = TPathGroup.objects.filter(check_item='signoff_timing', partition=partition, corner=this_corner, signoff_mode=signoff_mode, check_mode=check_mode, type='hold')
    if pathgroup_all_setup.last() :
        pathgroup_last = pathgroup_all_setup.last()
    else :
        pathgroup_last = pathgroup_all_hold.last()
    #print ('pathgroup_all_setup is : ',pathgroup_all_setup)

    ownercase_header =  ['Owner','WNS','TNS','NVP']
    path_group_header =  ['Path_group','WNS','TNS','NVP']

    signoff_timing_fieldsets = [
            {
            'name'  : 'Signoff PT database info',
            'editable' : False,
            'fields': ['project','partition','corner','check_mode','signoff_mode','setup_nvp','hold_nvp','database_version','summit_time'],
                }
            ]
    
    get_fields(pathgroup_last,signoff_timing_fieldsets)  

    errornote = "no info in Signoff Web database"
    cleannote = "no timing violation error"

    #-------------------------------------------------------------------------------------
    if "_delete" in request.POST:
        try:
            u = str(request.user)
            #if u == "JacobHuang":
            if True :
                for i in ownercase_all_setup: i.delete()
                for i in ownercase_all_hold: i.delete()
                for i in pathgroup_all_setup: i.delete()
                for i in pathgroup_all_hold: i.delete()
            else:
                print('Sorry, you cant delete')
            #item.save()
            return HttpResponseRedirect(reverse('signoff_check:index',args = ()))
        except Exception as e:    
            errornote = str(e)+"debug"
    #-------------------------------------------------------------------------------------

    return render(request,'signoff_check/partition_status.html',{
        'title':'',
        'ownercase_item':pathgroup_last,
        'signoff_timing_infos':signoff_timing_fieldsets,
        'errornote':errornote,
        'cleannote':cleannote,
        'partition':partition,
        #ownercase
        'ownercase_all':ownercase_all,
        'ownercase_header':ownercase_header,
        'ownercase_all_setup':ownercase_all_setup,
        'ownercase_all_hold':ownercase_all_hold,
        #pathgroup
        'path_group_header':path_group_header,
        'pathgroup_all_setup':pathgroup_all_setup,
        'pathgroup_all_hold':pathgroup_all_hold,
        })
#---------------------------------------------------------------------------------
def index_org(request):
    #return HttpResponse('hello tracking')
    #summary = OwnerCase.objects.filter(owner="Felix")
    #item = get_object_or_404(OwnerCase, pk=2)
    #last = OwnerCase.objects.last()
    #first = OwnerCase.objects.first()
    #all = OwnerCase.objects.all()
    
    this_stage = 'R0'

    ownercase_all = TOwnerCase.objects.filter(check_item='signoff_timing', partition='processor', stage=this_stage)
    ownercase_last = ownercase_all.last()

    ownercase_all_setup = TOwnerCase.objects.filter(check_item='signoff_timing', partition='processor', stage=this_stage, type='setup')
    ownercase_all_hold = TOwnerCase.objects.filter(check_item='signoff_timing', partition='processor', stage=this_stage, type='hold')

    pathgroup_all = TPathGroup.objects.all()
    pathgroup_all_setup = TPathGroup.objects.filter(check_item='signoff_timing', partition='processor', stage=this_stage, type='setup')
    pathgroup_all_hold  = TPathGroup.objects.filter(check_item='signoff_timing', partition='processor', stage=this_stage, type='hold')
    #print ('pathgroup_all_setup is : ',pathgroup_all_setup)

    #pathgroup_last = pathgroup_all.last()
    #check_lint_first = check_lint_all.first()
    
    #all = all.order_by('owner')

    #if(first.owner == 'null'):
    #    all=  list(filter(lambda item:(item.id!=1),OwnerCase.objects.all()))

    #all = OwnerCase.objects.order_by('owner')
    #print (ownercase_all)
    #print (pathgroup_all)
    
   # print ('new',new)
    
    #owner_set = list(map(lambda a:a.owner, all))
    #fail_num_set = list(map(lambda a:a.fail_number, all))
    #for o in owner_set: print(o)
        
    ownercase_header =  ['Owner','vio_type','WNS','TNS','NVP']
    #path_group_header =  ['Path_group','WNS','TNS','NVP','FREQ','WNS(H)','TNS(H)','NVP(H)']
    path_group_header =  ['Path_group','vio_type','WNS','TNS','NVP']
    #path_group_header =  ['Path_group','WNS','TNS','NVP','WNS(H)','TNS(H)','NVP(H)']

    signoff_timing_fieldsets = [
            {
            'name'  : 'Signoff PT database info',
            'editable' : False,
            'fields': ['project','partition','vio_total_number','corner','database_version','database_date','summit_time'],
                }
            ]
    
    get_fields(ownercase_last,signoff_timing_fieldsets)  

    #-------------------------------------------------------------------------------------
    vclp_all = TOwnerCase.objects.filter(check_item='signoff_power', partition='processor')
    #vclp_all = TOwnerCase.objects.filter(owner='vclp felix', partition='processor')
    vclp_last = vclp_all.last()
    #print('vclp all is : ', vclp_all)

    vclp_header =  ['Owner','vio_type','WNS','TNS','NVP']

    signoff_power_fieldsets = [
            {
            'name'  : 'Signoff VCLP database info',
            'editable' : False,
            'fields': ['project','partition','vio_total_number','corner','database_version','database_date','summit_time'],
                }
            ]
    
    get_fields(vclp_last,signoff_power_fieldsets)  

    #-------------------------------------------------------------------------------------
    tree_header =  ['No', 'Severity','Stage','Tag','Count','Waived']

    f = open(vclp_last.log)
    tree_summary = []
    num = 0

    for line in f.readlines():
        if (re.match('\s+(error|warning)', line)) :
            m = re.match('\s+(error|warning)\s+(\w+)\s+(\w+)\s+(\d+)\s+(\d+)', line)
            num = num + 1
            element = {'severity':m.group(1), 'stage':m.group(2), 'tag':m.group(3), 'count':m.group(4), 'waived':m.group(5), 'pk':num}
            tree_summary.append(element)
            #print('got error/warining line: ', line)


    #print(tree_summary)
    
    #-------------------------------------------------------------------------------------

    errornote = "no info in Signoff Web database"
    cleannote = "no timing violation error"

    return render(request,'signoff_check/index_org.html',{
        'title':'',
        'ownercase_item':ownercase_last,
        'signoff_timing_infos':signoff_timing_fieldsets,
        'errornote':errornote,
        'cleannote':cleannote,
        #ownercase
        'ownercase_all':ownercase_all,
        'ownercase_header':ownercase_header,
        'ownercase_all_setup':ownercase_all_setup,
        'ownercase_all_hold':ownercase_all_hold,
        #pathgroup
        'path_group_header':path_group_header,
        'pathgroup_all_setup':pathgroup_all_setup,
        'pathgroup_all_hold':pathgroup_all_hold,
        #tree_summary
        #'signoff_power_infos':signoff_power_fieldsets,
        #'tree_header':tree_header,
        #'tree_summary':tree_summary,
        })

#------------------------------------------------------------------------------------------------
def another_stage(request):
    
    this_stage = 'R1'

    ownercase_all = TOwnerCase.objects.filter(check_item='signoff_timing', partition='processor', stage=this_stage)
    ownercase_last = ownercase_all.last()

    ownercase_all_setup = TOwnerCase.objects.filter(check_item='signoff_timing', partition='processor', stage=this_stage, type='setup')
    ownercase_all_hold = TOwnerCase.objects.filter(check_item='signoff_timing', partition='processor', stage=this_stage, type='hold')

    pathgroup_all = TPathGroup.objects.all()
    pathgroup_all_setup = TPathGroup.objects.filter(check_item='signoff_timing', partition='processor', stage=this_stage, type='setup')
    pathgroup_all_hold  = TPathGroup.objects.filter(check_item='signoff_timing', partition='processor', stage=this_stage, type='hold')
    print ('pathgroup_all_setup is : ',pathgroup_all_setup)


    ownercase_header =  ['Owner','vio_type','WNS','TNS','NVP']
    #path_group_header =  ['Path_group','WNS','TNS','NVP','FREQ','WNS(H)','TNS(H)','NVP(H)']
    path_group_header =  ['Path_group','vio_type','WNS','TNS','NVP']
    #path_group_header =  ['Path_group','WNS','TNS','NVP','WNS(H)','TNS(H)','NVP(H)']

    signoff_timing_fieldsets = [
            {
            'name'  : 'Signoff PT database info',
            'editable' : False,
            'fields': ['project','partition','vio_total_number','corner','database_version','database_date','summit_time'],
                }
            ]
    
    get_fields(ownercase_last,signoff_timing_fieldsets)  


    #-------------------------------------------------------------------------------------

    errornote = "no info in Signoff Web database"
    cleannote = "no timing violation error"

    return render(request,'signoff_check/another_stage.html',{
        'title':'',
        'ownercase_item':ownercase_last,
        'signoff_timing_infos':signoff_timing_fieldsets,
        'errornote':errornote,
        'cleannote':cleannote,
        #ownercase
        'ownercase_all':ownercase_all,
        'ownercase_header':ownercase_header,
        'ownercase_all_setup':ownercase_all_setup,
        'ownercase_all_hold':ownercase_all_hold,
        #pathgroup
        'path_group_header':path_group_header,
        'pathgroup_all_setup':pathgroup_all_setup,
        'pathgroup_all_hold':pathgroup_all_hold,
        })
#--------------------------------------------------------------------------------
def owner(request,pk):
    item = get_object_or_404(TOwnerCase,pk=pk)
    item_pk = pk
    errornote = ""

    f = open(item.log_path)
    c = []
    error_set = []
    num = 1
    
    if (item.check_item == 'signoff_timing'):
        for line in f.readlines():
            if (re.match('\s+Startpoint:', line)) :
                #print('got start point line %s', line)
                m = re.match('\s+Startpoint:\s+(.*)', line)
                #print('m is: ', m.groups())
                start_point = m.group(0)
                #print('got start point ', start_point)

            elif (re.match('\s+Endpoint:', line)) :
                m = re.match('\s+Endpoint:\s+(.*)', line)
                end_point = m.group(0)

            elif (re.match('\s+slack \(VIOLATED\)', line)) :
                m = re.match('\s+slack \(VIOLATED\)\s+(.*)', line)
                slack = m.group(1)

                l = 'line number'+str(num)+line 
                c.append(l)
                error_element = {'num':num, 'start_point':start_point, 'end_point':end_point, 'slack':slack, 'pk':item_pk}
                #print('got error element', error_element)
                error_set.append(error_element)
                num = num + 1

            elif (re.match('\s+\((Path is unconstrained)\)', line)) :
                slack = 'Path is unconstrained'

                l = 'line number'+str(num)+line 
                c.append(l)
                error_element = {'num':num, 'start_point':start_point, 'end_point':end_point, 'slack':slack, 'pk':item_pk}
                #print('got error element', error_element)
                error_set.append(error_element)
                num = num + 1

            else:
                #print('not find Error match in %s', line)
                pass
        
    #print('c is %s', c)
    #item.content = "\n".join(c)
    item.content = c
    
    #print('error_set is %s', error_set)

    header =  ['No', 'Start point', 'End point', 'Slack']

    fieldsets = [
            {
            'name'  : 'Summary',
            'editable' : False,
            'fields': ['vio_number','log_path'],
                }
            ]
    get_fields(item,fieldsets)  

    return render(request,'signoff_check/owner.html',{
        'title':item.owner+"'s "+item.type+" violation",
        'infos':fieldsets,
        'errornote':errornote,
        'error_set':error_set,
        'header':header,
        'ownercase':item,
        })

#--------------------------------------------------------------------------------
def path(request,pk,path_id):
    item = get_object_or_404(TOwnerCase,pk=pk)
    errornote = ""

    #print('display log_path', item.log_path)
    f = open(item.log_path)
    selected_path = []
    p = ''
    num = 0
    i = str(path_id)

    #print('debug: path_id= ', path_id)
    #if (item.check_item == 'signoff_timing'):
    for line in f.readlines():
        #print('debug: num = ', num)
        if (re.match('\s+Startpoint:', line)) :
            num = num + 1
            if(str(num) == i):
                selected_path.append(line)
                p = p+line
            #else:
            #    print('debug: not match= ', num, path_id, i)
            #print('got start point line ', line)
            #print('after got: display path', selected_path)

        elif (re.match('\s+slack \(VIOLATED\)', line) or re.match('\s+\((Path is unconstrained)\)', line)) :
            if(str(num) == i):
                selected_path.append(line)
                p = p+line
                break
        elif (str(num) == i) :
            selected_path.append(line)
            #p = p+str(line)+'\n'
            p = p+line
            #print('got content line: ', str(line))
        else:
            #print('not find Error match in %s', line)
            pass

    header =  ['Timing Path']
    
    #print('display path', selected_path)

    return render(request,'signoff_check/selected_path.html',{
        'title':item.owner+"'s "+item.type+" violation: path "+path_id,
        'errornote':errornote,
        'selected_path':selected_path,
        'header':header,
        'p':p,
        })
#--------------------------------------------------------------------------------
def group(request,pk):
    item = get_object_or_404(TPathGroup,pk=pk)
    item_pk = pk
    errornote = ""

    f = open(item.log_path)
    c = []
    error_set = []
    num = 1
    
    if (item.check_item == 'signoff_timing'):
        for line in f.readlines():
            if (re.match('\s+Startpoint:', line)) :
                #print('got start point line %s', line)
                m = re.match('\s+Startpoint:\s+(.*)', line)
                #print('m is: ', m.groups())
                start_point = m.group(0)
                #print('got start point ', start_point)

            elif (re.match('\s+Endpoint:', line)) :
                m = re.match('\s+Endpoint:\s+(.*)', line)
                end_point = m.group(0)

            elif (re.match('\s+slack \(VIOLATED\)', line)) :
                m = re.match('\s+slack \(VIOLATED\)\s+(.*)', line)
                slack = m.group(1)

                l = 'line number'+str(num)+line 
                c.append(l)
                error_element = {'num':num, 'start_point':start_point, 'end_point':end_point, 'slack':slack, 'pk':item_pk}
                #print('got error element', error_element)
                error_set.append(error_element)
                num = num + 1

            elif (re.match('\s+\((Path is unconstrained)\)', line)) :
                slack = 'Path is unconstrained'

                l = 'line number'+str(num)+line 
                c.append(l)
                error_element = {'num':num, 'start_point':start_point, 'end_point':end_point, 'slack':slack, 'pk':item_pk}
                #print('got error element', error_element)
                error_set.append(error_element)
                num = num + 1

            else:
                #print('not find Error match in %s', line)
                pass
        
    #print('c is %s', c)
    #item.content = "\n".join(c)
    item.content = c
    
    #print('error_set is %s', error_set)

    header =  ['No', 'Start point', 'End point', 'Slack']

    fieldsets = [
            {
            'name'  : 'Summary',
            'editable' : False,
            'fields': ['nvp','log_path'],
                }
            ]
    get_fields(item,fieldsets)  

    return render(request,'signoff_check/group.html',{
        'title':item.group +"'s "+item.type+" violation",
        'infos':fieldsets,
        'errornote':errornote,
        'error_set':error_set,
        'header':header,
        })

#--------------------------------------------------------------------------------
def group_path(request,pk,path_id):
    item = get_object_or_404(TPathGroup,pk=pk)
    errornote = ""

    #print('display log_path', item.log_path)
    f = open(item.log_path)
    selected_path = []
    p = ''
    num = 0
    i = str(path_id)

    #print('debug: path_id= ', path_id)
    #if (item.check_item == 'signoff_timing'):
    for line in f.readlines():
        #print('debug: num = ', num)
        if (re.match('\s+Startpoint:', line)) :
            num = num + 1
            if(str(num) == i):
                selected_path.append(line)
                p = p+line
            #else:
            #    print('debug: not match= ', num, path_id, i)
            #print('got start point line ', line)
            #print('after got: display path', selected_path)

        elif (re.match('\s+slack \(VIOLATED\)', line) or re.match('\s+\((Path is unconstrained)\)', line)) :
            if(str(num) == i):
                selected_path.append(line)
                p = p+line
                break
        elif (str(num) == i) :
            selected_path.append(line)
            #p = p+str(line)+'\n'
            p = p+line
            #print('got content line: ', str(line))
        else:
            #print('not find Error match in %s', line)
            pass

    header =  ['Timing Path']
    
    #print('display path', selected_path)

    return render(request,'signoff_check/selected_path.html',{
        'title':item.group +"'s "+item.type+" violation: path "+path_id,
        'errornote':errornote,
        'selected_path':selected_path,
        'header':header,
        'p':p,
        })

#--------------------------------------------------------------------------------
def vclp(request):
    #print(' all base is : ', TBaseItem.objects.all())
    #vclp_all = TBaseItem.objects.filter(check_item='signoff_power', partition='processor')
    #print(' all base is : ', TOwnerCase.objects.all())
    vclp_all = TOwnerCase.objects.filter(check_item='signoff_power', partition='processor')
    #vclp_all = TOwnerCase.objects.filter(owner='vclp felix', partition='processor')
    vclp_last = vclp_all.last()
    #print('vclp all is : ', vclp_all)

    vclp_header =  ['Owner','vio_type','WNS','TNS','NVP']

    signoff_power_fieldsets = [
            {
            'name'  : 'Signoff database info',
            'editable' : False,
            'fields': ['project','partition','vio_total_number','corner','database_version','database_date','summit_time'],
                }
            ]
    
    get_fields(vclp_last,signoff_power_fieldsets)  

    #-------------------------------------------------------------------------------------
    tree_header =  ['No', 'Severity','Stage','Tag','Count','Waived']

    f = open(vclp_last.log)
    tree_summary = []
    num = 0

    for line in f.readlines():
        if (re.match('\s+(error|warning)', line)) :
            m = re.match('\s+(error|warning)\s+(\w+)\s+(\w+)\s+(\d+)\s+(\d+)', line)
            num = num + 1
            element = {'severity':m.group(1), 'stage':m.group(2), 'tag':m.group(3), 'count':m.group(4), 'waived':m.group(5), 'pk':num}
            tree_summary.append(element)
            #print('got error/warining line: ', line)


    #print(tree_summary)
    
    #-------------------------------------------------------------------------------------
    errornote = "no info in Signoff Web database"
    cleannote = "no timing violation error"

    return render(request,'signoff_check/vclp.html',{
        'title':'',
        'vclp_item':vclp_last,
        'signoff_power_infos':signoff_power_fieldsets,
        'errornote':errornote,
        'cleannote':cleannote,
        #tree_summary
        'tree_header':tree_header,
        'tree_summary':tree_summary,
        })  

#--------------------------------------------------------------------------------
def tag(request, pk, vtag, check_item):
    vclp_all = TOwnerCase.objects.filter(check_item=check_item, partition='processor')
    vclp_last = vclp_all.last()
    f = open(vclp_last.log)

    report_list = []
    find = 0
    num = 0
    logicsink = 0
    description = 0
    #print('got tag:',vtag)
    for line in f.readlines():
        #if (re.match('\s+Tag\s+:'+vtag+'\s+', line)) :
        #if (re.search(vtag, line)) :
        if (re.match('\s+Tag\s+:\s+'+vtag, line)) :
            #print('match tag: ', vtag)
            find = 1
            num = num + 1
        elif find and (re.match('\s+Description\s+:', line)):
            m = re.match('\s+Description\s+:\s+(.*)', line)
            description = m.group(1)
            #print('match description: ', description)

        elif find and (re.match('\s+(LogicSink|Instance|AnalogPin)\s+:', line)):
            m = re.match('\s+(LogicSink|Instance|AnalogPin)\s+:\s+(.*)', line)
            #print('match location 0: ', m.group(0))
            #print('match location 1: ', m.group(1))
            #print('match location 2: ', m.group(2))
            location = m.group(2)

        elif find and (re.match('\s+--------', line)):
            find = 0
            element = {'num':num, 'Location':location, 'Description':description}
            report_list.append(element)

    report_header =  ['No', 'Location','Description']
    errornote = ""
    cleannote = ""

    return render(request,'signoff_check/tag.html',{
        'tag':vtag,
        'log':vclp_last.log,
        'errornote':errornote,
        'cleannote':cleannote,
        #tree_summary
        'report_header':report_header,
        'report_list':report_list,
        })  
    
        

#--------------------------------------------------------------------------------
def vclp_case(request, pk, vtag):
    vclp_all = TOwnerCase.objects.filter(check_item='signoff_power', partition='processor')
    vclp_last = vclp_all.last()
    f = open(vclp_last.log)

    report_list = []
    start = 0
    num = 0
    content = ''
    #print('pk: ', pk)
    #print('got tag:',vtag)

    for line in f.readlines():
        if (re.match('\s+Tag\s+:\s+'+vtag, line)) :
            #print('match tag: ', vtag)
            num = num + 1
            #print('num: ', num)
            if str(num) == pk:
                start = 1
                #print('got line: ', line)
        elif start and (re.match('\s+--------', line)):
            start = 0
            break

        if start:
            content = content + line
            #print('got content: ', content)

    errornote = ""
    cleannote = ""

    return render(request,'signoff_check/vclp_case.html',{
        'title':'Detail info',
        'tag':vtag,
        'log':vclp_last.log,
        'errornote':errornote,
        'cleannote':cleannote,
        #tree_summary
        'content':content,
        })  
    
        

#--------------------------------------------------------------------------------
def get_html_content(item,mydict,review):
    input_list = ['comment']

    #if mydict['name'] == 'comment' :
    #    content = '<textarea class="vLargeTextField" cols="40" id="id_{0}" maxlength="50" name="{0}" rows="10">{1}</textarea>'.format(mydict['name'],getattr(item,mydict['name']))

    if mydict['name'] in input_list:
        content = '<input class="vTextField" id="id_{0}" maxlength="80" align="left" name="{0}" type="text" value="{1}" required />'.format(mydict['name'],getattr(item,mydict['name']))
    else:
        #content = '<textarea class="vTextField" cols="40" id="id_{0}" maxlength="1000" name="{0}" rows="10">{1}</textarea>'.format(mydict['name'],getattr(item,mydict['name']))
        content = getattr(item,mydict['name'])

    mydict['content'] = format_html(content)
    

def get_content(item,name):
    if name == 'feature_status' or name == 'status' :
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
                line['fields'][i] = mydict

def other_check(request):
    #all_user = User.objects.all()
    #print ('all_user is: ', all_user)
    #for i in all_user:
    #    upk = i.pk
    #    print ('%s pk is %s', i, upk)

    #pathgroup_delete = TCheckCase.objects.all()
    #for i in pathgroup_delete: 
    #    if i.check_owner:
    #        print ('found field check_owner in ', i)
    #        i.check_owner = get_object_or_404(User,pk=3)
    #        i.save()
    #    else:
    #        print ('not found field check_owner in ', i)
    
    #    print ('pathgroup_delete is: ', i)
    #    i.delete()
    #list all partion
    #partition_set = ['full_chip','processor_only','core_cluster','hif_only','fsl_only',]
    partition_set = ['full_chip']
    signoff_mode_set = ['normal', 'afs', 'atpg',]
    #signoff_mode_set = ['afs']
    #check_item_set = ['analog_connection_check','tweeter_balance_check']
    #partition_set = ['fsl_only']
    #partition_set = ['core_only','processor_only']

    #others = TPathGroup.objects.all()
    #others = TPathGroup.objects.filter(partition='fsl_only')
    #print ('others is : ',others)

    #
    display_set = []

    header = ['partition', 'corner', 'type', 'status', 'add time', 'database_version', 'owner', 'comment']
    #header = ['Parition', 'corner']
    #for i in check_item_set:
    #    header.append(i)
    #header.append('add time')
    #header.append('database_version')
    

    for p in partition_set:
        
        #find all corner of this partition
        #others = TOwnerCase.objects.filter(partition=p)
        #if others:
        #    pass
        #else:
        others = TCheckCase.objects.filter(partition=p)

        #if this partition object not exit, continue
        print ('partition is : ',p)
        if not others:
            element = {'partition':p, 'corner':'null', 'check':'null', 'summit_time':'null'}
            display_set.append(element) 
            continue

        #Got corner set
        #print ('Group case is : ',others)
        corner_set = []
        i = 0
        #while others:
        while i != 100:
            item_last = others.last()
            item_last_corner = item_last.corner
            #print ('item_last_corner is : ',item_last_corner)
            
            corner_set.append(item_last_corner)
            others = others.exclude(corner=item_last_corner)
            if not others: break
            i = i + 1      

        #print ('corner set is : ',corner_set)

        #Got check set
        others = TCheckCase.objects.filter(partition=p)
        #print ('Group case is : ',others)
        check_set = []
        i = 0
        #while others:
        while i != 100:
            item_last = others.last()
            item_last_check = item_last.check
            #print ('item_last_check is : ',item_last_check)
            
            check_set.append(item_last_check)
            others = others.exclude(check=item_last_check)
            if not others: break
            i = i + 1      

        print ('check set is : ',check_set)  
  
        i = 0
        for c in corner_set:
                
            for sm in signoff_mode_set:
                for ci in check_set:
                    i = i + 1
                    #print ('p is : ',p)
                    #print ('c is : ',c)

                    item0 = TCheckCase.objects.filter(partition=p, corner=c, signoff_mode=sm, check=ci).last()
                    
                    if item0:
                        pass
                    else:
                        #print('item0 not exit')
                        continue

                    try:
                        status = item0.status
                    except:
                        status = 'xxnull'

                    try:
                        check = item0.check
                    except:
                        check = 'xxnull'

                    try:
                        signoff_mode = item0.signoff_mode
                    except:
                        signoff_mode = 'xxnull'

                    try:
                        summit_time = item0.summit_time
                    except:
                        summit_time = 'xxnull'
                    
                    try:
                        database_version = item0.database_version
                    except:
                        database_version = 'xxnull'
                    
                    try:
                        comment = item0.comment
                    except:
                        comment = 'xxnull'
                    
                    try:
                        check_owner = '%s' % item0.check_owner
                    except:
                        check_owner = 'Null' 

                    element = {'partition':p, 'corner':c, 'signoff_mode':signoff_mode, 'check':check, 'status':status, 'summit_time':summit_time, 'database_version':database_version, 'comment':comment, 'pk':item0.pk, 'check_owner':check_owner}
                    display_set.append(element) 
                
    #print ('display set is : ',display_set)

    #pathgroup_delete = TCheckCase.objects.filter(database_version='felix_test')
    #pathgroup_delete = TCheckCase.objects.all()
    #for i in pathgroup_delete: 
    #    i.check_mode = 'setup'
    #    i.save()
    #    print ('pathgroup_delete is: ', i)
    #    i.delete()

    #return render(request,'signoff_check/test.html',{
    return render(request,'signoff_check/other_check.html',{
        'header':header,
        'display_set':display_set,
        'corner_set':corner_set,
        'partition_set':partition_set,
        'signoff_mode_set':signoff_mode_set,
        }) 

#--------------------------------------------------------------------------------
def other_check_status(request, partition, corner, signoff_mode):
    #item = get_object_or_404(TCheckCase,partition=partition,corner=corner,signoff_mode=signoff_mode)

    checkcase_all = TCheckCase.objects.filter(check_item='signoff_other', partition=partition, corner=corner, signoff_mode=signoff_mode)
    checkcase_last = checkcase_all.last()
    item = checkcase_last

    errornote = ""

    #print('display log_path', item.log_path)
    f = open(item.log_path)
    selected_path = []
    p = ''
    num = 0

    #print('debug: path_id= ', path_id)
    for line in f.readlines():
        p = p+line
        num = num + 1
 
    header =  ['Timing Path']
    
    #print('display path', selected_path)

    if "_delete" in request.POST:
        try:
            print('Item to delete is: ', item)
            item.delete()
            return HttpResponseRedirect(reverse('signoff_check:other_check',args = ()))
        except Exception as e:    
            errornote = str(e)+"debug"

    return render(request,'signoff_check/other_check_item.html',{
        'title':item.partition+"'s "+item.check+", corner is "+item.corner,
        'errornote':errornote,
        'selected_path':selected_path,
        'header':header,
        'p':p,
        })
#--------------------------------------------------------------------------------
#def update_comment(request, partition, corner, signoff_mode, check):
def update_comment(request, pk):
    #item = get_object_or_404(TCheckCase,partition=partition,corner=corner,signoff_mode=signoff_mode)

    #checkcase = TCheckCase.objects.filter(check_item='signoff_other', partition=partition, corner=corner, signoff_mode=signoff_mode, check=check)
    #for i in checkcase:
    #    item = i
    #    break
    item = get_object_or_404(TCheckCase,pk=pk)

    errornote = ""

    header = ['partition', 'corner', 'type', 'status', 'add time', 'database_version', 'comment']

    element = {'partition':item.partition, 'corner':item.corner, 'signoff_mode':item.signoff_mode, 'check':item.check, 'status':item.status, 'summit_time':item.summit_time, 'database_version':item.database_version, 'comment':item.comment}

    fieldsets = [
            {
                'name'     : 'Update comment',
                'editable' : True,
                'fields'   : ['partition', 'corner', 'check', 'status', 'summit_time', 'database_version', 'comment']
                },
            ]
    
    get_fields(item,fieldsets)

    if "_save" in request.POST:
        print('got POST', request.POST['comment'])
        try:
            item.comment = request.POST['comment']
            item.check_owner = request.user
            item.save()
            #return HttpResponseRedirect(reverse('signoff_check:other_check_status',args = (item.partition,item.corner,item.signoff_mode,)))
            return HttpResponseRedirect(reverse('signoff_check:other_check',args = ()))
        except Exception as e:    
            errornote = str(e)+"debug"

    return render(request,'signoff_check/update_comment.html',{
        'title':item.partition+"'s "+item.check+", corner is "+item.corner,
        'errornote':errornote,
        'header':header,
        'item':element,
        'infos':fieldsets,
        })
#--------------------------------------------------------------------------------
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

    context[REDIRECT_FIELD_NAME] = reverse('signoff_check:index')
    context.update(extra_context or {})

    defaults = {
            'extra_context': context,
            'authentication_form': AdminAuthenticationForm,
            'template_name': 'signoff_check/login.html',
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
            'next_page' : reverse('signoff_check:index'),
        }
    return LogoutView.as_view(**defaults)(request)

def password_change(request, extra_context=None):
    """
    Handles the "change password" task -- both form display and validation.
    """
    from django.contrib.admin.forms import AdminPasswordChangeForm
    from django.contrib.auth.views import password_change
    url = reverse('signoff_check:password_change_done')
    defaults = {
        'password_change_form': AdminPasswordChangeForm,
        'post_change_redirect': url,
        'extra_context': dict(**(extra_context or {})),
    }
    defaults['template_name'] = 'signoff_check/change_password.html'
    return password_change(request, **defaults)

def password_change_done(request, extra_context=None):
    """
    Displays the "success" page after a password change.
    """
    from django.contrib.auth.views import password_change_done
    defaults = {
        'extra_context': dict( **(extra_context or {})),
    }
    defaults['template_name'] = 'signoff_check/change_password_done.html'
    return password_change_done(request, **defaults)




#--------------------------------------------------------------------------------
# Create your views here.
