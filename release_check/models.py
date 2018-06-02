from django.db import models

# Create your models here.

class BaseItem(models.Model):
	
	summit_time = models.CharField('summit_time', max_length=20, default='')	
	project = models.CharField('project', max_length=20, default='')	
	check_item = models.CharField('check_item', max_length=20, default='')	
	partition = models.CharField('partition', max_length=20, default='')	
	fail_total_number = models.CharField('fail_total_number', max_length=20, default='')	
	fail_owner_count= models.CharField('fail_owner_count', max_length=20, default='')	
	design_git_number = models.CharField('design_git_number', max_length=50, default='')	
	design_git_date = models.CharField('design_git_date', max_length=50, default='')	

	def __str__(self) : return self.summit_time

class OwnerCase(BaseItem):
	owner = models.CharField('owner', max_length=20, default='')	
	fail_number = models.CharField('fail_number', max_length=20, default='')	
	warn_number = models.CharField('warn_number', max_length=20, default='')	
	info_number = models.CharField('info_number', max_length=20, default='')	
	log_path = models.CharField('log_path', max_length=150, default='')	
	content = models.TextField('content', max_length=3000, default='')	
	
	def design_git_num(self):
		if re.match('(\w\w\w\w\w\w\w\w)', str(self.design_git_number)):
			num = re.match('(\w\w\w\w\w\w\w\w)', str(self.design_git_number))
			return num.group(1)+'*'
		else:
			return self.design_git_number

	def __str__(self) : return self.owner


class unit(models.Model):
	key = models.CharField('key', max_length=20, default='', unique=True, primary_key=True)	
	val = models.CharField('val', max_length=20, default='')	
	def __str__(self) : return self.key+' -> '+self.val

class case_old(models.Model):
	case_type = models.CharField('case_type', max_length=20, default='')	
	case_num = models.CharField('case_num', max_length=5, default='')	
	c1 = models.ForeignKey('unit', on_delete = models.CASCADE, related_name='c1', default='')
	c2 = models.ForeignKey('unit', on_delete = models.CASCADE, related_name='c2', default='')
	c3 = models.ForeignKey('unit', on_delete = models.CASCADE, related_name='c3', default='')
	c4 = models.ForeignKey('unit', on_delete = models.CASCADE, related_name='c4', default='')
	c5 = models.ForeignKey('unit', on_delete = models.CASCADE, related_name='c5', default='')
	link = models.CharField('link', max_length=150, default='')	
	def __str__(self) : return self.c1
	
class case(BaseItem):
	table_title = models.CharField('table_title', max_length=50, default='')	
	table_order = models.CharField('table_order', max_length=50, default='')	
	case_type = models.CharField('case_type', max_length=30, default='')	
	column_num = models.CharField('case_num', max_length=5, default='')	
	c1_key = models.CharField('c1_key', max_length=30, default='')	
	c1_val = models.CharField('c1_val', max_length=30, default='')	
	c2_key = models.CharField('c2_key', max_length=30, default='')	
	c2_val = models.CharField('c2_val', max_length=30, default='')	
	c3_key = models.CharField('c3_key', max_length=30, default='')	
	c3_val = models.CharField('c3_val', max_length=30, default='')	
	c4_key = models.CharField('c4_key', max_length=30, default='')	
	c4_val = models.CharField('c4_val', max_length=30, default='')	
	c5_key = models.CharField('c5_key', max_length=30, default='')	
	c5_val = models.CharField('c5_val', max_length=30, default='')	
	c6_key = models.CharField('c6_key', max_length=30, default='')	
	c6_val = models.CharField('c6_val', max_length=30, default='')	

	link = models.CharField('link', max_length=150, default='')	
	def __str__(self) : return self.c1_key + '-> ' + self.c1_val
