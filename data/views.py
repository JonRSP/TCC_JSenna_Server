# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render
from django.http import StreamingHttpResponse, HttpResponse

# Create your views here.

@csrf_exempt
def index(request):
	if (request.method=='POST'):
		received_data = json.loads(request.body)
		sensorID=received_data['sensorID']
		if(received_data['sensorID']==0):
			#do stuff
			pass
		if(received_data['sensorID']==0):
			return StreamingHttpResponse(str(newSensor.id))
		
		else:
			return StreamingHttpResponse("0")
	else:
		return StreamingHttpResponse("0")
