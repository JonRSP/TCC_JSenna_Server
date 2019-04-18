# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import *
from django.contrib import admin

# Register your models here.
admin.site.register(Questions)
admin.site.register(PossibleAnswers)
admin.site.register(Answers)
admin.site.register(QuestionKind)
