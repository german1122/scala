from flask import Flask, redirect, url_for, render_template, request, session, json
#paquetería de tiempo
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from datetime import date, datetime
from flask import flash
from flask_sqlalchemy import SQLAlchemy
#Bases de datos
from Scala.__init__ import engine
#Pandas y numpy
import pandas as pd
import numpy as np
import math
import os
#Flask
from flask import Blueprint
from flask_wtf import Form
from wtforms import DateField
from datetime import date
from wtforms import validators, StringField, PasswordField
#Aquí importamos funciones propias
from .credito import creditop
from .restructura import reestructurar
#Definamos un blueprint para crear rutas

cotizador_bp = Blueprint('cotizador', __name__, template_folder='templates', static_folder='static', static_url_path='/Arrendamiento/static/assets')

@cotizador_bp.route("/Dashboard", methods = ["GET"])
#@login_required
def dashboard():
    return render_template("Reportes/dashboard.html")    

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