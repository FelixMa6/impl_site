from django.contrib import admin
from .models import VectorIssue,Comment,Category,DailyReport
from django import forms

class CommentInline(admin.StackedInline):
    model = Comment
    extra = 1


class IssueAdmin(admin.ModelAdmin):
    inlines = [CommentInline]
    list_display = ('id','vector','bugowner','category','project','active','set_top','add_time','modified_time','last_comment')

    fieldsets = [
	    ('content',               {'fields':['vector','content']}),
	    ('path',{'fields':['src_path','wave_path','log_path']}),
	    ('status',{'fields':['category','bugowner','reason','active','set_top']}),
	    ]

    def formfield_for_dbfield(self,db_field,**kwargs):
        formfield = super(IssueAdmin,self).formfield_for_dbfield(db_field,**kwargs)
        if db_field.name in ['content']:
            formfield.widget = forms.Textarea(attrs={'rows':3,'cols':50})
        if db_field.name in ['src_path','wave_path','log_path'] :
            formfield.widget = forms.Textarea(attrs={'rows':1,'cols':100})
        return formfield  


def project_clear_counter(self,request,queryset):
    rowsUpdated = queryset.update(counter=0)
    if rowsUpdated == 1 : ms = "1 category was"
    else : ms = "%s categories were" % rowsUpdated
    self.message_user(request,"%s successfully changed counter to 0." % ms)
project_clear_counter.short_description = "Clear selected categories counter"

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title','counter','owner')
    actions = [project_clear_counter]

class ReportAdmin(admin.ModelAdmin):
    list_display = ('add_time','start_day','end_day','pass_number','fail_number','pass_rate')

admin.site.register(VectorIssue,IssueAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(DailyReport,ReportAdmin)


# Register your models here.
