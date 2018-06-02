from django.contrib import admin
from .models import TBaseItem, TOwnerCase, TPathGroup, TCheckCase

class TBaseAdmin(admin.ModelAdmin):
    list_display = ('project','partition','check_item','vio_total_number','corner','database_version','database_date','summit_time')
    fieldsets = [
            ('base',{'fields':['project','partition','check_item','vio_total_number','corner','database_version','database_date','summit_time']}),
            ]
    def __init__(self,*args,**kargs):
        if hasattr(self,'otherfields'):
            self.fieldsets=self.fieldsets + self.otherfields
        if hasattr(self,'otherlist'):
            self.list_display=self.list_display + self.otherlist
            pass
        super(TBaseAdmin,self).__init__(*args,**kargs)

class TOwnerCaseAdmin(TBaseAdmin):
    #inlines = [PointCommentInline]
    otherlist = ('owner','wns','tns','nvp','freq','wns_h','tns_h','nvp_h')
    otherfields = [
            ('other',{'fields':['owner','wns','tns','nvp','freq','wns_h','tns_h','nvp_h']}),
            #('user',{'fields':['class','cover_way','cover_way_status','verify_status']}),
            ]

class TPathGroupAdmin(TBaseAdmin):
    #inlines = [PointCommentInline]
    otherlist = ('group','wns','tns','nvp','freq','wns_h','tns_h','nvp_h')
    otherfields = [
            ('other',{'fields':['group','wns','tns','nvp','freq','wns_h','tns_h','nvp_h']}),
            #('user',{'fields':['class','cover_way','cover_way_status','verify_status']}),
            ]

class TCheckCaseAdmin(TBaseAdmin):
    #inlines = [PointCommentInline]
    otherlist = ('check','status','log_path')
    otherfields = [
            ('other',{'fields':['check','status','log_path']}),
            #('user',{'fields':['class','cover_way','cover_way_status','verify_status']}),
            ]
#admin.site.register(TOwnerCase, TOwnerCaseAdmin, TPathGroup, TPathGroupAdmin)
admin.site.register(TOwnerCase, TOwnerCaseAdmin)
admin.site.register(TPathGroup, TPathGroupAdmin)
admin.site.register(TCheckCase, TCheckCaseAdmin)

# Register your models here.
