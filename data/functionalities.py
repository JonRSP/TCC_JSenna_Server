# -*- coding: utf 8 -*-
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg
from datetime import datetime, timedelta
import threading

count = {}
#escalável
def addSensor(received_data):
	newSensor = Sensor(score=0)
	newSensor.save()
	newSensor.description = "Descricao temporaria sensor "+str(newSensor.id)
	newSensor.save()
	for kind in received_data['sensorKind']:
		try:
			kindObj = SensorKind.objects.get(description=kind)
			kindObj.sensors.add(newSensor)
		except ObjectDoesNotExist:
			newKind = SensorKind(description=kind)
			newKind.save()
			newKind.sensors.add(newSensor)
	return newSensor.id

#escalavel
def addReading(received_data, sensorID):
	global count
	number = 15 #numero de leituras antes de calcular score novamente
	if(not str(sensorID) in count):
		count.update({str(sensorID):0})
	count[str(sensorID)] = (count[str(sensorID)]+1)%number
	sensorObj = Sensor.objects.get(id=sensorID)
	if( count[str(sensorID)] == 0):
		threadScore = threading.Thread(target=calculateScore,args=(sensorID,number))
		threadScore.start()
	for kind, reading in zip(received_data['sensorKind'], received_data['value']):
		kindObj = SensorKind.objects.get(description=kind)
		newReading = Reading(sensor=sensorObj, sensorKind=kindObj, value=reading)
		newReading.save()

#não escalavel
def generateAvgData(dates, sensor_id):
	countInfo =[]
	tempAverage =[]
	umidAverage =[]
	for day in dates:
		countInfo.append(Reading.objects.filter(sensor_id__exact = sensor_id, moment__year=day.year, moment__month=day.month,moment__day=day.day).count())
	for hour in range(0, 24):
		tempAverage.append((hour, Reading.objects.filter(sensor_id__exact=sensor_id,moment__hour=hour, sensorKind__description__iexact='Temperatura').aggregate(Avg('value'))['value__avg']))
		umidAverage.append((hour, Reading.objects.filter(sensor_id__exact=sensor_id,moment__hour=hour, sensorKind__description__iexact='Umidade').aggregate(Avg('value'))['value__avg']))
	return (sensor_id, zip(dates,countInfo), tempAverage, umidAverage )

#nao escalavel
def generateLastData(sensor_id):
	lastTempAvg = []
	lastUmidAvg = []
	now = datetime.now()
	today = now - timedelta(minutes=now.minute,seconds=now.second, microseconds=now.microsecond)
	yesterday = now - timedelta(days=1, minutes=now.minute,seconds=now.second, microseconds=now.microsecond)
	for hour in listOfHours(yesterday.hour):
		lastUmidAvg.append((hour, Reading.objects.filter(sensor_id__exact = sensor_id, moment__gte=yesterday, moment__lt=today, moment__hour=hour, sensorKind__description__iexact='Umidade').aggregate(Avg('value'))['value__avg']))
		lastTempAvg.append((hour, Reading.objects.filter(sensor_id__exact = sensor_id, moment__gte=yesterday, moment__lt=today, moment__hour=hour, sensorKind__description__iexact='Temperatura').aggregate(Avg('value'))['value__avg']))
	return (sensor_id, lastTempAvg, lastUmidAvg)

def listOfHours(begin):
	aux = []
	for i in range(0,24):
		aux.append((begin+i)%24)
	return aux

#calcula o score de um sensor - escalavel
def calculateScore(id,number):
	now = datetime.now()
	delta = timedelta(days=5,minutes=30,seconds=now.second, microseconds=now.microsecond)
	lastDelta = now - delta
	kinds = SensorKind.objects.filter(sensors__exact=id)
	scoreKind=0
	totalScore=0
	for kind in kinds:
		lastNAvg = Reading.objects.filter(sensor_id__exact=id, sensorKind__description__iexact=kind.description).order_by('-id')[:number].aggregate(Avg('value'))['value__avg']
		timeAvg = Reading.objects.filter(sensor_id__exact=id, sensorKind__description__iexact=kind.description,moment__gte=(lastDelta), moment__time__gte=(lastDelta).time(), moment__time__lt=(now+delta).time()).aggregate(Avg('value'))['value__avg']
		scoreKind = (1/(abs((lastNAvg/timeAvg)-1)+1))*5
		if(scoreKind > 4):
			if(checkErrorEqual(id, kind, 12)):
				totalScore += 99999999
			else:
				totalScore += 1/scoreKind
		else:
			totalScore += 1/scoreKind
	totalScore = len(kinds)/totalScore
	sensor = Sensor.objects.get(id__exact=id)
	sensor.score = (float(sensor.score)+totalScore)/2
	sensor.save()

#indica se as leituras das ultimas time horas foram iguais - escalavel
def checkErrorEqual(sensor_id, kind, time):
	now = datetime.now()
	deltaError = timedelta(hours = time)
	lastReadings = Reading.objects.filter(sensor_id__exact=sensor_id, sensorKind__description__iexact=kind.description,moment__gte=(now-deltaError), moment__time__gte=(now-deltaError).time()).values('value')
	maxVal = max(lastReadings)
	minVal = min(lastReadings)
	if (maxVal == minVal):
		return True
	else:
		return False
