from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg
from datetime import datetime, timedelta
import threading

count = {}

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

def addReading(received_data, sensorID):
	number = 25
	sensorObj = Sensor.objects.get(id=sensorID)
	# if(not str(sensorID) in count):
	# 	count.update({str(sensorID):0})
	# count[str(sensorID)] =  (count[str(sensorID)]+1)%number
	# if( count[str(sensorID)] == 0):
	# 	threadScore = threading.Thread(target=calculateScore,args=(sensorID,number))
	# 	threadScore.start()
	for kind, reading in zip(received_data['sensorKind'], received_data['value']):
		kindObj = SensorKind.objects.get(description=kind)
		newReading = Reading(sensor=sensorObj, sensorKind=kindObj, value=reading)
		newReading.save()

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

def calculateScore(id, number):
	now = datetime.now()
	delta = timedelta(days=10,minutes=30,seconds=now.second, microseconds=now.microsecond)
	lastAvgUmid = Reading.objects.filter(sensor_id__exact=id, sensorKind__description__iexact='Umidade').order_by('-id')[:number].aggregate(Avg('value'))['value__avg']
	timeAvgUmid = Reading.objects.filter(sensor_id__exact=id, sensorKind__description__iexact='Umidade',moment__gte=(now-delta), moment__time__gte=(now-delta).time(),moment__time__lt=(now+delta).time()).aggregate(Avg('value'))['value__avg']
	lastAvgTemp = Reading.objects.filter(sensor_id__exact=id, sensorKind__description__iexact='Temperatura').order_by('-id')[:number].aggregate(Avg('value'))['value__avg']
	timeAvgTemp = Reading.objects.filter(sensor_id__exact=id, sensorKind__description__iexact='Temperatura',moment__gte=(now-delta) , moment__time__gte=(now-delta).time(),moment__time__lt=(now+delta).time()).aggregate(Avg('value'))['value__avg']
	scoreUmid = (1/(abs((lastAvgUmid/timeAvgUmid)-1)+1))*5
	scoreTemp = (1/(abs((lastAvgTemp/timeAvgTemp)-1)+1))*5
	score = 2/((1/scoreUmid)+(1/scoreTemp))
	sensor = Sensor.objects.get(id__exact=id)
	sensor.score = (float(sensor.score)+score)/2
	sensor.save()
