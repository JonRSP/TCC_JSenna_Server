# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import redirect, render
from django.http import StreamingHttpResponse, HttpResponse
from .functionalities import *
from .models import *
from django.db.models import Count

# Create your views here.

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
	dateReadingInfo = Reading.objects.filter(sensor_id__exact = sensor_id).dates('moment','day')
	countInfo = []
	for moment in dateReadingInfo:
		countInfo.append(Reading.objects.filter(sensor_id__exact = sensor_id, moment__year=moment.year, moment__month=moment.month,moment__day=moment.day).count())
	dateCountInfo= zip(dateReadingInfo,countInfo)
	print(dateCountInfo)
	context = {'id':sensor_id,'dateCountInfo':dateCountInfo}
	return render(request, 'data/sensor.html', context)
