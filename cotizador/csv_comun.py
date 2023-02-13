import pandas as pd
import numpy as np
import math
from datetime import date
from datetime import timedelta
#from datetime import time
from dateutil.relativedelta import relativedelta
from sympy import Symbol, nsolve

#from datetime import date
from scipy.optimize import fsolve
#from datetime import datetime, date
import datetime
import csv, json
from airium import Airium
import random, string

def csv_process(csvfilename,string_title, string_id, string_concepto, option_repeat, productos, servicios):
    b = Airium()
    #datos de toyota
    #string_title = str(title)
    #string_id = str(id)
    #string_concepto = str(concepto)
    csvfilepath = '/Users/germanvillar/Documents/Flask/Scala/cotizador/csv/' + str(csvfilename)
    df = pd.read_csv(csvfilepath)
    json_csv = df.to_json(orient="table")
    data = json.loads(json_csv)
    k=len(data["data"])
    g = list(range(1,101))    #'baterias' + str(i)] = int(request.form['bateria' +'-'+ str(i) + 'q'
    list_bat = ['regeneración', 'remanufactura', 'reparación',  ]
    #Base de productos:
    csvmateriales = '/Users/germanvillar/Documents/Flask/Scala/cotizador/csv/base_productos.csv'
    dfmateriales = pd.read_csv(csvmateriales)
    json_csvmateriales = dfmateriales.to_json(orient="table")
    datamateriales = json.loads(json_csvmateriales)
    k_m=len(datamateriales["data"])

    #Base de servicios:
    csvservicios = '/Users/germanvillar/Documents/Flask/Scala/cotizador/csv/base_servicios.csv'
    dfservicios = pd.read_csv(csvservicios)
    json_csvservicios = dfservicios.to_json(orient="table")
    dataservicios = json.loads(json_csvservicios)
    k_s=len(dataservicios["data"])

    with b.h4(_t=string_title):
        with b.p(_t='Favor de elegir una cantidad de '+ string_concepto + 's y un(a) ' + string_concepto + ':'):
            with b.div(klass="form-row").div( klass="form-group"):
                with b.div(klass="form-group"):
                    for h in zip(range(option_repeat)):
                        with b.span(klass="input-group-text"):
                            with b.select(name=string_concepto +'-'+ str(h[0]) + 'q', style="width: 80%", id=string_concepto):
                                for i in g:
                                    with b.option(id=str(i), name=string_concepto+ '-' + str(i) + 'q'):
                                        b(i)

                            #b('<input type = "number" class="js-example-basic-single", name =' + string_concepto +'-'+ str(h) + 'q' +', style="width: 80%", id=string_concepto>')
                        with b.select(name=string_concepto +'-'+ str(h[0]), style="width: 80%", id=string_concepto):
                             for i in range(k):
                                    with b.option(id=str(i), name=string_concepto+ '-' + str(i)):
                                        b(data["data"][i][string_id])
                        for n, y in zip(range(productos),range(servicios)):
                            with b.p(_t='Favor de seleccionar cantidad y material para el equipo # ' + str(h[0])):
                                b('<input type="text" class="form-control" placeholder="¿Cuantos materiales cotizarás?" aria-label="days" name = "productos_q-'+str(n)+'">')
                                with b.select(name='producto' +'-'+ str(n), style="width: 80%", id='producto' + str(n)):
                                    for i in range(k_m):
                                        with b.option(id=str(i), name=string_concepto+ '-' + str(i) + 'p'):
                                            b(datamateriales["data"][i]["descripcion"])

                            with b.p(_t='Favor de seleccionar cantidad y servicio para el equipo # ' + str(h[0])):
                                b('<input type="text" class="form-control" placeholder="¿Cuantos servicios cotizarás?" aria-label="days" name = "servicios_q-'+str(y)+'">')
                                with b.select(name='servicio' +'-'+ str(y), style="width: 80%", id='servicio' + str(y)):
                                     for i in range(k_s):
                                        with b.option(id=str(i), name=string_concepto+ '-' + str(i) + 's'):
                                            b(dataservicios["data"][i]["descripcion"])



                                         #with b.select()
                                        #for i in g:
                                            #    with b.option(id=str(i), name=string_concepto+ '-' + str(i) + 'q'):
                                            #b(i)`
            #with b.p(_t='Favor de elegir una cantidad para cada ' + string_concepto + ':'):
                #for h in range(option_repeat):
                    #with b.select(klass="js-example-basic-single", name=string_concepto +'-'+ str(h) + 'q', style="width: 80%", id=string_concepto):


    html2 = str(b)
    html3 = str(' ')
    if option_repeat>0:
        return html2
    if option_repeat==0:
        return html3


def cotizador_process(num_rows, concepto, concepts, csvfilename, quantities, var, productos, servicios):

    csvfilepath = '/Users/germanvillar/Documents/Flask/Scala/cotizador/csv/' + str(csvfilename)
    df = pd.read_csv(csvfilepath)
    json_csv = df.to_json(orient="table")
    data = json.loads(json_csv)
    k=len(data["data"])
    #t = [None]*(k)
    index = [None]*(num_rows)
    #for i in range(k):
    #    t[i]=data["data"][i]["modelo"]
    products = []

    def get_data(csv, variable, cantidad):
        path = '/Users/germanvillar/Documents/Flask/Scala/cotizador/csv/' + str(csv)
        dataf = pd.read_csv(csvfilepath)
        json_ = dataf.to_json(orient="table")
        datos = json.loads(json_)
        rango=len(datos["data"])
        conceptos = [None]*(rango)
        price = [None]*(cantidad)
        for i in range(rango):
            conceptos[i]=datos["data"][i][variable]
        return conceptos, datos, rango

    #conceptos_mat = get_data('base_servicios', var, productos)[0]
    #datos_mat = get_data('base_servicios')[1]
    #rango_mat = get_data('base_servicios')[2]
    #conceptos_ser = get_data('base_servicios')[0]
    #datos_ser = get_data('base_servicios')[1]
    #rango_ser = get_data('base_servicios')[2]
    conceptos_bat = get_data('base_baterias', var, num_rows)[0]
    datos_bat = get_data('base_baterias', var, num_rows)[1]
    rango_bat = get_data('base_baterias', var, num_rows)[2]


    def findprice(rango, conceptos_, filas, precio_, data_, col_name):
        t = [None]*(rango)
        indice = []*(filas)
        precio = str(precio_)
        for i in range(rango):
            t[i]=data_["data"][i][col_name]

        for l, g, h in zip(range(rango), range(filas), conceptos_.values()):
                    #for h in conceptos_.values():
            if h == t[l]:

                indice[g] = data_["data"][l][precio]
                #indice2[l] = l
                if indice[g] == None:
                #while indice[g]== None:
                    indice[g] = data_["data"][l][precio]
            elif h != t[l]:
                #try:
                for b in range(rango-l):
                    if h==t[b]:
                        indice[g] = data_["data"][b][precio]
                    elif h!=t[b]:
                        for e in range(rango-b):
                            if h==t[e]:
                                indice[g] = data_["data"][e][precio]
                    elif h!= t[e]:
                        for c in range(rango-e):
                            if h==t[c]:
                                indice[g] = data_["data"][c][precio]
        return indice
    #precio1 = findprice(k, concepts, num_rows, var, data, 'modelo')

    precio_bat = findprice(rango_bat, concepts, num_rows, var, datos_bat, 'modelo')
    #precio_m = findprice(rango_mat, conceptos_mat, num_rows,ultimo_costo , datos_mat)
    #precio_s = findeprice(rango_ser, conceptos_ser, num_rows, monto, datos_ser)





    #precio = data["data"][index[0]]["cliente_mxn"]
    #for m, q in zip(index, quantities.values()):
    #    subtotal = sum(q*m)



    for num1, num2 in zip(precio1, quantities.values()):
    	products.append(num1 * num2)

    c = Airium()
    with c.tfoot(contenteditable='True'):
        with c.tr().td(index2):
                c('Totales')
                with c.td().td().td():
                            c("${:,.2f}".format(sum(products)))
                            with c.td():
                                c("${:,.2f}".format(sum(products)*0.16))
                                with c.td():
                                    c("${:,.2f}".format(sum(products)*1.16))
                                    with c.thead():
                                        with c.th(scope="col", contenteditable='true'):
                                            #for m in index:
                                            for k, m, q in zip(concepts.values(), index, quantities.values()):
                                                with c.tr():
                                                    with c.td(contenteditable='True', id=k):
                                                        c(k)
                                                    with c.td(contenteditable='True', id=m):
                                                        c("${:,.2f}".format(round(m, 2)))
                                                    with c.td(contenteditable='True', id=m):
                                                        c(q)
                                                    with c.td(contenteditable='True', id=m):
                                                        c("${:,.2f}".format(round(q*m, 2)))
                                                    with c.td(contenteditable='True', id=m):
                                                        c("${:,.2f}".format(round(q*m*0.16, 2)))
                                                    with c.td(contenteditable='True', id=m):
                                                        c("${:,.2f}".format(round(q*m*1.16, 2)))





#[None, '$19,941.68', '$26,763.44', '$28,798.00', '$21,672.32']
#['$20,465.28', '$21,672.32','$28,798.00','$26,763.44' ,'$19,941.68' ]




    html2=str(c)
    html3=str('')
    if num_rows==0:
        return html3
    if num_rows>0:
        return html2
