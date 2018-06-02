from django.contrib import admin
from .models import BaseItem, OwnerCase
from .models import case

class BaseAdmin(admin.ModelAdmin):
    list_display = ('summit_time', 'project', 'check_item', 'partition', 'fail_total_number', 'design_git_number')
    fieldsets = [
        ('base',{'fields':['summit_time','project','design_git_number','fail_total_number']}),
        ]
    def __init__(self,*args,**kargs):
        if hasattr(self,'otherfields'):
            self.fieldsets=self.fieldsets + self.otherfields
        if hasattr(self,'otherlist'):
            self.list_display=self.list_display + self.otherlist
            pass
        super(BaseAdmin,self).__init__(*args,**kargs)

class OwnerCaseAdmin(BaseAdmin):
    otherlist = ('owner','fail_number','log_path')
    otherfields = [
            ('other',{'fields':['owner','fail_number','log_path','content']}),
            ]

class caseAdmin(BaseAdmin):
    otherlist = ('table_order','case_type','c1_key')
    otherfields = [
            ('other',{'fields':['table_title','column_num','c2_key','c2_val']}),
            ]

admin.site.register(OwnerCase,OwnerCaseAdmin)
admin.site.register(case,caseAdmin)

# Register your models here.
