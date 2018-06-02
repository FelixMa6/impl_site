from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.cache import never_cache
from django.utils.translation import ugettext as _, ugettext_lazy
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.shortcuts import render,get_object_or_404
from django.utils.html import format_html
import socket,datetime
import re
from .models import BaseItem, OwnerCase, case
import os

def index(request):
    try:
        #check_lint_all = OwnerCase.objects.filter(check_item='check_lint', partition='tingtao')
        check_lint_all = OwnerCase.objects.all()
        check_lint_last = check_lint_all.last()
        print ('check lint all object is: ',check_lint_all)

        check_lint_fieldsets = [
            {
            'name'      :'Linting result summary',
            'editable'  :False,
            'fields'    :['fail_total_number','project','summit_time','design_git_number','design_git_date'],
                }
            ]

        get_fields(check_lint_last,check_lint_fieldsets)
    except:
        check_lint_last = None
        check_lint_all = None
        check_lint_fieldsets = None

     
    header = ['Owner','fail_number','warn_number','info_number']
    #-------------------------------------------------------------------------------------
	#for case table
    case_type_set = []
    table_title_1 = None
    case_header_1 = None
    case_all_1 = None
    column_num_1 = None
    table_title_2 = None
    case_header_2 = None
    case_all_2 = None
    column_num_2 = None
    table_title_3 = None
    case_header_3 = None
    case_all_3 = None
    column_num_3 = None
    table_title_4 = None
    case_header_4 = None
    case_all_4 = None
    column_num_4 = None

    try:
        case_all = case.objects.all()
        others = case_all
        table_num = 0
        while table_num != 100:
        	item_last = others.last()
        	item_last_type = item_last.case_type
        	case_type_set.append(item_last_type)
        	others = others.exclude(case_type=item_last_type)
        	if not others: break
        	table_num = table_num + 1

        print ('case type list is: ',case_type_set)
        
        case_last = case_all.last()

        case_fieldsets = [
            {
            'name'      :'Linting result summary',
            'editable'  :False,
            'fields'    :['fail_total_number','project','summit_time','design_git_number','design_git_date'],
                }
            ]

        get_fields(case_last, case_fieldsets)
        
		#divide table
        k = 0
        while k <= table_num:
            k = k + 1
            case_set = case.objects.filter(table_order=str(k))
            case_last = case_set.last()
					
            case_header = []
            i = 0
            while i < int(case_last.column_num):
            	i = i + 1
            	if i == 1: case_header.append(case_last.c1_key)
            	if i == 2: case_header.append(case_last.c2_key)
            	if i == 3: case_header.append(case_last.c3_key)
            	if i == 4: case_header.append(case_last.c4_key)
            	if i == 5: case_header.append(case_last.c5_key)
            	if i == 6: case_header.append(case_last.c6_key)
            	
            column_num = int(case_last.column_num)
            table_title = case_last.table_title

            print ('loop k is ', k)
			
            if k == 1: 
            	table_title_1 = table_title
            	case_header_1 = case_header
            	case_all_1 = case_set
            	column_num_1 = column_num
            
            if k == 2: 
            	table_title_2 = table_title
            	case_header_2 = case_header
            	case_all_2 = case_set
            	column_num_2 = column_num

            if k == 3: 
            	table_title_3 = table_title
            	case_header_3 = case_header
            	case_all_3 = case_set
            	column_num_3 = column_num

            if k == 4: 
            	table_title_4 = table_title
            	case_header_4 = case_header
            	case_all_4 = case_set
            	column_num_4 = column_num

            print ('case_header is ', case_header)
            print ('case_set is ', case_set)
            print ('column_num is ', column_num)
            print ('table title is ', table_title)
    except:
        table_title = None
        case_header = None
        case_all = None
        column_num = None
        print ('no case object')

    #-------------------------------------------------------------------------------------
    #for check timing
    #1) for parition processor 
    check_timing_processor_all = OwnerCase.objects.filter(check_item='check_timing', partition='tingtao')
    check_timing_processor_all = check_timing_processor_all.order_by('owner')
    check_timing_processor_last = check_timing_processor_all.last()
    check_timing_processor_first = check_timing_processor_all.first()
    #print (check_timing_processor_last)

    #print (check_timing_processor_all)

    check_timing_processor_fieldsets = [
            {
            'name'  : 'Check Timing for xxx',
            'editable' : False,
            'fields': ['fail_total_number','project','summit_time','design_git_number','design_git_date'],
                }
            ]
    
    if check_timing_processor_last:
        get_fields(check_timing_processor_last,check_timing_processor_fieldsets)  

    #-------------------------------------------------------------------------------------

    errornote = 'no info in release check database'
    cleannote = 'no lint error'

    return render(request, 'release_check/index.html',{
        'title':'',
        'infos':case_fieldsets,
		#lint case
        'item':check_lint_last,
        'all':check_lint_all,
        'header':header,
        'errornote':errornote,
        'cleannote':cleannote,
        #show table 1 case
		'table_title_1':table_title_1,
		'case_header_1':case_header_1,
		'case_all_1':case_all_1,
		'column_num_1':column_num_1,
        #show table 2 case
		'table_title_2':table_title_2,
		'case_header_2':case_header_2,
		'case_all_2':case_all_2,
		'column_num_2':column_num_2,
        #show table 3 case
		'table_title_3':table_title_3,
		'case_header_3':case_header_3,
		'case_all_3':case_all_3,
		'column_num_3':column_num_3,
        #show table 4 case
		'table_title_4':table_title_4,
		'case_header_4':case_header_4,
		'case_all_4':case_all_4,
		'column_num_4':column_num_4,
        #check timing for processor
        'check_timing_processor_item':check_timing_processor_last,
        'check_timing_processor_all':check_timing_processor_all,
        'check_timing_processor_infos':check_timing_processor_fieldsets,
        })

#--------------------------------------------------------------------------------------
def owner(request,pk):
    
    item = get_object_or_404(OwnerCase,pk=pk)
    print ("item in owner is :", item)
    print ("item pk is :", item.pk)
    print ("item path is :", item.log_path)
    errornote = ''

    f = open(item.log_path)
    c = []
    error_set = []
    num = 1

    for line in f.readline():
        if (re.search('Line', line) and item.check_item == 'check_lint') :
            l = 'line number'+str(num)+line
            c.append(l)
            error_element = {'num':num, 'line':line}
            error_set.append(error_element)
            num = num + 1
        else:
            pass

    item.content = c

    header = ['No', 'Error info']

    fieldsets = [
        {
        'name'      :'Summary',
        'editable'  : False,
        'fields'    :['fail_number','log_path']
            }
    ]
    get_fields(item,fieldsets)
    print ("infos is :", fieldsets)

    return render(request, 'release_check/owner.html', {
        'title':item.owner+"'s fail",
        'infos':fieldsets,
        'errornote':errornote,
        'error_set':error_set,
        'header':header,
        'ownercase':item,
        })
#--------------------------------------------------------------------------------------
def get_html_content (item, mydict, review):
    #input_list = ['summit_time', 'project', ]

    if mydict['name'] == 'content' :
        content = '<textarea class="vLargeTextField" cols="40" id="id_{0} maxlength="900" name="{0} rows="10">{1}</textarea>'.format(mydict['name'], getattr(item, mydict['name']))

    mydict['content'] = format_html(content)

#--------------------------------------------------------------------------------------
def get_content(item,name):
    if name == 'feature_status' or name == 'status' :
        name = 'get_%s_display' % name
    attr = getattr(item, name)
    return attr

#--------------------------------------------------------------------------------------
def get_fields(item, fieldsets, review=0):
    if not fieldsets : return
    name_change = {}
    for line in fieldsets:
        if not line['editable']:
            for i in range(len(line['fields'])):
                name = line['fields'][i]
                content = get_content(item, name)
                if content == '' : content = '-'
                if name in name_change.keys():
                    name = name_change[name]
                line['fields'][i] = {
                    'content': content,
                    'name': name,
                    }
        else:
            for i in range(len(line['fields'])):
                name = line['fields'][i]
                mydict = {
                    'name':name,
                    }
                get_html_content(item, mydict, review)
                line['fields'][i] = mydict
#--------------------------------------------------------------------------------
def log(request, pk):
    item = get_object_or_404(case,pk=pk)
    errornote = ""

    #print('display log_path', item.log_path)
    f = open(item.link)
    selected_path = []
    p = ''
    num = 0

    for line in f.readlines():
        p = p+line


    header =  'Log content;'
    
    #print('display path', selected_path)

    return render(request,'release_check/log.html',{
        'title':item.c1_val +"'s log content",
        'errornote':errornote,
        'header':header,
        'p':p,
        })

#--------------------------------------------------------------------------------------

