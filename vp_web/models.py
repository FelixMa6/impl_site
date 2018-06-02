from django.db import models
from django.contrib.auth.models import User

class BaseItem(models.Model):
    name = models.CharField('name',max_length=80,db_index=True,unique=True)#feature type
    description = models.TextField('description',max_length=2000)#feature type description
    owner = models.ForeignKey(User,verbose_name="Owner") #feature type owner, equal to reveiwer

    add_time    = models.DateTimeField('date published',auto_now_add=True)
    modified_time = models.DateTimeField('date changed',auto_now=True,blank=True)
    STATUS = (
        ('0','0%'),
        ('1','10%'),
        ('2','20%'),
        ('3','30%'),
        ('4','40%'),
        ('5','50%'),
        ('6','60%'),
        ('7','70%'),
        ('8','80%'),
        ('9','90%'),
        ('10','100%'),
        ('DO','closed'),
        )

    T_STATUS = (
        #('NO','no progress'),
        ('OG','on going'),
        #('RD','ready'),
        ('DO','closed'),
        )

    #status = models.CharField(max_length=2,choices=T_STATUS,default=T_STATUS[0][0],blank=True)
    status = models.CharField(max_length=2,choices=STATUS,default=STATUS[0][0],blank=True)

    def __str__(self) : return self.name

class CComponent(BaseItem):
    pass

class CChecker(BaseItem):pass
class CVector(BaseItem):pass
class CCover(BaseItem):pass


class CFeature(BaseItem):
    component = models.ForeignKey('CComponent')

class CVerification(BaseItem):
    feature = models.ForeignKey('CFeature',default='')
    #feature_name = models.CharField('Feature_name',max_length=80,blank=True)#feature point name
    #feature_description = models.TextField('Feature_description',default='',max_length=300)
    msr_info = models.CharField('MSR ',max_length=80,blank=True)
    feature_tag = models.CharField('Feature_tag',max_length=100,blank=True)
    feature_tag_exist = models.BooleanField('Feeature tag exist status',default=False)
    feature_status = models.CharField(max_length=2,choices=BaseItem.STATUS,default=BaseItem.STATUS[0][0],blank=True)

    cover_sva = models.CharField('Cover_sva',default='fill your cover sva file name',max_length=500,blank=True)
    cover_sva_owner = models.ForeignKey(User,default='',related_name="Cover_sva_owner") 
    cover_sva_description = models.TextField('cover_sva_description',default='',max_length=1000)
    cover_status = models.CharField(max_length=2,choices=BaseItem.STATUS,default=BaseItem.STATUS[0][0],blank=True)
    cover_sva_exist = models.BooleanField('Cover sva exist status',default=False)

    coverage = models.CharField('Coverage',default='fill your cover sva file name',max_length=500,blank=True)
    coverage_owner = models.ForeignKey(User,default='',related_name="Coverage_owner") 
    coverage_status = models.CharField(max_length=2,choices=BaseItem.STATUS,default=BaseItem.STATUS[0][0],blank=True)
    coverage_description = models.TextField('coverage_description',default='',max_length=1000)
    coverage_exist = models.BooleanField('Cover sva exist status',default=False)

    #cover_sva_owner = models.ForeignKey(User,default='',verbose_name="Verify_owner") 
    reviewer = models.ForeignKey(User,default='',related_name="Reviewer") 

    verify_status = models.CharField(max_length=2,choices=BaseItem.STATUS,default=BaseItem.STATUS[0][0],blank=True)

    stimulus = models.CharField('Stimulus',max_length=500,blank=True)
    stimulus_other = models.CharField('Stimulus_other',max_length=500,blank=True)
    #class_owner = models.ForeignKey(User,default='',related_name="Class_owner") 
    stimulus_owner = models.ForeignKey(User,default='',related_name="Stimulus_owner") 
    stimulus_description = models.TextField('Stimulus_description',default='',max_length=1000)
    stimulus_status = models.CharField(max_length=2,choices=BaseItem.STATUS,default=BaseItem.STATUS[0][0],blank=True)
    stimulus_exist = models.BooleanField('Stimulus exist status',default=False)
    stimulus_other_exist = models.BooleanField('Stimulus other exist status',default=False)

    check_way = models.CharField('Check_way',max_length=500,blank=True)
    check_way_owner = models.ForeignKey(User,default='',related_name="Check_way_owner") 
    check_way_description = models.TextField('Check_way_description',default='',max_length=1000)
    check_way_status = models.CharField(max_length=2,choices=BaseItem.STATUS,default=BaseItem.STATUS[0][0],blank=True)
    check_way_exist = models.BooleanField('Check way exist status',default=False)

    COVER_STATUS = (
        ('N','not covered'),
        ('Y','covered'),
        )  

    vp_covered = models.BooleanField('VP covered status',default=False)
    vp_cover_count = models.CharField('VP cover count',max_length=10,blank=True)
    vp_covered_status = models.CharField(max_length=2,choices=COVER_STATUS,default=COVER_STATUS[0][0],blank=True)

    RANDOM_STATUS = (
        ('N','not randomed'),
        ('Y','randomed'),
        ) 

    stimulus_covered = models.BooleanField('Stimulus covered status',default=False)
    stimulus_covered_status = models.CharField(max_length=2,choices=RANDOM_STATUS,default=RANDOM_STATUS[0][0],blank=True)

    VRG_STATUS = (
        ('NO','not in regression'),
        ('RD','has in regression'),
        )

    into_regression = models.CharField(max_length=2,choices=VRG_STATUS,default=VRG_STATUS[0][0],blank=True)
    #def not_ready(self) : return (check_way_status != BaseItem.STATUS[-2][0] & check_way_status != BaseItem.STATUS[-1][0]) 


class PointComment(models.Model):
    Author     = models.ForeignKey(User,verbose_name='Author') 
    point     = models.ForeignKey(CVerification,verbose_name='point') 
    content    = models.TextField(max_length=900)
    add_time   = models.DateTimeField('date published',auto_now_add=True)
    def __str__(self) : return "%s: %s" % (self.Author.username,self.content)

    #assignee =  models.ForeignKey(User,verbose_name='Assignee')

#
