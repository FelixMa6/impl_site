# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-22 02:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaseItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summit_time', models.CharField(default='', max_length=20, verbose_name='summit_time')),
                ('project', models.CharField(default='', max_length=20, verbose_name='project')),
                ('check_item', models.CharField(default='', max_length=20, verbose_name='check_item')),
                ('partition', models.CharField(default='', max_length=20, verbose_name='partition')),
                ('fail_total_number', models.CharField(default='', max_length=20, verbose_name='fail_total_number')),
                ('design_git_number', models.CharField(default='', max_length=50, verbose_name='design_git')),
                ('design_git_date', models.CharField(default='', max_length=50, verbose_name='design_git_date')),
            ],
        ),
        migrations.CreateModel(
            name='OwnerCase',
            fields=[
                ('baseitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='release_check.BaseItem')),
                ('owner', models.CharField(default='', max_length=20, verbose_name='owner')),
                ('fail_number', models.CharField(default='', max_length=20, verbose_name='fail_number')),
                ('log_path', models.CharField(default='', max_length=150, verbose_name='log_path')),
                ('content', models.TextField(default='', max_length=3000, verbose_name='content')),
            ],
            bases=('release_check.baseitem',),
        ),
    ]