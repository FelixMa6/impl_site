from django.contrib import admin
from .models import CComponent,CFeature,CVerification,PointComment

class PointCommentInline(admin.StackedInline):
    model = PointComment
    extra = 1

class BaseAdmin(admin.ModelAdmin):
    list_display = ('name','description','owner','modified_time')
    fieldsets = [
            ('base',{'fields':['name','description','owner']}),
            ]
    def __init__(self,*args,**kargs):
        if hasattr(self,'otherfields'):
            self.fieldsets=self.fieldsets + self.otherfields
        if hasattr(self,'otherlist'):
            self.list_display=self.list_display + self.otherlist
            pass
        super(BaseAdmin,self).__init__(*args,**kargs)

class ComponentAdmin(BaseAdmin):
    pass

class FeatureAdmin(BaseAdmin):
    otherlist = ('component',)
    otherfields = [
            ('component',{'fields':['component']}),
            ]



class VerificationAdmin(BaseAdmin):
    inlines = [PointCommentInline]
    otherlist = ('status','cover_status')
    otherfields = [
            ('other',{'fields':['feature','coverage','feature_status']}),
            #('Stimulus',{'fields':['stimulus_single','stimulus_dual','stimulus_description','stimulus_owner','vrg_register_status','stimulus_status']}),
            ('user',{'fields':['stimulus_single','check_way','coverage_description','check_way_status','verify_status']}),
            ]

admin.site.register(CComponent,ComponentAdmin)
admin.site.register(CFeature,FeatureAdmin)
admin.site.register(CVerification,VerificationAdmin)

# Register your models here.
