# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.template import loader
from django.views.generic.edit import UpdateView
from data.models import Sensor


# Create your views here.

def index(request):
	template = loader.get_template('data/homepage.html')
	context={}
	return HttpResponse(template.render(context,request))

class sensorEdit(UpdateView):
	model = Sensor
	fields = ['description']
	success_url = 'http://jsenna.xyz/data'
