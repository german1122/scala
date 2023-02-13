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


def cotizador_process(num_rows, concepto, concepts, csvfilename, quantities, var, productos, servicios, q_p, q_s):

    csvfilepath = '/Users/germanvillar/Documents/Flask/Scala/cotizador/csv/' + str(csvfilename)
    df = pd.read_csv(csvfilepath)
    json_csv = df.to_json(orient="table")
    data = json.loads(json_csv)
    k=len(data["data"])
    products = []

    bat = [None]*(num_rows)
    mat = [None]*(len(q_p))
    ser = [None]*(len(q_s))
    for i in range(num_rows):
        bat[i] = concepts['baterias' +str(i)]
    for i in range(len(q_p)):
        mat[i] = productos['productos' +str(i)]
    for i in range(len(q_s)):
        ser[i] = servicios['servicios' +str(i)]

    def get_data(csv, variable, cantidad, col_name, conceptos):
        path = '/Users/germanvillar/Documents/Flask/Scala/cotizador/csv/' + str(csv)
        dataf = pd.read_csv(path)
        json_ = dataf.to_json(orient="table")
        datos = json.loads(json_)
        rango=len(datos["data"])
        largo=len(conceptos)
        t = [None]*(rango)
        indice = [None]*(cantidad)
        for i in range(rango):
            t[i]=datos["data"][i][col_name]
        for l, g, h in zip(range(largo), range(cantidad), conceptos):
            if h == t[l]:
                indice[g] = datos["data"][l][variable]
                if indice[g] == None:
                    indice[g] = datos["data"][l][variable]
            elif h != t[l]:
                for b in range(rango-l):
                    if h==t[b]:
                        indice[g] = datos["data"][b][variable]
                    elif h!=t[b]:
                        for e in range(rango-b):
                            if h==t[e]:
                                indice[g] = datos["data"][e][variable]
                    elif h!= t[e]:
                        for c in range(rango-e):
                            if h==t[c]:
                                indice[g] = datos["data"][c][variable]
        return indice
    precios_bat = get_data('base_baterias.csv', var, num_rows, 'modelo', bat)
    #precios_mat = get_data('base_productos.csv', 'ultimo_costo', int(list(q_p.values())[0]), 'descripcion', mat)
    #precios_mat = get_data('base_productos.csv', 'ultimo_costo', len(q_p), 'descripcion', mat)
    precios_ser = get_data('base_servicios.csv', 'monto', len(q_s), 'descripcion', ser)


    for num1, num2 in zip(precios_bat, quantities.values()):
    	products.append(num1 * num2)
    def producto_punto(x, y):
        for num1, num2 in zip(x, y):
            products=[]
            products.append(num1 * num2)
            return products
    gran_total= sum(producto_punto(precios_ser, list(q_s.values()))) + sum(producto_punto(precios_bat, quantities.values()))

    c = Airium()
    with c.tfoot(contenteditable='True'):
        with c.tr().td(quantities):
                c('Totales')
                with c.td().td().td():
                            c("${:,.2f}".format(gran_total))

                            with c.td():
                                c("${:,.2f}".format(gran_total*0.16))
                                #c(len(q_p))
                                #c(precios_ser[0])
                                #c(list(q_s.values())[0])
                                with c.td():
                                    c("${:,.2f}".format(gran_total*1.16))

                                    with c.thead():
                                        with c.th(scope="col", contenteditable='true'):
                                            #for m in index:
                                            for k, m, q in zip(concepts.values(), precios_bat, quantities.values()):
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
                                            for k, m, q in zip(ser, precios_ser, q_s.values()):
                                                with c.tr():
                                                    with c.td(contenteditable='True', id=k):
                                                        c(k)
                                                    with c.td(contenteditable='True', id=m):
                                                        c("${:,.2f}".format(round(int(m), 2)))

                                                    with c.td(contenteditable='True', id=m):
                                                        c(q)
                                                    with c.td(contenteditable='True', id=m):
                                                        c("${:,.2f}".format(round(int(q)*int(m), 2)))

                                                    with c.td(contenteditable='True', id=m):
                                                        c("${:,.2f}".format(round(int(q)*int(m)*0.16, 2)))

                                                    with c.td(contenteditable='True', id=m):
                                                        c("${:,.2f}".format(round(int(q)*int(m)*1.16, 2)))











    html2=str(c)
    html3=str('')
    if num_rows==0:
        return html3
    if num_rows>0:
        return html2
