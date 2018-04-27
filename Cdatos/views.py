from django.shortcuts import render
from datetime import datetime, date, time
import requests
import json

# Create your views here.
def gis(request):
	baseSensor = "sensor"
	patronmedida = "unidades"
	url = 'http://ec2-54-202-254-90.us-west-2.compute.amazonaws.com:8080/backendAmbiente/webresources/generic/getAllEstaciones'
	r = requests.get(url)
	url_1 = 'http://ec2-54-202-254-90.us-west-2.compute.amazonaws.com:8080/backendAmbiente/webresources/generic/getAllSensores'
	r_1 = requests.get(url_1)
	# consultando mediciones
	url_2 = 'http://ec2-54-202-254-90.us-west-2.compute.amazonaws.com:8080/backendAmbiente/webresources/generic/getAllMedicionesByEstacion'
	# consultando mediciones
	if r.status_code==200 and r_1.status_code==200:
	    estaciones = r.json()
	    estaciones_s = json.dumps(estaciones)
	    estaciones_d = json.loads(estaciones_s)

	    sensores = r_1.json()
	    sensores_s = json.dumps(sensores)
	    sensores_d = json.loads(sensores_s)

        for i in range(len(estaciones_d)):
            a = estaciones_d[i]
            valorA = a['idEstacion']
            strv = str(valorA)
            #
            med = requests.post(url_2,data=strv)
            medi = med.json()
            med_s = json.dumps(medi)
            med_d = json.loads(med_s)
            #mediciones = '%s' % (capturas)
            
            #diccionarios de medidas
            for clave,valor in med_d.items():
                estaciones_d[i][str(clave)] = dict()
                l = list()
                for v in valor:
                        diccionarioInterno = dict()
                        lista = v.split(";")
                        fecha = lista[0].split("/")
                        anio = int(fecha[0])
                        mes = int(fecha[1])
                        dia = int(fecha[2])
                        fecha_py = date(anio,mes,dia)
                        tiempo = lista[1].split(":")
                        h = int(tiempo[0]) 
                        m = int(tiempo[1])
                        s = int(tiempo[2])
                        tiempo_py = time(h,m,s)
                        f_captura = datetime.combine(fecha_py,tiempo_py)
                        d_capturado = float(lista[2])
                        diccionarioInterno['fecha'] = f_captura
                        diccionarioInterno['medida'] = d_capturado
                        diccionarioInterno['unidadesM'] = str(lista[3])
                        l.append(diccionarioInterno)
                L_orden = sorted(l, reverse=True)
                for k,s in L_orden[0].items():
                    v1 = "%s_%s" % (clave, k)
                    estaciones_d[i][v1] = s
                #estaciones_d[i][str(clave)] = L_orden

	    # for i in range(len(estaciones_d)):
	    #     a = estaciones_d[i]
	    #     valorA = a['idEstacion']
	    #     k = 0
	    #     for j in range(len(sensores_d)):
	    #         b = sensores_d[j]
	    #         valorB = b['idEstacion']
	    #         if valorA == valorB:
	    #             k += 1
	    #             nSensor = '%s%d' % (baseSensor,k)
	    #             unidades = '%s%d' % (patronmedida,k)
	    #             estaciones_d[i][nSensor] = sensores_d[j]['nombre']
	    #             estaciones_d[i][unidades] = sensores_d[j]['unidades']

		context = {
		"valores": estaciones_d,
		}
	

	return render(request, "home.html", context)