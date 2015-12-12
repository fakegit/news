# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccountType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('account', models.CharField(max_length=128, verbose_name=b'\xe8\xb4\xa6\xe6\x88\xb7\xe7\xb1\xbb\xe5\x9e\x8b')),
                ('complex_level', models.CharField(max_length=16, verbose_name=b'\xe5\xa4\x8d\xe6\x9d\x82\xe5\xba\xa6', choices=[(b'0', b'\xe9\x9a\x8f\xe6\x84\x8f\xe7\x88\xac\xe5\x8f\x96'), (b'1', b'\xe9\x9c\x80\xe8\xa6\x81\xe7\x99\xbb\xe5\xbd\x95'), (b'2', b'\xe7\x99\xbb\xe5\xbd\x95+\xe9\xaa\x8c\xe8\xaf\x81\xe7\xa0\x81'), (b'3', b'\xe9\xaa\x8c\xe8\xaf\x81\xe7\xa0\x81\xe8\xaf\x86\xe5\x88\xab\xe5\x9b\xb0\xe9\x9a\xbe'), (b'4', b'\xe7\x99\xbb\xe5\xbd\x95\xe6\x9c\xba\xe5\x88\xb6\xe5\xa4\x8d\xe6\x9d\x82'), (b'5', b'\xe9\x9c\x80\xe4\xba\xba\xe5\xb7\xa5\xe6\xa8\xa1\xe5\xbc\x8f')])),
            ],
            options={
                'verbose_name': '\u652f\u6301\u7f51\u7ad9',
                'verbose_name_plural': '\u652f\u6301\u7f51\u7ad9',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.CharField(max_length=16, verbose_name=b'\xe5\x88\x86\xe7\xb1\xbb')),
            ],
            options={
                'verbose_name': '\u5206\u7c7b',
                'verbose_name_plural': '\u5206\u7c7b',
            },
        ),
        migrations.CreateModel(
            name='CrawlerTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('task_type', models.CharField(default=b'1', max_length=10, verbose_name=b'\xe4\xbb\xbb\xe5\x8a\xa1\xe7\xb1\xbb\xe5\x9e\x8b', choices=[(b'1', b'\xe9\x95\xbf\xe6\x9c\x9f\xe4\xbb\xbb\xe5\x8a\xa1'), (b'0', b'\xe4\xb8\x80\xe6\xac\xa1\xe6\x80\xa7\xe4\xbb\xbb\xe5\x8a\xa1')])),
                ('execute_time', models.DateTimeField(verbose_name=b'\xe6\x89\xa7\xe8\xa1\x8c\xe6\x97\xb6\xe9\x97\xb4')),
                ('account', models.CharField(default=b'get_site_info', max_length=128, verbose_name=b'\xe7\x9b\x91\xe8\xa7\x86\xe5\xb8\x90\xe5\x8f\xb7')),
                ('account_type', models.ForeignKey(verbose_name=b'\xe5\xb8\x90\xe5\x8f\xb7\xe7\xb1\xbb\xe5\x9e\x8b', to='news.AccountType')),
            ],
            options={
                'verbose_name': '\u722c\u866b\u4efb\u52a1\u7c7b\u8868',
                'verbose_name_plural': '\u722c\u866b\u4efb\u52a1\u7c7b\u8868',
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128, verbose_name=b'\xe6\x96\xb0\xe9\x97\xbb\xe6\xa0\x87\xe9\xa2\x98')),
                ('rank', models.IntegerField(verbose_name=b'\xe6\x96\xb0\xe9\x97\xbbranking')),
                ('news_time', models.DateField(verbose_name=b'\xe5\x8f\x91\xe5\xb8\x83\xe6\x97\xb6\xe9\x97\xb4')),
                ('publisher', models.CharField(max_length=128, verbose_name=b'\xe6\x96\xb0\xe9\x97\xbb\xe6\x9d\xa5\xe6\xba\x90')),
                ('news_url', models.URLField(verbose_name=b'\xe6\x96\xb0\xe9\x97\xbb\xe7\xbd\x91\xe9\xa1\xb5\xe9\x93\xbe\xe6\x8e\xa5')),
                ('content', ckeditor.fields.RichTextField(verbose_name=b'\xe6\x96\xb0\xe9\x97\xbb\xe5\x86\x85\xe5\xae\xb9')),
                ('hash_digest', models.CharField(unique=True, max_length=64, verbose_name=b'\xe5\x93\x88\xe5\xb8\x8c\xe6\x91\x98\xe8\xa6\x81')),
            ],
            options={
                'verbose_name': '\u65b0\u95fb',
                'verbose_name_plural': '\u65b0\u95fb',
            },
        ),
        migrations.CreateModel(
            name='NewsStatistic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('click', models.IntegerField(default=0, verbose_name=b'\xe7\x82\xb9\xe5\x87\xbb\xe6\xac\xa1\xe6\x95\xb0')),
                ('news', models.OneToOneField(verbose_name=b'\xe6\x96\xb0\xe9\x97\xbb', to='news.News')),
            ],
            options={
                'verbose_name': '\u65b0\u95fb\u4fe1\u606f\u7edf\u8ba1',
                'verbose_name_plural': '\u65b0\u95fb\u4fe1\u606f\u7edf\u8ba1',
            },
        ),
        migrations.CreateModel(
            name='Suggestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('visitor', models.GenericIPAddressField(verbose_name=b'\xe5\xbb\xba\xe8\xae\xae\xe8\x80\x85ip')),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe6\x97\xb6\xe9\x97\xb4')),
                ('title', models.CharField(max_length=128, verbose_name=b'\xe5\xbb\xba\xe8\xae\xae\xe6\xa0\x87\xe9\xa2\x98')),
                ('contact', models.CharField(max_length=64, verbose_name=b'\xe8\x81\x94\xe7\xb3\xbb\xe6\x96\xb9\xe5\xbc\x8f')),
                ('detail', ckeditor.fields.RichTextField(verbose_name=b'\xe5\xbb\xba\xe8\xae\xae\xe5\x86\x85\xe5\xae\xb9')),
            ],
            options={
                'verbose_name': '\u5efa\u8bae\u4e0e\u610f\u89c1',
                'verbose_name_plural': '\u5efa\u8bae\u4e0e\u610f\u89c1',
            },
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tag', models.CharField(max_length=32, verbose_name=b'\xe6\xa0\x87\xe7\xad\xbe')),
                ('tag_hash', models.CharField(unique=True, max_length=64, verbose_name=b'\xe6\xa0\x87\xe7\xad\xbe\xe6\xa0\x87\xe7\xa4\xba')),
                ('search_times', models.IntegerField(default=0, verbose_name=b'\xe6\x90\x9c\xe7\xb4\xa2\xe6\xac\xa1\xe6\x95\xb0')),
                ('included_items_num', models.IntegerField(default=0, verbose_name=b'tag\xe6\x89\x80\xe5\x90\xab\xe6\x9d\xa1\xe7\x9b\xae\xe6\x95\xb0\xe9\x87\x8f')),
                ('news', models.ManyToManyField(to='news.News', verbose_name=b'\xe5\x85\xb3\xe8\x81\x94\xe5\x86\x85\xe5\xae\xb9')),
            ],
            options={
                'verbose_name': '\u6807\u7b7e',
                'verbose_name_plural': '\u6807\u7b7e',
            },
        ),
        migrations.AddField(
            model_name='category',
            name='news',
            field=models.ManyToManyField(to='news.News', verbose_name=b'\xe5\x88\x86\xe7\xb1\xbb\xe5\x86\x85\xe5\xae\xb9'),
        ),
    ]
