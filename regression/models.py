from django.db import models
import re
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.utils import timezone
import datetime
from django.utils.html import format_html

class VectorIssue(models.Model):
    BUG_TYPE = (
        ('IN','unknown'),
        ('RE','real bug'),
        ('EN','environment issue'),
        ('VC','vector issue'),
        ('PF','performance issue'),
        )
    
    vector      = models.CharField('vector_name',max_length=80,db_index=True,unique=True)
    snippet     = models.CharField('abstract',max_length=100,default='')
    content     = models.CharField('content',max_length=320)
    src_path    = models.CharField('vector path',default="",max_length=150)
    wave_path   = models.CharField('waveform path',default='',max_length=150)
    log_path    = models.CharField('log path',default='',max_length=150)
    reason        = models.CharField(max_length=2,choices=BUG_TYPE,default=BUG_TYPE[0][0])
    add_time    = models.DateTimeField('date published',auto_now_add=True)
    bugowner    = models.ForeignKey(User,verbose_name='Owner')
    category    = models.ForeignKey('Category')
    active      = models.BooleanField('Bug opened',default=True)
    set_top = models.BooleanField('Set top',default=True)
    project     = models.CharField('project',max_length=20,default='')

    design_git  = models.CharField('design git version',max_length=100,default='-')
    env_git     = models.CharField('env git version',max_length=100,default='-')
    design_git_date     = models.CharField('env git version',max_length=100,default='-')
    env_git_date     = models.CharField('env git version',max_length=100,default='-')

    modified_time = models.DateTimeField('date changed',auto_now=True,blank=True)

    def last_comment(self):
        return self.comment_set.last()

    def last_7days(self):
        return self.add_time >= timezone.now - datetime.timedelta(days=7)
    
    def play_fsdb(self):
        return "/haydn/marshall/tools/fsdb_tool/playfsdb.py civ {0}".format(self.wave_path)


    def __str__(self) : return self.vector

class Category(models.Model):
    title = models.CharField('Fail Type', max_length=50, db_index=True,unique=True)
    owner = models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    counter = models.IntegerField(default=0)
    
    class Meta : ordering = ['title',]

    def clear(self) : counter = -1 #save will auto add

    def save(self, *args,flag=False, **kwargs):
        if flag:
            self.counter += 1
        super(Category,self).save(*args,**kwargs)

    def isEmpty(self):
        return self.counter==0


    def __str__(self) : return self.title

class Comment(models.Model):
    Assignee     = models.ForeignKey(User,verbose_name='assignee') 
    vector     = models.ForeignKey(VectorIssue,verbose_name='vector') 
    content    = models.TextField(max_length=900)
    add_time   = models.DateTimeField('date published',auto_now_add=True)
    def __str__(self) : return "%s: %s" % (self.Assignee.username,self.content)

class DailyReport(models.Model):
    pass_number = models.IntegerField(default=0)
    fail_number = models.IntegerField(default=0)

    pass_number_prj1 = models.IntegerField(default=0)
    fail_number_prj1 = models.IntegerField(default=0)

    total_request = models.IntegerField(default=0)
    c2m           = models.IntegerField(default=0)
    c2p           = models.IntegerField(default=0)
    p2c           = models.IntegerField(default=0)
    c2p_io        = models.IntegerField(default=0)
    c2p_mem       = models.IntegerField(default=0)
    c2p_special   = models.IntegerField(default=0)
    cl0_l2_hit    = models.IntegerField(default=0)
    cl0_l2_miss   = models.IntegerField(default=0)
    cl1_l2_hit    = models.IntegerField(default=0)
    cl1_l2_miss   = models.IntegerField(default=0)
    hotwire       = models.IntegerField(default=0)
    fsbc_request  = models.IntegerField(default=0)
    fsbc_trigger  = models.IntegerField(default=0)
    cl0_msr_read  = models.IntegerField(default=0)
    cl0_msr_write = models.IntegerField(default=0)
    cl1_msr_read  = models.IntegerField(default=0)
    cl1_msr_write = models.IntegerField(default=0)
    interrupt_ipi = models.IntegerField(default=0)
    interrupt_msi = models.IntegerField(default=0)
    interrupt_sb  = models.IntegerField(default=0)

    c2m_s1           = models.IntegerField(default=0)
    c2p_s1           = models.IntegerField(default=0)
    p2c_s1           = models.IntegerField(default=0)
    c2p_io_s1        = models.IntegerField(default=0)
    c2p_mem_s1       = models.IntegerField(default=0)
    c2p_special_s1   = models.IntegerField(default=0)
    cl0_l2_hit_s1    = models.IntegerField(default=0)
    cl0_l2_miss_s1   = models.IntegerField(default=0)
    cl1_l2_hit_s1    = models.IntegerField(default=0)
    cl1_l2_miss_s1   = models.IntegerField(default=0)
    hotwire_s1       = models.IntegerField(default=0)
    fsbc_request_s1  = models.IntegerField(default=0)
    fsbc_trigger_s1  = models.IntegerField(default=0)
    cl0_msr_read_s1  = models.IntegerField(default=0)
    cl0_msr_write_s1 = models.IntegerField(default=0)
    cl1_msr_read_s1  = models.IntegerField(default=0)
    cl1_msr_write_s1 = models.IntegerField(default=0)
    interrupt_ipi_s1 = models.IntegerField(default=0)
    interrupt_msi_s1 = models.IntegerField(default=0)
    interrupt_sb_s1  = models.IntegerField(default=0)

    vpi_s0_s1 = models.IntegerField(default=0)
    vpi_s1_s0 = models.IntegerField(default=0)

    jtag          = models.IntegerField(default=0)

    add_time    = models.DateTimeField('date add',auto_now_add=True)

    def pass_rate(self):
        if self.pass_number + self.fail_number == 0:
            return "0.00%"
        pass_rate = self.pass_number / (self.pass_number + self.fail_number) * 100.0
        return "%.2f%%" % pass_rate

    def add_pass(self):
        self.pass_number += 1

    def add_fail(self):
        self.fail_number += 1


    def pass_rate_prj1(self):
        if self.pass_number_prj1 + self.fail_number_prj1 == 0:
            return "0.00%"
        pass_rate_prj1 = self.pass_number_prj1 / (self.pass_number_prj1 + self.fail_number_prj1) * 100.0
        return "%.2f%%" % pass_rate_prj1

    def add_pass_prj1(self):
        self.pass_number_prj1 += 1

    def add_fail_prj1(self):
        self.fail_number_prj1 += 1

    def pass_rate_prj2(self): 
        return self.pass_rate_prj1

    def pass_number_prj2(self): 
        return self.pass_number_prj1

    def fail_number_prj2(self): 
        return self.fail_number_prj1

    def create_time(self):
        return self.start_day().strftime('%d-%b-%Y')

    def start_day(self):
        temp = self.add_time + datetime.timedelta(hours=8)
        day_num = temp.weekday()
        hour = temp.hour
        if hour < 18 :
            temp = temp - datetime.timedelta(days=1)
        year  = temp.year
        month = temp.month
        day   = temp.day
        delta = datetime.timedelta(hours=18)
        return datetime.datetime(year,month,day) + delta

    def end_day(self):
        temp = self.add_time + datetime.timedelta(hours=8)
        hour = temp.hour
        if hour >= 18 :
            temp = temp + datetime.timedelta(days=1)
        year  = temp.year
        month = temp.month
        day   = temp.day
        delta = datetime.timedelta(hours=18)
        return datetime.datetime(year,month,day) + delta


    def is_same_work_day(self):
        now = datetime.datetime.now()
        if now > self.end_day():
            return False
        if now < self.start_day():
            raise Exception("create time error")
        return True

    def __str__(self):
        return "Pass Number: %d; Fail Number: %d; Total request: %d" % (self.pass_number,self.fail_number,self.total_request)



# Create your models here.
