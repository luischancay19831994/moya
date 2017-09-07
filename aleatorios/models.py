# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models.fields import FloatField


# Create your models here.

class Calculator(models.Model):
    primeiro = FloatField()
    segundo = FloatField()


class Lineal_metodo(models.Model):
    a = FloatField()
    xo = FloatField()
    c = FloatField()
    m = FloatField()
    n = FloatField()


class Multiplicativo_metodo(models.Model):
    a = FloatField()
    xo = FloatField()
    m = FloatField()
    n = FloatField()

    class Cuadrado_metodo(models.Model):
        x = FloatField()
        d = FloatField()
        nr = FloatField()
