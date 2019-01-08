# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from data.models import *
#from ..data.models import Sensor


# Create your models here.

class Questions(models.Model):
	description = models.CharField(max_length=75)
	weight = models.IntegerField()
	sensorKind = models.ManyToManyField(SensorKind)

	def __str__(self):
		return self.description

class PossibleAnswers(models.Model):
	description = models.CharField(max_length=50)
	questions = models.ManyToManyField(Questions)


class Answers(models.Model):
	sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
	question = models.ForeignKey(Questions, on_delete=models.CASCADE)
	answer = models.ForeignKey(PossibleAnswers, on_delete=models.CASCADE)
	moment = models.DateTimeField(auto_now_add=True)

