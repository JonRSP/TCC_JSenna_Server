from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='indexData'),
	url(r'^addReading/', views.postData, name='postData'),
]
