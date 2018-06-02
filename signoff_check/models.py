from django.db import models
import re
#from django.template.defaultfilters import slugify
from django.utils import timezone
import datetime
#from django.utils.html import format_html
from django.contrib.auth.models import User

class TBaseItem(models.Model):
    #check_owner = models.ForeignKey(User,verbose_name="check_owner")
    #check_owner = models.ForeignKey(User,default='admin',related_name="check_owner") 

    project     = models.CharField('project',max_length=20,default='')
    check_item  = models.CharField('check_item',max_length=20,default='')
    partition  = models.CharField('partition',max_length=20,default='')
    stage     = models.CharField('stage',max_length=20,default='R0')

    vio_total_number = models.CharField('vio total number',max_length=10,default='')
    corner  = models.CharField('corner',max_length=20,default='-')
    fn  = models.CharField('fn',max_length=20,default='-')
    signoff_mode  = models.CharField('signoff_mode',max_length=20,default='-')
    check_mode  = models.CharField('check_mode',max_length=20,default='-')

    database_version  = models.CharField('database version',max_length=50,default='-')
    database_date   = models.CharField('database date',max_length=50,default='-')
    summit_time	= models.CharField('summit time',max_length=40,default='')

    redundent = models.CharField('redundent',max_length=100)
    log  = models.CharField('log',max_length=300,default='-')

    setup_wns = models.CharField('Setup WNS',max_length=20,default='-')
    setup_tns = models.CharField('Setup TNS',max_length=20,default='-')
    setup_nvp = models.CharField('Setup NVP',max_length=20,default='-')

    hold_wns = models.CharField('Hold WNS',max_length=20,default='-')
    hold_tns = models.CharField('Hold TNS',max_length=20,default='-')
    hold_nvp = models.CharField('Hold NVP',max_length=20,default='-')

    def __str__(self) : return self.summit_time

class TOwnerCase(TBaseItem):
    owner		= models.CharField('Owner',max_length=20,default='-')
    wns         = models.CharField('WNS',max_length=20,default='-')
    tns         = models.CharField('TNS',max_length=20,default='-')
    nvp         = models.CharField('NVP',max_length=20,default='-')
    freq        = models.CharField('FREQ',max_length=20,default='-')
    wns_h       = models.CharField('WNS(H)',max_length=20,default='-')
    tns_h       = models.CharField('TNS(H)',max_length=20,default='-')
    nvp_h       = models.CharField('NVP(H)',max_length=20,default='-')
    type        = models.CharField('type',max_length=20,default='-')
    log_path    = models.CharField('log path',max_length=500,default='-')

    def __str__(self) : return self.owner

class TPathGroup(TBaseItem):
    group       = models.CharField('Path Group',max_length=50,default='-')
    wns         = models.CharField('WNS',max_length=20,default='-')
    tns         = models.CharField('TNS',max_length=20,default='-')
    nvp         = models.CharField('NVP',max_length=20,default='-')
    freq        = models.CharField('FREQ',max_length=20,default='-')
    wns_h       = models.CharField('WNS(H)',max_length=20,default='-')
    tns_h       = models.CharField('TNS(H)',max_length=20,default='-')
    nvp_h       = models.CharField('NVP(H)',max_length=20,default='-')
    type        = models.CharField('type',max_length=20,default='-')
    log_path    = models.CharField('log path',max_length=500,default='-')

    def __str__(self) : return self.group
	

class TCheckCase(TBaseItem):
    check       = models.CharField('Check',max_length=40,default='-')
    status      = models.CharField('Status',max_length=20,default='-')
    log_path    = models.CharField('log path',max_length=500,default='-')
    comment     = models.TextField(max_length=500,default='-')

    #l = models.CharField('l ',max_length=5,default='-')
    check_owner = models.ForeignKey(User,models.SET_NULL,blank=True,null=True,related_name="check_owner")
    #check_owner = models.ForeignKey(User,models.SET_NULL,blank=True,null=True,on_delete=models.SET_NULL,related_name="check_owner")
    #check_owner = models.ForeignKey(User,db_index=True,related_name="check_owner")
    #check_owner = models.ForeignKey(User,default='',related_name="check_owner") 

    def __str__(self) : return self.check

# Create your models here.
