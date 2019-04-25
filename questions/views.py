# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic.edit import CreateView
from questions.models import *
from data.models import Sensor, SensorKind
from django.shortcuts import get_object_or_404
import random
from django.shortcuts import redirect, render

# Create your views here.
class AnswerCreate(CreateView):
    model = Answers
    fields = ["answer"]

    def form_valid(self, form):
        question = get_object_or_404(Questions, pk=self.randomQuestion)
        form.instance.question = question
        sensor = get_object_or_404(Sensor, pk=self.sensor)
        form.instance.sensor = sensor
        return super(AnswerCreate,self).form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super(AnswerCreate, self).get_context_data(**kwargs)
        ctx['question'] = get_object_or_404(Questions, pk=self.randomQuestion)
        return ctx

    def get_form(self,*args, **kwargs):
        form = super(AnswerCreate, self).get_form(*args, **kwargs)
        form.fields['answer'].queryset = PossibleAnswers.objects.filter(questions__id__exact=self.randomQuestion)
        return form

    def dispatch(self, request, *args, **kwargs):
        self.sensor = get_object_or_404(Sensor, pk=kwargs['sensor_id'])
        self.sensor = kwargs['sensor_id']
        self.randomQuestion = get_object_or_404(Questions, pk=kwargs['sensor_id'])
        self.randomQuestion = kwargs['question_id']
        return super(AnswerCreate,self).dispatch(request,*args,**kwargs)


def randomQuestion( sensor_id):
    questions = Questions.objects.filter(sensorKind__sensors = sensor_id)
    return random.choice(questions)

def preQuestion(request, sensor_id):
        question = randomQuestion(sensor_id)
        url = request.path+'/' +str(question.pk)
        return redirect(url)
