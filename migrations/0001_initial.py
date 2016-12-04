# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.CharField(max_length=16, verbose_name=b'\xe5\x88\x86\xe7\xb1\xbb')),
                ('category_name', models.CharField(max_length=32, null=True, verbose_name=b'\xe7\xb1\xbb\xe5\x88\xab')),
            ],
            options={
                'verbose_name': '\u5206\u7c7b',
                'verbose_name_plural': '\u5206\u7c7b',
            },
        ),
        migrations.CreateModel(
            name='HotWordTrace',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('word', models.CharField(max_length=32, verbose_name=b'\xe8\xaf\x8d\xe8\xaf\xad')),
                ('time', models.DateField(auto_now_add=True, verbose_name=b'\xe6\x8e\xa8\xe8\x8d\x90\xe6\x97\xb6\xe9\x97\xb4')),
                ('rank', models.IntegerField(default=0, verbose_name=b'\xe6\x8e\x92\xe5\xba\x8f')),
                ('reliable', models.BooleanField(default=True, verbose_name=b'reliable')),
                ('score', models.FloatField(default=0.0, verbose_name=b'\xe6\x8e\xa8\xe8\x8d\x90\xe5\x9b\xa0\xe5\xad\x90')),
                ('note', models.CharField(default=b'additional note', max_length=128, verbose_name=b'\xe5\xa4\x87\xe6\xb3\xa8')),
            ],
            options={
                'verbose_name': 'hotwordtrace',
                'verbose_name_plural': 'hotwordtrace',
            },
        ),
        migrations.CreateModel(
            name='MeaninglessWord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('word', models.CharField(unique=True, max_length=32, verbose_name=b'\xe8\xaf\x8d\xe8\xaf\xad')),
            ],
            options={
                'verbose_name': 'Meaningless Word',
                'verbose_name_plural': 'Meaningless Word',
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
                ('section', models.CharField(default=b'headline', max_length=32, verbose_name=b'\xe5\x88\x86\xe7\xb1\xbb')),
                ('hash_digest', models.CharField(unique=True, max_length=64, verbose_name=b'\xe5\x93\x88\xe5\xb8\x8c\xe6\x91\x98\xe8\xa6\x81')),
                ('cover', models.CharField(default=b'/static/news/image/newsCover.jpg', max_length=512, verbose_name=b'\xe5\xb0\x81\xe9\x9d\xa2')),
                ('site', models.CharField(default=b'getqiu.com', max_length=32, verbose_name=b'\xe6\x96\xb0\xe9\x97\xbb\xe6\x9d\xa5\xe6\xba\x90')),
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
            name='SearchTrace',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('expression', models.CharField(max_length=64, verbose_name=b'\xe6\x90\x9c\xe7\xb4\xa2\xe8\xa1\xa8\xe8\xbe\xbe\xe5\xbc\x8f')),
                ('time', models.DateTimeField(auto_now=True, verbose_name=b'\xe6\x90\x9c\xe7\xb4\xa2\xe6\x97\xb6\xe9\x97\xb4', db_index=True)),
                ('day', models.DateField(auto_now=True, verbose_name=b'\xe6\x90\x9c\xe7\xb4\xa2\xe6\x97\xa5\xe6\x9c\x9f')),
                ('ip', models.CharField(max_length=40, verbose_name=b'IP \xe5\x9c\xb0\xe5\x9d\x80')),
            ],
            options={
                'verbose_name': 'searchTrace',
                'verbose_name_plural': 'searchTrace',
            },
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(unique=True, max_length=32, verbose_name=b'option Name')),
                ('option', models.CharField(default=b'0', max_length=128, verbose_name=b'value')),
                ('comment', models.CharField(default=b'COMMENT', max_length=512, verbose_name=b'\xe6\xb3\xa8\xe9\x87\x8a')),
            ],
            options={
                'verbose_name': 'settings',
                'verbose_name_plural': 'settings',
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
            ],
            options={
                'verbose_name': '\u6807\u7b7e',
                'verbose_name_plural': '\u6807\u7b7e',
            },
        ),
        migrations.CreateModel(
            name='TagsNews',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('news', models.ForeignKey(verbose_name=b'\xe6\x96\xb0\xe9\x97\xbb', to='news.News')),
                ('tags', models.ForeignKey(verbose_name=b'\xe6\xa0\x87\xe7\xad\xbe', to='news.Tags')),
            ],
            options={
                'db_table': 'news_tags_news',
                'verbose_name': '\u65b0\u95fb\u4e0e\u6807\u7b7e\u5173\u7cfb',
                'verbose_name_plural': '\u65b0\u95fb\u4e0e\u6807\u7b7e\u5173\u7cfb',
            },
        ),
        migrations.AddField(
            model_name='tags',
            name='news',
            field=models.ManyToManyField(to='news.News', verbose_name=b'\xe5\x85\xb3\xe8\x81\x94\xe5\x86\x85\xe5\xae\xb9', through='news.TagsNews'),
        ),
        migrations.AlterIndexTogether(
            name='searchtrace',
            index_together=set([('ip', 'day')]),
        ),
        migrations.AlterIndexTogether(
            name='news',
            index_together=set([('id', 'news_time', 'rank'), ('news_time', 'rank'), ('section', 'news_time', 'rank')]),
        ),
        migrations.AlterIndexTogether(
            name='hotwordtrace',
            index_together=set([('time', 'word', 'reliable')]),
        ),
        migrations.AddField(
            model_name='category',
            name='news',
            field=models.ManyToManyField(to='news.News', verbose_name=b'\xe5\x88\x86\xe7\xb1\xbb\xe5\x86\x85\xe5\xae\xb9'),
        ),
        migrations.AlterUniqueTogether(
            name='tagsnews',
            unique_together=set([('news', 'tags')]),
        ),
    ]
