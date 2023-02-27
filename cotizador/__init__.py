from flask import Flask, redirect, url_for, render_template, request, session, json
from airium import Airium
from bs4 import BeautifulSoup as bs4
import csv, smtplib, ssl
#paquetería de tiempo
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import random
from datetime import date, datetime
from flask import flash
from flask_sqlalchemy import SQLAlchemy
from collections import Counter
#Bases de datos
from Scala.__init__ import engine
#Pandas y numpy
import pandas as pd
import numpy as np
import math
import os
import io
from email.mime.text import MIMEText
#Flask
from flask import Blueprint, jsonify
from flask_wtf import Form
from wtforms import DateField
from datetime import date
from wtforms import validators, StringField, PasswordField
#Aquí importamos funciones propias
from .mensajeria import mensajes
from .credito import creditop
from .restructura import reestructurar
from .csv_comun2 import csv_process, cotizador_process
import csv, json
from flask_cors import CORS, cross_origin
from email.mime.multipart import MIMEMultipart
import ssl
from email.mime.text import MIMEText
import pywhatkit

#from .mensajes import send_mails
#from jsonmerge import merge, mergeStrategy


#Definamos un blueprint para crear rutas

cotizador_bp = Blueprint('cotizador', __name__, template_folder='templates', static_folder='static', static_url_path='/Arrendamiento/static/assets')

@cotizador_bp.route("/Dashboard", methods = ["GET"])
#@login_required
def dashboard():
    return render_template("Reportes/dashboard.html")

@cotizador_bp.route("/mensajeria", methods=["GET", "POST"])
def mensajeria():
    if request.method == "GET":
        template_dir = os.path.join(os.getcwd(), 'cotizador/templates/cotizador/mensajeria')

        # Get a list of all files in the templates directory
        template_files = [f for f in os.listdir(template_dir) if f.endswith('.html')]

        return render_template("cotizador/mensajeria/cuestionario-email.html", templates=template_files)
    elif request.method == "POST":

        file = request.files["excel"]
        file_content = file.read().decode("utf-8")
        csvreader = csv.reader(io.StringIO(file_content))

        text = str(request.form["parrafo"])
        nombre = str(request.form["nombre"])
        asunto = str(request.form["asunto"])
        selected_template = str(request.form["selected_template"])
        #con_copia = str(request.form["concopia"])
        #textoglobal = str(render_template("cotizador/mensajeria/email-inlined2.html", text = text, nombre = nombre))

        header = next(csvreader)
        header = next(csvreader)

        rows = []
        for row in csvreader:
            rows.append(row)

            receptor = row[0]
            emisor = row[1]
            clave = row[2]
            cc = row[3]
            nombre_emisor = row[4]
            saludo = row[5]
            nombre_receptor = row[6]
            nombre_vendedor = row[7]
            #textoglobal = str(render_template("cotizador/mensajeria/email-inlined2.html",
            textoglobal = str(render_template("cotizador/mensajeria/"+str(selected_template),
            text = text, nombre_receptor = nombre_receptor, nombre_emisor=nombre_emisor, saludo=saludo,nombre_vendedor=nombre_vendedor ))
            # Define the message content
            message = MIMEMultipart("alternative")
            message['Subject'] = asunto
            message['From'] = nombre_emisor
            message['cc'] = cc
            message['to'] = receptor

            # Create a connection to the SMTP server
            part_text = MIMEText(text, "plain")
            part_html = MIMEText(textoglobal, "html")

            message.attach(part_text)
            message.attach(part_html)
            #server.starttls()
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(emisor, clave)
                server.sendmail(emisor, receptor, message.as_string())

            # Close the connection to the SMTP server
                server.quit()

        #return render_template("cotizador/mensajeria/email-inlined2.html", text = text, nombre = nombre)
        return render_template("cotizador/mensajeria/" + str(selected_template),
        text = text, nombre_receptor = nombre_receptor, nombre_emisor=nombre_emisor, saludo=saludo, nombre_vendedor=nombre_vendedor)

@cotizador_bp.route("/mensajeria-whats", methods=["GET", "POST"])
def whatsapp():
    if request.method == "GET":
        template_dir = os.path.join(os.getcwd(), 'cotizador/templates/cotizador/mensajeria')

        # Get a list of all files in the templates directory
        template_files = [f for f in os.listdir(template_dir) if f.endswith('.html')]

        return render_template("cotizador/mensajeria/cuestionario-whats.html", templates=template_files)
    elif request.method == "POST":

        file = request.files["excel"]
        file_content = file.read().decode("utf-8")
        csvreader = csv.reader(io.StringIO(file_content))

        text = str(request.form["parrafo"])
        header = next(csvreader)
        header = next(csvreader)
        rows = []

        for row in csvreader:
            rows.append(row)
            telefono = row[0]
            nombre_receptor = row[1]
            saludo=row[2]
            text_complete = saludo + " " + nombre_receptor + " " + text
            now = datetime.now()
            hour = now.hour
            minute = now.minute + 1
            segundo = now.second
            new_minute = int(minute)
            new_minute = new_minute
            print (hour,new_minute, nombre_receptor)
            telf = "+52"+telefono
            if segundo >= 40:
                new_minute = new_minute + 1
            if new_minute == 60:
                new_minute = 1
                hour = hour + 1
            pywhatkit.sendwhatmsg(telf,text_complete,hour,new_minute,15,True,5)

        return render_template("cotizador/mensajeria/respuesta-w.html" )

@cotizador_bp.route("/cuestionario", methods=["POST", "GET"])
def cotizador():
    if request.method == "GET":
        return render_template("/cotizador/credito/cuestionario.html")
    elif request.method == "POST":
        kwargs = {
            'dias': float(request.form["dias"]),
            'tasa_ordinaria': float(request.form["tasa_ordinaria_anual"]),
            'yrs': float(request.form["years"]),
            'principal': float(request.form["Principal"]),
            'tasa_comision': float(request.form["tasa_comision"]),
            'startdate': datetime.strptime(request.form["fechainicio"], "%Y-%m-%d").date(),
            'accesorios': float(request.form["acc"]),
            'Agregar': int(request.form["agregar"]),
            'nombre': str(request.form["nombre"]),

        }

        credito_funcion = creditop(kwargs['dias'], kwargs['tasa_ordinaria'], kwargs['yrs'],
                                   kwargs['principal'], kwargs['tasa_comision'], kwargs['startdate'],
                                    kwargs['accesorios'], kwargs['nombre'])

        args = {
            'hoy': credito_funcion[0],
            'capital': credito_funcion[1],
            'years': credito_funcion[2],
            'pago': credito_funcion[3],
            'desembolso': credito_funcion[4],
            'intereses': credito_funcion[5],
            'tir': credito_funcion[6],
            'tiriva': credito_funcion[7],
            'cat': credito_funcion[8],
            'costo': credito_funcion[9],
            'row_data': credito_funcion[10],
            'column_names': credito_funcion[11],
            'acc': credito_funcion[12],
            'comision': credito_funcion[13],
            'int_total': credito_funcion[25],
            'df': credito_funcion[26],
            'time': credito_funcion[28]
        }
        if kwargs['Agregar'] == 1:
            args['df'].to_sql(
                'creditos', con=engine, schema=None, if_exists='append')

        elif kwargs['Agregar']==2:
            args['df2'] = pd.read_sql("select * from creditos where id = ?", engine, params={kwargs['nombre']})
            #para más información ir a la función "reestructurar" en reestructura.py:
            time = pd.DataFrame(args['df2']['fecha'])
            time = time.values.tolist()
            startdate2 = args['time'][1]
            df3 = pd.DataFrame(args['df2'])
            df = pd.DataFrame(args['df'])
            df4 = reestructurar(startdate2, time, df3, df)
            args['columns'] = df3.columns.values
            args['rows'] = list(df3.round(2).values.tolist())
            args['columns2'] = df4.columns.values
            args['rows2'] = list(df4.round(2).values.tolist())
        elif kwargs['Agregar']==3:
            args['df2'] = pd.read_sql("select * from creditos where id = ?", engine, params={kwargs['nombre']})
            #para más información ir a la función "reestructurar" en reestructura.py:
            time = pd.DataFrame(args['df2']['fecha'])
            time = time.values.tolist()
            startdate2 = args['time'][1]
            df3 = pd.DataFrame(args['df2'])
            df = pd.DataFrame(args['df'])
            df4 = reestructurar(startdate2, time, df3, df)

            args['columns'] = df3.columns.values
            args['rows'] = list(df3.round(2).values.tolist())
            args['columns2'] = df4.columns.values
            args['rows2'] = list(df4.round(2).values.tolist())
            id = kwargs['nombre']
            connection = engine.raw_connection()
            cur = connection.cursor()
            cur.execute("DELETE FROM creditos where id = ?",(id,))
            connection.commit()
            df5 = df4[['N', 'Capital', 'interés', 'IVA', 'amortización', 'accesorios', 'pago', 'liquidación', 'ID', 'fecha']]
            df5.to_sql('creditos', con=engine, schema=None, if_exists='append')


        return render_template("cotizador/credito/cotizador.html", **kwargs, **args, zip=zip)

'''A partir de aquí realizamos pruebas get de bases de datos estáticas mediante CSV'''

@cotizador_bp.route("/forklift", methods=["GET", "POST"])
@cross_origin()
def forklift():
    content = request.get_json(silent=True)
    csvfilepath = '/Users/germanvillar/Documents/Flask/Scala/cotizador/csv/prueba.csv'
    data = {}
    inputm = []

    df = pd.read_csv(csvfilepath)
    jsondatos = df.to_json(orient="table")
    jsondatos1 = df.to_json(orient="index")
    # creating a list of column names by
    # calling the .columns
    list_of_column_names = list(df.columns)

    #json.loads(jsondatos)
    k = json.loads(jsondatos)
    l = k["data"]
    h = json.loads(jsondatos1)

    #with open(r'/Users/germanvillar/Documents/Flask/Scala/cotizador/csv/fabian.json') as f:
    #    datosfabian= json.load(f)
    #l = str(len(datosfabian))

    jsondict = {
        "count": len(k["data"]),
        "next": [],
        "previous": [],
        "":k["data"]
        }
    jsondict2 = {
    "data": k["data"]
    }

    jsondict3 = [{"index": 0, "ubicacion": "TRANZVM", "tipo": "HOMBRE PARADO SENTADO", "marca": "TOYOTA", "modelo": "6FBRE16", "serie": "36412", "anum": "2013", "precio_cliente": "$250,000.00", "modelo_bateria": "24-125-11", "v": "48V", "ah": "625", "capacidad": "1600", "altura_max": "8.5 METROS", "reparacion_faltante": "LISTO PARA VENTA", "precio_dist": " $ 195,000.00 ", "margen": "22%"}, {"index": 1, "ubicacion": "TRANZVM", "tipo": "HOMBRE PARADO SENTADO", "marca": "TOYOTA", "modelo": "6FBRE16", "serie": "36413", "anum": "2013", "precio_cliente": "$250,000.00", "modelo_bateria": "24-125-11", "v": "48V", "ah": "625", "capacidad": "1600", "altura_max": "8.5 METROS", "reparacion_faltante": "LISTO PARA VENTA", "precio_dist": " $ 195,000.00 ", "margen": "22%"}]
    #return mergede_dict, 200
    #return jsonify(jsondict), 200
    #return json.dumps(jsondict2["data"]), 200
    return json.dumps(jsondict3), 200

@cotizador_bp.route("/forklift2", methods=["GET", "POST"])
@cross_origin()
def forklift2():
    if request.method == "GET":
        return render_template("/cotizador/tranzvm/qform.html")
    elif request.method == "POST":
        kwargs = {
        'baterias': int(request.form["baterias"]),
        'productos_bat': int(request.form["productos_bat"]),
        'servicios_bat': int(request.form["servicios_bat"]),
        'cargador': int(request.form["cargadores"]),
        'montacargas': int(request.form["montacargas"]),
        #'montacargas2': int(request.form["montacargas2"]),
        #'producto': int(request.form["productos"]),
        #'proveedor': int(request.form["proveedores"]),
        'regeneracion': int(request.form["regeneraciones"]),
        #'regeneracion2': int(request.form["regeneraciones2"]),
        }
        session['baterias'] = kwargs['baterias']
        session['cargadores'] = kwargs['cargador']
        session['montacargas'] = kwargs['montacargas']
        #session['productos'] = kwargs['producto']
        #session['proveedores'] = kwargs['proveedor']
        session['regeneraciones'] = kwargs['regeneracion']
        session['productos_bat'] = kwargs['productos_bat']
        session['servicios_bat'] = kwargs['servicios_bat']
        #session['regeneraciones2'] = kwargs['regeneracion2']
        a = Airium()


        baterias_rem=csv_process('base_baterias.csv','Base de baterías', 'modelo', 'bateria', kwargs['baterias'], kwargs['productos_bat'], kwargs['servicios_bat'])
        cargadores=csv_process('base_cargadores.csv','Base de cargadores', 'modelo', 'cargador'  ,kwargs['cargador'], kwargs['productos_bat'], kwargs['servicios_bat'])
        montas=csv_process('base_montacargas.csv','Base de montacargas', 'modelo', 'montacargas' ,kwargs['montacargas'], kwargs['productos_bat'], kwargs['servicios_bat'])
        #montas2=csv_process('base_montacargas2.csv','Base de montacargas2', 'modelo', 'montacargas' ,kwargs['montacargas2'])
        #productos=csv_process('base_productos.csv','Base de productos', 'descripcion', 'producto',kwargs['producto'], kwargs['productos_bat'], kwargs['servicios_bat'])
        #proveedores=csv_process('base_proveedores.csv','Base de proveedores', 'nombre', 'proveedor',kwargs['proveedor'])
        regeneraciones=csv_process('base_regeneraciones.csv','Base de regeneraciones', 'concepto', 'regeneración',kwargs['regeneracion'], kwargs['productos_bat'], kwargs['servicios_bat'])
        #regeneraciones2=csv_process('base_toyota.csv','Base de Toyota', 'concepto', 'regeneración2',kwargs['regeneracion2'])

        #html = kwargs['baterias']*baterias_rem + kwargs['cargadores']*cargadores + kwargs['montacargas']*montas + kwargs['montacargas2']*montas2 + kwargs['productos']*productos + kwargs['proveedores']*proveedores + kwargs['regeneraciones']*regeneraciones + kwargs['regeneraciones2']*regeneraciones2
        html = baterias_rem + cargadores + montas   + regeneraciones
        #args = {
        #'baterias_names': [idx for idx, element in enumerate(kwargs['baterias']) if condition(element)]
        #}

        #html = str(a) + 200*csv_process('base_productos.csv','Base de productos', 'descripcion', 'materiales')  # casting to string extracts the value


            #return render_template("/cotizador/tranzvm/cuestionario.html", html = html)
            #return render_template("/cotizador/tranzvm/cuestionario.html", html = html)

        # or directly to UTF-8 encoded bytes:

        #html_bytes = bytes(a)  # casting to bytes is a shortcut to str(a).encode('utf-8')
        #return json.dumps(data["data"][10]["modelo"]), 200
        #return html, 200
        return render_template("/cotizador/tranzvm/cuestionario.html", html=html, kwargs = kwargs)


    #return kwargs, 200



@cotizador_bp.route("/forklift-form", methods=["GET", "POST"])
@cross_origin()
def forklift_form():
    if request.method == "GET":
        return render_template("/cotizador/tranzvm/cuestionario.html")
    elif request.method == "POST":
        args={
        'baterias' : session.get('baterias', None),
        'servicios_bat' : int(session.get('servicios_bat', None)),
        'productos_bat' : int(session.get('productos_bat', None)),
        'cargadores' : session.get('cargadores', None),
        'montacargas': session.get('montacargas', None),
        'productos': session.get('productos', None),
        'proveedores': session.get('proveedores', None),
        'regeneraciones': session.get('regeneraciones', None),
        #'regeneraciones2': session.get('regeneraciones2', None)
        }
        string='0123456789ABCDEF'

        concepts = dict()
        quantities = dict()
        prod = dict()
        serv = dict()
        q_prod = dict()
        q_serv = dict()
        for i in range(args['baterias']):
            concepts['baterias' + str(i)] = request.form['bateria' +'-'+ str(i)]
            quantities['baterias' + str(i)] = int(request.form['bateria' +'-'+ str(i) + 'q'])
        for i in range(args['productos_bat']):
            prod['productos' + str(i)] = request.form['producto-' + str(i)]
            q_prod['productosq' + str(i)] = int(request.form['productos_q-'+str(i)])
        for i in range(args['servicios_bat']):
            serv['servicios' + str(i)] = request.form['servicio-' + str(i)]
            q_serv['serviciosq' + str(i)] = int(request.form['servicios_q-'+str(i)])
        var = 'cliente_mxn'
        #baterias = cotizador_process(num_rows, concepto, concepts, csvfilename):
        baterias = cotizador_process(args['baterias'], 'baterias', concepts,
         'base_baterias.csv', quantities, var, prod, serv, q_prod, q_serv)
        html = baterias
        folio = ''.join(random.choice('0123456789') for i in range(4))
        folio2 = ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(3))
        foliot = folio + folio2
        return render_template("/cotizador/tranzvm/cotizador.html", html = html, folio=foliot, hoy = date.today())


@cotizador_bp.route("/pruebas", methods=["GET", "POST"])
@cross_origin()
def pruebas():
    csvfilepath = '/Users/germanvillar/Documents/Flask/Scala/cotizador/csv/base_baterias.csv'
    df = pd.read_csv(csvfilepath)
    json_csv = df.to_json(orient="table")
    data = json.loads(json_csv)
    k=len(data["data"])
    t = [None]*(k)
    index = [None]*2
    for i in range(k):
        t[i]=data["data"][i]["modelo"]
        if '18-100-19' == t[i]:
            index[0] = i
            if any(elem is None for elem in index)=='false':
                index[1] = any(elem is None for elem in index)

    precio = data["data"][index[0]]["cliente_mxn"]

    #index[g] = data["data"][l]["cliente_mxn"]


    #return json.dumps(data["data"][40]["cliente_mxn"])
    #return str(k)
    #return json.dumps(data["data"]), 200
    #return json.dumps(precio)
    return str(index)
