# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-04-18 12:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionKind',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=75, verbose_name='Descri\xe7\xe3o')),
            ],
        ),
        migrations.RemoveField(
            model_name='questions',
            name='weight',
        ),
        migrations.AlterField(
            model_name='questions',
            name='description',
            field=models.CharField(max_length=75, verbose_name='Descri\xe7\xe3o'),
        ),
        migrations.AlterField(
            model_name='questions',
            name='sensorKind',
            field=models.ManyToManyField(to='data.SensorKind', verbose_name='Tipo de sensor'),
        ),
        migrations.AddField(
            model_name='questions',
            name='questionKind',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='questions.QuestionKind'),
        ),
    ]
