from django.conf.urls import url, include
from django.views.generic import ListView, DetailView
from . import views

urlpatterns = [
	url(r'^$', views.index),
        #url(r'^submit/', views.submit, name='submit'),

]
