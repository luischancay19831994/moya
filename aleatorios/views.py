import random

import numpy as np
import scipy.stats
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render

from .form import *

# Create your views here.

datos = []
datosMulti = []
datosCuad = []
mlineal = []
mcum = []
mmulti = []
mc = []


def op_metodo_lineal(a, xo, xoinicial, c, m, n):
    matriz = []

    print "n   Xo   (aXo + c) mod m   Xn + 1   Numero Rectangular      Random"

    for i in range(n):
        i += 1
        div = ((a * xo) + c) / m
        mod = ((a * xo) + c) % m
        nr = float((mod + .0) / (m - 1))
        #  print "%d   %d     %d  +   %d/%d      %d        %f                    %d " % (
        # i, xo, div, mod, m, mod, nr, random.randrange(n))
        rand = random.randrange(n)
        xox = xo
        xo = mod
        matriz.append(nr)
        mlineal.append(nr)
        datos.append([i, xox, div, mod, m, mod, nr, rand])
        if xoinicial == mod and i == m:
            print 'Generador congruencial mixto confiable'

        elif xoinicial == mod:
            print 'Generador congruencial mixto no confiable'

        elif xoinicial != mod and i == m:
            print 'Generador congruencial mixto no confiable'
            # return render('metodo_lineal.html', {'i': i, 'div': div, 'mod': mod, 'nr': nr,'rand':rand})

    return matriz


def metodo_multiplicativo(a, xo, xoinicial, m, n):
    matriz = []
    print "n   Xo   (a * Xo) mod m   Xn + 1   Numero Rectangular      Random"
    for i in range(n):
        i += 1
        div = (a * xo) / m
        mod = (a * xo) % m
        nr = float((mod + .0) / (m))
        print "%d   %d     %d  +   %d/%d      %d        %f                 %d " % (
            i, xo, div, mod, m, mod, nr, random.randrange(n))
        xox = xo
        xo = mod
        rand = random.randrange(n)

        matriz.append(nr)
        mmulti.append(nr)
        datosMulti.append([i, xox, div, mod, m, mod, nr, rand])

        if xoinicial == mod and i == m:
            print 'Generador congruencial Multiplicativo confiable'

        elif xoinicial == mod:
            print 'Generador congruencial Multiplicativo no confiable'

        elif xoinicial != mod and i == m:
            print 'Generador congruencial Multiplicativo no confiable'
    return matriz


def cuadrado_medio(x, d, n):
    matriz = []
    print "n     Xn       Xn^2      Xn + 1       Random"
    for i in range(n):
        i += 1
        cuadrado = x * x
        sobrante = int(len(str(cuadrado)) - d)
        dato = 0
        if sobrante % 2 == 0:
            extrae = (sobrante / 2)
            dato = str(cuadrado)[extrae: extrae + d]
        else:
            sobrante = int(len(str(cuadrado * 10)) - d)
            extrae = (sobrante / 2)
            dato = str(cuadrado)[extrae: extrae + d]
        print '%d    %d    %d    %d               %d' % (i, x, cuadrado, int(dato), random.randrange(n))
        rand = random.randrange(n)
        x = int(dato)
        datosCuad.append([i, x, cuadrado, dato, rand])
        mcum.append(x)
        matriz.append(x)
    return matriz


def principal(request):
    return HttpResponse("Pagina Principal")


def metodo_lineal(request):
    form = formcalculator()
    if request.method == 'POST':
        a = int(request.POST['a'])
        c = int(request.POST['c'])
        n = int(request.POST['n'])
        xo = int(request.POST['xo'])
        m = int(request.POST['m'])
        x = int(request.POST['x'])
        d = int(request.POST['d'])
        metodo = request.POST['metodo']
        if metodo == 'metodo_lineal':
            del datos[:]
            del mlineal[:]

            # resultado = a + c
            xoinicial = xo
            contador = 0
            matrizNueva = []
            matrizNueva = op_metodo_lineal(a, xo, xoinicial, c, m, n)

            if n >= 10 and n % 2 == 0:
                for x in matrizNueva:
                    contador = contador + 1
                    arr = np.array(matrizNueva).reshape(2, -1)
                    chi2, p, dof, expected = scipy.stats.chi2_contingency(arr)

            else:
                chi2 = 0
                arr = 0
                p = 0
                dof = 0
                messages.error(request, "El valor de N es impar, no se puede calcular chi2")

            for y in range(n):
                print (random.random())

        elif metodo == 'metodo_multiplicativo':
            del datosMulti[:]
            del mmulti[:]
            xoinicial = xo
            contador = 0
            matrizNueva = []
            matrizNueva = metodo_multiplicativo(a, xo, xoinicial, m, n)
            if n >= 10 and n % 2 == 0:
                for x in matrizNueva:
                    contador = contador + 1
                    arr = np.array(matrizNueva).reshape(2, -1)
                    chi2, p, dof, expected = scipy.stats.chi2_contingency(arr)

            else:
                chi2 = 0
                arr = 0
                p = 0
                dof = 0
                messages.error(request, "El valor de N es impar, no se puede calcular chi2")

            for y in range(n):
                print (random.random())
        elif metodo == 'metodo_cuadradomedio':
            del datosCuad[:]
            del mcum[:]
            contador = 0
            matrizNueva = []
            matrizNueva = cuadrado_medio(x, d, n)
            rand = random.randrange(n)
            chi2 = 0
            p = 0
            dof = 0
            for x in matrizNueva:
                contador = contador + 1
                #  plt.figure('Generador de Congruencial Multiplicativo')
                # plt.scatter(x, contador, c='#ffffff', s=x * 100, alpha=0.9)
                # plt.scatter(x, contador, c='#000000')
                # arr = np.array(matrizNueva).reshape(2, -1)
                # chi2, p, dof, expected = scipy.stats.chi2_contingency(arr)
            messages.error(request, "No se puede calcular Chi2")

            for y in range(n):
                print (random.random())

        return render(request, 'aleatorios/index.html',
                      {'chi2': chi2, 'p': p, 'a': a, 'c': c, 'n': n, 'x': x, 'm': m, 'xo': xo, 'd': d,
                       'dof': dof, 'mlineal': mlineal, 'mmulti': mmulti, 'mcum': mcum, 'datos': datos,
                       'datosMulti': datosMulti, 'datosCuad': datosCuad, 'matrizNueva': matrizNueva})

        # return HttpResponse(matrizNueva)
        # return render_to_response('metodo_lineal.html',{'matrizNueva':op_metodo_lineal})

    return render(request, 'aleatorios/index.html')
