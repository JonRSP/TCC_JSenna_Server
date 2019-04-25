# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from data.models import *
#from ..data.models import Sensor


# Create your models here.

class QuestionKind(models.Model):
	description = models.CharField(max_length=75, verbose_name='Descrição')

	def __str__(self):
		return self.description

class Questions(models.Model):
	description = models.CharField(max_length=75,verbose_name='Descrição')
	sensorKind = models.ManyToManyField(SensorKind,verbose_name='Tipo de sensor')
	questionKind = models.ForeignKey(QuestionKind, on_delete=models.CASCADE, null=True)

	def __str__(self):
		return self.description

# class QuestionKind(models.Model):
# 	description = models.CharField(max_length=75, verbose_name='Descrição')

class PossibleAnswers(models.Model):
	description = models.CharField(max_length=50)
	questions = models.ManyToManyField(Questions)

	def __str__(self):
		return self.description


class Answers(models.Model):
	sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
	question = models.ForeignKey(Questions, on_delete=models.CASCADE)
	answer = models.ForeignKey(PossibleAnswers, on_delete=models.CASCADE,verbose_name='Resposta', null=False)
	moment = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.sensor) +' '+ str(question)+' '+ str(answer)+' '+ str(moment)
