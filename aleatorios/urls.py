from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^$', views.metodo_lineal, name='metodo_lineal'),

]
