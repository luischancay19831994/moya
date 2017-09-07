# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import random

import numpy as np
import scipy.stats
import sys
from django.contrib import messages
from django.shortcuts import render
from aleatorios import views
import json
# Create your views here.
from aleatorios.views import  metodo_multiplicativo, op_metodo_lineal

num = []
datos = []
mx = []
mprob = []
mfreca = []
mfrecd = []
mfrecda = []
mdesde = []
mfrecd2 = []
matrizNueva =[]
mfreha2 = []
mresultado = []
mnume = []
def monte_carlo(request):
    if request.method == 'POST':

        metodo = request.POST['metodo']
        if metodo == 'montecarlo':

            # resultado = a + c
            contador = 0
            matrizNueva = []
            # matrizNueva = op_montecarlo(frecuencia)

            #seleccion de numeros para rango de campos a generar
        elif metodo == 'numeros':
            n = int(request.POST['n'])
            del num[:]
            nume = n
            num.append(nume)
            return render(request, 'montecarlo/index.html', {'nume': nume, 'num': range(n)})

        #selecciona el metodo montecarlo
        elif metodo == 'valor_x':
            #vacia las matrices para llenar de datos nuevos
            del mprob [:]
            del mfreca [:]
            del datos[:]
            del mfrecd[:]
            del mfrecd2[:]
            del mfreha2[:]
            del mresultado[:]
            del mx[:]
            # variables con request.POST para recibir datos de html
            no = int(request.POST['no'])
            nx = str(request.POST['nx'])
            nfre = str(request.POST['nfre'])

            #variables de valores para campos generados
            vx = request.POST.getlist('vx')  # will be ['heya1','heya2']
            vfre = request.POST.getlist('vfre')


            #variable para seleccion de metodo
            metodoa = request.POST['metodoa']

            #si se selecciona metodo lineal o metodo multiplicativo
            #  selecciona el metodo en la vista de la aplicacion de numeros aleatorios
            # reutilizando el codigo
            if metodoa == 'lineal':
                # variables de numeros aleatorios
                a = int(request.POST['a'])
                c = int(request.POST['c'])
                n = int(request.POST['n'])
                xo = int(request.POST['xo'])
                m = int(request.POST['m'])
                matrizNueva = []
                del matrizNueva[:]
                xoinicial = xo
                matrizNueva = op_metodo_lineal(a, xo, xoinicial, c, m, n)

            elif metodoa == 'multiplicativo':
                # variables de numeros aleatorios
                a = int(request.POST['a'])
                n = int(request.POST['n'])
                xo = int(request.POST['xo'])
                m = int(request.POST['m'])
                matrizNueva = []
                del matrizNueva[:]
                xoinicial = xo
                matrizNueva = metodo_multiplicativo(a, xo, xoinicial, m, n)
            elif metodoa == 'manual':
                matrizNueva = []
                del matrizNueva[:]

                nmanual = request.POST.getlist('nmanual')
                # re realiza recorrido para metodo desde y hasta
                for i in range(len(nmanual)):
                    # valores de frecuencia y valores de x
                    # se vx[i] siendo i inical 0 hasta el ultimo valor de frecuencia
                    nume = float(nmanual[i])
                    mnume.append(nume)
                    matrizNueva = mnume

            #inicializamos variables en 0 para operaciones matematicas
            sum = 0
            freca = 0
            frecd =0
            #matriz de suma para valores de frecuencia
            msum =[]
            #se realiza recorrido y se suman los valores de frecuencia
            #suma de frecuencia
            for i in range(len(vfre)):
                sum = sum + float(vfre[i])
                msum.append(sum)
            #re realiza recorrido para metodos
            for i in range (len(vfre)):
                #valores de frecuencia y valores de x
                # se vx[i] siendo i inical 0 hasta el ultimo valor de frecuencia
                fre = float(vfre[i])
                x = str(vx[i])

                #Metodo de probabilidad
                #se divide el valor de frecuencia sobre la suma
                prob = float(vfre[i]) / sum
                #se guarda en matriz mprob la probabilidad
                mprob.append(prob)
                #se guarda en matriz mx los valores de x
                mx.append(x)

                #Frecuencia acumulada
                #suma la frecuencia inicial con los siguientes valores
                freca = freca + float(mprob[i])
                #se guarda los valores sumados de frecuencia en la matriz mfreca
                mfreca.append(freca)

                #Le damos formato al float solo con 3 decimales
                #para frecuencia HASTA
                freh = float(mfreca[i])
                freha = round(freh,3)

                #Se guarda los valores formateados con 3 decimales
                #  en nueva matriz mfreha2
                mfreha2.append(freha)
                #se sua 0.001 para realizar matriz DESDE
                fred = float(freha)+0.001

                # si la matriz mfreca (Matriz Frecuencia Acumlada)
                # es igual a la posicion 0 se ingresa el valor de 0
                # y guardamos en nueva matriz DESDE mfrecd2

                if mfreca[i] == mfreca[0]:
                 mfrecd2.insert(int(fred), 0)
                #no funciona aun jaja
                #if mfreca[i] == mfreca[nm]:
                 #mfrecd2.remove(-1)

                #guardamos datos de frecuencia desde a nueva matriz
                #que en el codigo anterior le agregamos el 0
                mfrecd2.append(fred)

                # Hacemos una matriz con los datos de i frecuencia desde y Hasta
                mfrecd.append([i,fred,freha])
                #Hacemos matriz datos y guardamos todos los datos generados
                datos.append([i, x, fre, prob,freca,frecd,fred,freha])

            ### seleccion de  Frecuencia para resultados
            #hacemos 2 recorridos, uno para los eventos y otro para seleccionar el valor de x
            #recorrido de eventos
            for i in (range(no)):
                #recorrido para seleccionar valores de x
                for j in range(len(mfrecd)):
                    #hacemos un if que compare los datos con la matriz y las frecuencias DESDE y HASTA
                    #si se cumple la funcion se guardan los datos en la matriz mresultado
                 if matrizNueva[i] >= mfrecd2[j] and matrizNueva[i] <= mfreha2[j]:
                     #se guardan los datos en la matriz , de numeros aleatorios matrizNueva[i]
                     #  y de la matriz de frecuencia mfreca[j] y matriz de valores de x mx[j]
                    mresultado.append([i,matrizNueva[i],mfreca[j],mx[j]])

            #renderizamos todas las matrices para parsearlas en HTML
            return render(request, 'montecarlo/index.html', {'mnume':mnume,'mresultado':mresultado,'matrizNueva':matrizNueva,'mfrecd2':mfrecd2,'mdesde':mdesde,'mfrecd':mfrecd,'mfreca':mfreca,'sum':sum,'no':range(no),'datos': datos, 'nx': nx,'nfre':nfre})



        #si ocurre un error mostrara mensaje error
        else:
            messages.error(request, "error")
        #renderizamos pagina html
        return render(request, 'montecarlo/index.html')

        #renderizamos pagina index.html
    return render(request, 'montecarlo/index.html')
