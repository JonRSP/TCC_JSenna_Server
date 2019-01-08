from .models import *
from django.core.exceptions import ObjectDoesNotExist

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
