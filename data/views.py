# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import redirect
from django.http import StreamingHttpResponse, HttpResponse
from .functionalities import *

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
	return StreamingHttpResponse("data pagina principal")
