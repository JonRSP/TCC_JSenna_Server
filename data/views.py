# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import redirect, render
from django.http import StreamingHttpResponse, HttpResponse
from .functionalities import *
from .models import *

from datetime import datetime
from .functionalities import generateAvgData, generateLastData, calculateScore

# Create your views here.
varAux = datetime.now()-timedelta(1)
varAux2 = datetime.now()-timedelta(hours=1)
dateReadingInfo=0
dadosAvg = {}
dadosLast = {}


@csrf_exempt
def postData(request):
	if (request.method=='POST'):
		received_data = json.loads(request.body)
		sensorID = received_data['sensorID']
		if(received_data['sensorID']==0):
			sensorID = addSensor(received_data)
		addReading(received_data, sensorID)
		if(received_data['sensorID']==0):
			return StreamingHttpResponse(str(sensorID))
		else:
			return StreamingHttpResponse("0")
	else:
		return redirect('indexData')

def index(request):
	sensorInfo = Sensor.objects.all()
	numReadings = Reading.objects.count()
	sensorReadingInfo = []
	lastReading=[]
	for sensor in sensorInfo:
		sensorReadingInfo.append(Reading.objects.filter(sensor_id__exact = sensor.id).count())
		lastReading.append(Reading.objects.filter(sensor_id__exact=sensor.id).latest('moment'))
	info = zip(sensorInfo, sensorReadingInfo, lastReading)
	pieData =[('sensor', 'quantidade')]
	for data in info:
		pieData.append((data[0].description, data[1]))
	context = {
	 'numReadings':numReadings,
	 'info':info,
	 'pieData':pieData
	 }
	return render(request, 'data/index.html', context)

def sensorDetail(request, sensor_id):
	global varAux
	global varAux2
	global dateReadingInfo
	global dadosAvg
	global dadosLast
	now = datetime.now()
	sensor = Sensor.objects.get(id=sensor_id)
	lastTempReading = Reading.objects.filter(sensor_id__exact=sensor_id, sensorKind__description__iexact='Temperatura').latest('moment')
	lastUmidReading = Reading.objects.filter(sensor_id__exact=sensor_id, sensorKind__description__iexact='Umidade').latest('moment')
	if(varAux2.hour != now.hour or not dadosLast or str(sensor_id) not in dadosLast):
		if(varAux2.hour != now.hour and str(sensor_id) in dadosLast):
			dadosLast[str(sensor_id)] = generateLastData(sensor_id)
		else:
			dadosLast.update({str(sensor_id):generateLastData(sensor_id)})
		varAux2 = now
	if((varAux.date() != now.date() or not dadosAvg) or str(sensor_id) not in dadosAvg):
	 	dateReadingInfo = Reading.objects.filter(sensor_id__exact = sensor_id).dates('moment','day')
	# 	if (varAux.date() != now.date() and str(sensor_id) in dadosAvg):
	# 		dadosAvg[str(sensor_id)]=generateAvgData(dateReadingInfo, sensor_id)
	# 	else:
	# 		dadosAvg.update({str(sensor_id):generateAvgData(dateReadingInfo, sensor_id)})
		varAux = now
	dadosGraficos = zip(
	# dadosAvg[str(sensor_id)][2],
	#  dadosAvg[str(sensor_id)][3],
	dadosLast[str(sensor_id)][1],
	dadosLast[str(sensor_id)][2])
	context = {
	 'id':sensor_id,
	 'dateCountInfo':dateReadingInfo,
	 'lastTempReading':lastTempReading,
	 'lastUmidReading':lastUmidReading,
	 'sensor':sensor,
	 'dadosGraficos': dadosGraficos
	 }
	return render(request, 'data/sensor.html', context)
