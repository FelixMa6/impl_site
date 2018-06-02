# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-02-06 13:52
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
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=50, unique=True, verbose_name='Fail Type')),
                ('counter', models.IntegerField(default=0)),
                ('owner', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=900)),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='date published')),
                ('Assignee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='assignee')),
            ],
        ),
        migrations.CreateModel(
            name='DailyReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pass_number', models.IntegerField(default=0)),
                ('fail_number', models.IntegerField(default=0)),
                ('pass_number_prj1', models.IntegerField(default=0)),
                ('fail_number_prj1', models.IntegerField(default=0)),
                ('total_request', models.IntegerField(default=0)),
                ('c2m', models.IntegerField(default=0)),
                ('c2p', models.IntegerField(default=0)),
                ('p2c', models.IntegerField(default=0)),
                ('c2p_io', models.IntegerField(default=0)),
                ('c2p_mem', models.IntegerField(default=0)),
                ('c2p_special', models.IntegerField(default=0)),
                ('cl0_l2_hit', models.IntegerField(default=0)),
                ('cl0_l2_miss', models.IntegerField(default=0)),
                ('cl1_l2_hit', models.IntegerField(default=0)),
                ('cl1_l2_miss', models.IntegerField(default=0)),
                ('hotwire', models.IntegerField(default=0)),
                ('fsbc_request', models.IntegerField(default=0)),
                ('fsbc_trigger', models.IntegerField(default=0)),
                ('cl0_msr_read', models.IntegerField(default=0)),
                ('cl0_msr_write', models.IntegerField(default=0)),
                ('cl1_msr_read', models.IntegerField(default=0)),
                ('cl1_msr_write', models.IntegerField(default=0)),
                ('interrupt_ipi', models.IntegerField(default=0)),
                ('interrupt_msi', models.IntegerField(default=0)),
                ('interrupt_sb', models.IntegerField(default=0)),
                ('c2m_s1', models.IntegerField(default=0)),
                ('c2p_s1', models.IntegerField(default=0)),
                ('p2c_s1', models.IntegerField(default=0)),
                ('c2p_io_s1', models.IntegerField(default=0)),
                ('c2p_mem_s1', models.IntegerField(default=0)),
                ('c2p_special_s1', models.IntegerField(default=0)),
                ('cl0_l2_hit_s1', models.IntegerField(default=0)),
                ('cl0_l2_miss_s1', models.IntegerField(default=0)),
                ('cl1_l2_hit_s1', models.IntegerField(default=0)),
                ('cl1_l2_miss_s1', models.IntegerField(default=0)),
                ('hotwire_s1', models.IntegerField(default=0)),
                ('fsbc_request_s1', models.IntegerField(default=0)),
                ('fsbc_trigger_s1', models.IntegerField(default=0)),
                ('cl0_msr_read_s1', models.IntegerField(default=0)),
                ('cl0_msr_write_s1', models.IntegerField(default=0)),
                ('cl1_msr_read_s1', models.IntegerField(default=0)),
                ('cl1_msr_write_s1', models.IntegerField(default=0)),
                ('interrupt_ipi_s1', models.IntegerField(default=0)),
                ('interrupt_msi_s1', models.IntegerField(default=0)),
                ('interrupt_sb_s1', models.IntegerField(default=0)),
                ('vpi_s0_s1', models.IntegerField(default=0)),
                ('vpi_s1_s0', models.IntegerField(default=0)),
                ('jtag', models.IntegerField(default=0)),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='date add')),
            ],
        ),
        migrations.CreateModel(
            name='VectorIssue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vector', models.CharField(db_index=True, max_length=80, unique=True, verbose_name='vector_name')),
                ('snippet', models.CharField(default='', max_length=100, verbose_name='abstract')),
                ('content', models.CharField(max_length=320, verbose_name='content')),
                ('src_path', models.CharField(default='', max_length=150, verbose_name='vector path')),
                ('wave_path', models.CharField(default='', max_length=150, verbose_name='waveform path')),
                ('log_path', models.CharField(default='', max_length=150, verbose_name='log path')),
                ('reason', models.CharField(choices=[('IN', 'unknown'), ('RE', 'real bug'), ('EN', 'environment issue'), ('VC', 'vector issue'), ('PF', 'performance issue')], default='IN', max_length=2)),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='date published')),
                ('active', models.BooleanField(default=True, verbose_name='Bug opened')),
                ('set_top', models.BooleanField(default=True, verbose_name='Set top')),
                ('project', models.CharField(default='', max_length=20, verbose_name='project')),
                ('design_git', models.CharField(default='-', max_length=100, verbose_name='design git version')),
                ('env_git', models.CharField(default='-', max_length=100, verbose_name='env git version')),
                ('design_git_date', models.CharField(default='-', max_length=100, verbose_name='env git version')),
                ('env_git_date', models.CharField(default='-', max_length=100, verbose_name='env git version')),
                ('modified_time', models.DateTimeField(auto_now=True, verbose_name='date changed')),
                ('bugowner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='regression.Category')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='vector',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='regression.VectorIssue', verbose_name='vector'),
        ),
    ]
