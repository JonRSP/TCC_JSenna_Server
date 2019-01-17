# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import redirect, render
from django.http import StreamingHttpResponse, HttpResponse
from .functionalities import *
from .models import *

from datetime import datetime, timedelta, time
from .functionalities import generateData

# Create your views here.
varAux = datetime.now()-timedelta(1)
dateReadingInfo=0
dados={}


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
	context = {'numReadings':numReadings , 'info':info, 'pieData':pieData}
	return render(request, 'data/index.html', context)

def sensorDetail(request, sensor_id):
	global varAux
	global dateReadingInfo
	global dados
	sensor = Sensor.objects.get(id=sensor_id)
	lastTempReading = Reading.objects.filter(sensor_id__exact=sensor_id, sensorKind__description__iexact='Temperatura').latest('moment')
	lastUmidReading = Reading.objects.filter(sensor_id__exact=sensor_id, sensorKind__description__iexact='Umidade').latest('moment')
	if(varAux.date() != datetime.now().date() or not dados):
		dateReadingInfo = Reading.objects.filter(sensor_id__exact = sensor_id).dates('moment','day')
		varAux = datetime.now()
		dados = generateData(dateReadingInfo)
	context = {'id':sensor_id,'dateCountInfo':dados[str(sensor_id)][1], 'tempAverage':dados[str(sensor_id)][2], 'umidAverage':dados[str(sensor_id)][3], 'lastTempReading':lastTempReading, 'lastUmidReading':lastUmidReading, 'sensor':sensor}
	return render(request, 'data/sensor.html', context)
