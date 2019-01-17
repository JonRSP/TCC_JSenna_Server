from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg


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
	sensorObj = Sensor.objects.get(id=sensorID)
	for kind, reading in zip(received_data['sensorKind'], received_data['value']):
		kindObj = SensorKind.objects.get(description=kind)
		newReading = Reading(sensor=sensorObj, sensorKind=kindObj, value=reading)
		newReading.save()

def generateData(dates):
	dados = {}
	sensores = Sensor.objects.all()
	for sensor in sensores:
		countInfo =[]
		tempAverage =[]
		umidAverage =[]
		for day in dates:
			countInfo.append(Reading.objects.filter(sensor_id__exact = sensor.id, moment__year=day.year, moment__month=day.month,moment__day=day.day).count())
		for hour in range(0, 24):
			tempAverage.append(Reading.objects.filter(sensor_id__exact=sensor.id,moment__hour=hour, sensorKind__description__iexact='Temperatura').aggregate(Avg('value'))['value__avg'])
		tempAverage = zip(range(0,24), tempAverage)
		for hour in range(0, 24):
			umidAverage.append(Reading.objects.filter(sensor_id__exact=sensor.id,moment__hour=hour, sensorKind__description__iexact='Umidade').aggregate(Avg('value'))['value__avg'])
		umidAverage = zip(range(0,24), umidAverage)
		aux = (sensor.id, zip(dates,countInfo), tempAverage, umidAverage )
		dados.update({str(sensor.id):aux})
	return dados
