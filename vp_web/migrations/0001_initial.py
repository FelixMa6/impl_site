# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-28 01:11
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=80, unique=True, verbose_name='name')),
                ('description', models.TextField(max_length=2000, verbose_name='description')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='date published')),
                ('modified_time', models.DateTimeField(auto_now=True, verbose_name='date changed')),
                ('status', models.CharField(blank=True, choices=[('0', '0%'), ('1', '10%'), ('2', '20%'), ('3', '30%'), ('4', '40%'), ('5', '50%'), ('6', '60%'), ('7', '70%'), ('8', '80%'), ('9', '90%'), ('10', '100%'), ('DO', 'closed')], default='0', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='PointComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=900)),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='date published')),
                ('Author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Author')),
            ],
        ),
        migrations.CreateModel(
            name='CChecker',
            fields=[
                ('baseitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='vp_web.BaseItem')),
            ],
            bases=('vp_web.baseitem',),
        ),
        migrations.CreateModel(
            name='CComponent',
            fields=[
                ('baseitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='vp_web.BaseItem')),
            ],
            bases=('vp_web.baseitem',),
        ),
        migrations.CreateModel(
            name='CCover',
            fields=[
                ('baseitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='vp_web.BaseItem')),
            ],
            bases=('vp_web.baseitem',),
        ),
        migrations.CreateModel(
            name='CFeature',
            fields=[
                ('baseitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='vp_web.BaseItem')),
                ('component', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vp_web.CComponent')),
            ],
            bases=('vp_web.baseitem',),
        ),
        migrations.CreateModel(
            name='CVector',
            fields=[
                ('baseitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='vp_web.BaseItem')),
            ],
            bases=('vp_web.baseitem',),
        ),
        migrations.CreateModel(
            name='CVerification',
            fields=[
                ('baseitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='vp_web.BaseItem')),
                ('msr_info', models.CharField(blank=True, max_length=80, verbose_name='MSR ')),
                ('feature_tag', models.CharField(blank=True, max_length=100, verbose_name='Feature_tag')),
                ('feature_tag_exist', models.BooleanField(default=False, verbose_name='Feeature tag exist status')),
                ('feature_status', models.CharField(blank=True, choices=[('0', '0%'), ('1', '10%'), ('2', '20%'), ('3', '30%'), ('4', '40%'), ('5', '50%'), ('6', '60%'), ('7', '70%'), ('8', '80%'), ('9', '90%'), ('10', '100%'), ('DO', 'closed')], default='0', max_length=2)),
                ('cover_sva', models.CharField(blank=True, default='fill your cover sva file name', max_length=500, verbose_name='Cover_sva')),
                ('cover_sva_description', models.TextField(default='', max_length=1000, verbose_name='cover_sva_description')),
                ('cover_status', models.CharField(blank=True, choices=[('0', '0%'), ('1', '10%'), ('2', '20%'), ('3', '30%'), ('4', '40%'), ('5', '50%'), ('6', '60%'), ('7', '70%'), ('8', '80%'), ('9', '90%'), ('10', '100%'), ('DO', 'closed')], default='0', max_length=2)),
                ('cover_sva_exist', models.BooleanField(default=False, verbose_name='Cover sva exist status')),
                ('verify_status', models.CharField(blank=True, choices=[('0', '0%'), ('1', '10%'), ('2', '20%'), ('3', '30%'), ('4', '40%'), ('5', '50%'), ('6', '60%'), ('7', '70%'), ('8', '80%'), ('9', '90%'), ('10', '100%'), ('DO', 'closed')], default='0', max_length=2)),
                ('stimulus_single', models.CharField(blank=True, max_length=500, verbose_name='Stimulus_single')),
                ('stimulus_dual', models.CharField(blank=True, max_length=500, verbose_name='Stimulus_dual')),
                ('stimulus_description', models.TextField(default='', max_length=1000, verbose_name='Stimulus_description')),
                ('stimulus_status', models.CharField(blank=True, choices=[('0', '0%'), ('1', '10%'), ('2', '20%'), ('3', '30%'), ('4', '40%'), ('5', '50%'), ('6', '60%'), ('7', '70%'), ('8', '80%'), ('9', '90%'), ('10', '100%'), ('DO', 'closed')], default='0', max_length=2)),
                ('stimulus_exist', models.BooleanField(default=False, verbose_name='Stimulus exist status')),
                ('stimulus_dual_exist', models.BooleanField(default=False, verbose_name='Stimulus dual exist status')),
                ('check_way', models.CharField(blank=True, max_length=500, verbose_name='Check_way')),
                ('check_way_description', models.TextField(default='', max_length=1000, verbose_name='Check_way_description')),
                ('check_way_status', models.CharField(blank=True, choices=[('0', '0%'), ('1', '10%'), ('2', '20%'), ('3', '30%'), ('4', '40%'), ('5', '50%'), ('6', '60%'), ('7', '70%'), ('8', '80%'), ('9', '90%'), ('10', '100%'), ('DO', 'closed')], default='0', max_length=2)),
                ('check_way_exist', models.BooleanField(default=False, verbose_name='Check way exist status')),
                ('vp_covered', models.BooleanField(default=False, verbose_name='VP covered status')),
                ('vp_cover_count', models.CharField(blank=True, max_length=10, verbose_name='VP cover count')),
                ('vp_covered_status', models.CharField(blank=True, choices=[('N', 'not covered'), ('Y', 'covered')], default='N', max_length=2)),
                ('stimulus_covered', models.BooleanField(default=False, verbose_name='Stimulus covered status')),
                ('stimulus_covered_status', models.CharField(blank=True, choices=[('N', 'not randomed'), ('Y', 'randomed')], default='N', max_length=2)),
                ('vrg_register_status', models.CharField(blank=True, choices=[('NO', 'not register'), ('RD', 'registered')], default='NO', max_length=2)),
                ('check_way_owner', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='Check_way_owner', to=settings.AUTH_USER_MODEL)),
                ('cover_sva_owner', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='Cover_sva_owner', to=settings.AUTH_USER_MODEL)),
                ('feature', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='vp_web.CFeature')),
                ('reviewer', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='Reviewer', to=settings.AUTH_USER_MODEL)),
                ('stimulus_owner', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='Stimulus_owner', to=settings.AUTH_USER_MODEL)),
            ],
            bases=('vp_web.baseitem',),
        ),
        migrations.AddField(
            model_name='baseitem',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Owner'),
        ),
        migrations.AddField(
            model_name='pointcomment',
            name='point',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vp_web.CVerification', verbose_name='point'),
        ),
    ]
