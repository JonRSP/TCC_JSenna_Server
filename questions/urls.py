from django.conf.urls import url
from . import views


urlpatterns = [
	# url(r'^$', views.index, name='indexQuestions'),
    url(r'^addAnswer/(?P<sensor_id>[0-9]+)/(?P<question_id>[0-9]+)$', views.AnswerCreate.as_view(success_url="../../../data"), name='answer'),
    url(r'^addAnswer/(?P<sensor_id>[0-9]+)$', views.preQuestion, name='pre-question'),
]
