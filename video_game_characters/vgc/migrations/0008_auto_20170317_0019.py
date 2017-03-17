# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2017-03-17 00:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vgc', '0007_auto_20170313_2316'),
    ]

    operations = [
        migrations.CreateModel(
            name='ListElement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)])),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='character',
            name='picture',
            field=models.ImageField(blank=True, upload_to='char_images'),
        ),
        migrations.AddField(
            model_name='rating',
            name='character',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vgc.Character'),
        ),
        migrations.AddField(
            model_name='rating',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vgc.UserProfile'),
        ),
        migrations.AddField(
            model_name='listelement',
            name='character',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vgc.Character'),
        ),
        migrations.AddField(
            model_name='listelement',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vgc.UserProfile'),
        ),
        migrations.AddField(
            model_name='character',
            name='ratings',
            field=models.ManyToManyField(through='vgc.Rating', to='vgc.UserProfile'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='list',
            field=models.ManyToManyField(through='vgc.ListElement', to='vgc.Character'),
        ),
        migrations.AlterUniqueTogether(
            name='rating',
            unique_together=set([('user', 'character')]),
        ),
        migrations.AlterUniqueTogether(
            name='listelement',
            unique_together=set([('user', 'character'), ('user', 'position')]),
        ),
    ]
