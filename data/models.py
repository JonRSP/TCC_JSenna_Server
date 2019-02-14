# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Sensor(models.Model):
	description = models.CharField(max_length=50, null=True,verbose_name='Descrição'	)
	longitude = models.DecimalField(max_digits=5, decimal_places=2, null=True)
	latitude = models.DecimalField(max_digits=5, decimal_places=2, null=True)
	score = models.DecimalField(max_digits=3, decimal_places=2)

	def __str__(self):
		return self.description

class SensorKind(models.Model):
	description = models.CharField(max_length=50)
	unit = models.CharField(max_length=5, null=True)
	minValue = models.DecimalField(max_digits=7,decimal_places=2, null=True)
	maxValue = models.DecimalField(max_digits=7,decimal_places=2, null=True)
	sensors = models.ManyToManyField(Sensor)

    	def __str__(self):
    		return self.description

class Reading(models.Model):
	id = models.BigAutoField(primary_key=True)
	sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
	sensorKind = models.ForeignKey(SensorKind, on_delete=models.CASCADE)
	value = models.FloatField()
	moment = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.sensorKind)+' no valor de '+str(self.value)+ ' em ' +str(self.moment)
