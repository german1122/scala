#flask dependencies
from flask import Flask, redirect, url_for, render_template, request, session, json
#Vamos a importar las funciones financieras
from .credito import creditop
#pandas python
import pandas as pd
import numpy as np
import math
#Flask modularity
from sqlalchemy.orm import sessionmaker
from datetime import date
from datetime import timedelta
#from datetime import time
from dateutil.relativedelta import relativedelta
from datetime import date, datetime
import os
from flask import Blueprint
from Scala.__init__ import engine, db, legal_ap, legal_ap_a

legal_bp = Blueprint('legal', __name__, template_folder='templates')
Session = sessionmaker(bind = engine)
session = Session()

##########################################################################################################################################################
# A PARTIR DE AQUÍ CREAREMOS TODAS LAS RUTAS DE LOS CONTRATOS, ANEXOS Y PAGARÉS
##########################################################################################################################################################

@legal_bp.route("/Dashboard-Legal", methods = ["GET"])
#@login_required
def dashboard():
    return render_template("legal/index-legal.html")
@legal_bp.route("/credito_prendario", methods=["POST", "GET"])
def credito_prendario():
    if request.method == "GET":
        return render_template("legal/credito/cuestionario_cp.html")

    elif request.method == "POST":
        args = {
            'numero_contrato': str(request.form["numero_contrato"]),
            'acreditante': str(request.form["acreditante"]),
            'RFC_acreditante': str(request.form["RFC_acreditante"]),
            'domicilio_acreditante': str(request.form["domicilio_acreditante"]),
            'pagina_web': str(request.form["pagina_web"]),
            'apoderado_acreditante': str(request.form["apoderado_acreditante"]),
            'facultades': str(request.form["facultades"]),
            'poliza': str(request.form["poliza"]),
            'fecha_poliza': str(request.form["fecha_poliza"]),
            'fedatario': str(request.form["fedatario"]),
            'numero_notaria': str(request.form["numero_notaria"]),
            'entidad': str(request.form["entidad"]),
            'folio_mercantil': str(request.form["folio_mercantil"]),
            'lugar_inscripcion': str(request.form["lugar_inscripcion"]),
            'fecha_inscripcion': str(request.form["fecha_inscripcion"]),
            'denominacion': str(request.form["denominacion"]),
            'RFC_acreditada': str(request.form["RFC_acreditada"]),
            'nacionalidad': str(request.form["nacionalidad"]),
            'giro': str(request.form["giro"]),
            'telefonos': str(request.form["telefonos"]),
            'email': str(request.form["email"]),
            'domicilio_acreditada': str(request.form["domicilio_acreditada"]),
            'apoderado_acreditada': str(request.form["apoderado_acreditada"]),
            'instrumento_acreditada': str(request.form["instrumento_acreditada"]),
            'fecha_acreditada': str(request.form["fecha_acreditada"]),
            'fedatario_publico_acreditada': str(request.form["fedatario_publico_acreditada"]),
            'notaria_acreditada': str(request.form["notaria_acreditada"]),
            'entidad_acreditada': str(request.form["entidad_acreditada"]),
            'inscripcion_acreditada': str(request.form["inscripcion_acreditada"]),
            'lugar_inscripcion_acreditada': str(request.form["lugar_inscripcion_acreditada"]),
            'fecha_inscripcion_acreditada': str(request.form["fecha_inscripcion_acreditada"]),
            'actos_corporativos': str(request.form["actos_corporativos"]),
            'facultades_apoderado': str(request.form["facultades_apoderado"]),
            'poliza_apoderado': str(request.form["poliza_apoderado"]),
            'fecha_poliza_apoderado': str(request.form["fecha_poliza_apoderado"]),
            'cargo': str(request.form["cargo"]),
            'cargo_acreditada': str(request.form["cargo_acreditada"]),
            # Obligado Solidario
            'obligado_solidario': str(request.form["obligado_solidario"]),
            'RFC_obligado': str(request.form["RFC_obligado"]),
            'regimen_social': str(request.form["regimen_social"]),
            'nacionalidad_obligado': str(request.form['nacionalidad_obligado']),
            'ciudad_obligado': str(request.form['ciudad_obligado']),
            'curp': str(request.form['curp']),
            'ocupacion': str(request.form['ocupacion']),
            'telefono_obligado': str(request.form['telefono_obligado']),
            'email_obligado': str(request.form['email_obligado']),
            'domicilio_obligado': str(request.form['domicilio_obligado']),
            'estado_civil': str(request.form['estado_civil']),
            'ciudad_firma': str(request.form['ciudad_firma'])
        }

        hoy = date.today()
        now = datetime.now()
        dt_string = now.strftime("%d")
        dt_string2 = now.strftime("%m")
        dt_string3 = now.strftime("%Y")

        def meses(X):
            if X == '01':
                return 'enero'
            elif X == '02':
                return 'febrero'
            elif X == '03':
                return 'marzo'
            elif X == '04':
                return 'abril'
            elif X == '05':
                return 'mayo'
            elif X == '06':
                return 'junio'
            elif X == '07':
                return 'julio'
            elif X == '08':
                return 'agosto'
            elif X == '09':
                return 'septiembre'
            elif X == '10':
                return 'octubre'
            elif X == '11':
                return 'noviembre'
            elif X == '12':
                return 'diciembre'
        mesprint = meses(dt_string2)

        return render_template("legal/credito/credito_prendario.html", **args, hoy=hoy, dias=dt_string, mes=mesprint, año=dt_string3)


@legal_bp.route("/anexo_a_cp", methods=["POST", "GET"])
def anexo_a_cp():

    if request.method == "GET":
        return render_template("legal/credito/cuestionario_anexoa_cp.html")

    elif request.method == "POST":
        kwargs = {
            'dias': float(request.form["dias"]),
            'tasa_ordinaria': float(request.form["tasa_ordinaria_anual"]),
            'yrs': float(request.form["years"]),
            'principal': float(request.form["Principal"]),
            'tasa_comision': float(request.form["tasa_comision"]),
            'startdate': datetime.strptime(request.form["fechainicio"], "%Y-%m-%d").date(),
            'accesorios': float(request.form["acc"]),
            'nombre': str(request.form["nombre"]),
            'agregar': int(request.form["agregar"]),
            # Información del Anexo a partir de aquí
            'numero_contrato': str(request.form["numero_contrato"]),
            'numero_anexo': str(request.form["numero_anexo"]),
            'dia_firma': str(request.form["dia_firma"]),
            'mes_firma': str(request.form["mes_firma"]),
            'año_firma': str(request.form["año_firma"]),
            'acreditante': str(request.form["acreditante"]),
            'denominacion': str(request.form["denominacion"]),
            'bien1_folio': str(request.form["bien1_folio"]),
            'bien1_descripcion': str(request.form["bien1_descripcion"]),
            'bien1_accesorios': str(request.form["bien1_accesorios"]),
            'bien_observaciones': str(request.form["bien1_observaciones"]),
            'bien1_precio': str(request.form["bien1_precio"]),
            'bien1_cantidad': str(request.form["bien1_cantidad"]),
            'bien2_folio': str(request.form["bien2_folio"]),
            'bien2_descripcion': str(request.form["bien2_descripcion"]),
            'bien2_accesorios': str(request.form["bien2_accesorios"]),
            'bien2_observacion': str(request.form["bien2_observacio"]),
            'bien2_precio': str(request.form["bien2_precio"]),
            'bien2_cantidad': str(request.form["bien2_cantidad"]),
            'moneda': str(request.form["moneda"]),
            'banco': str(request.form["banco"]),
            'CLABE': str(request.form["CLABE"]),
            'cuenta': str(request.form["cuenta"]),
            'destino': str(request.form['destino']),
            'comision_reestructuracion': str(request.form['comision_reestructuracion']),
            'comision_pagoanticipado': str(request.form['comision_pagoanticipado']),
            'extrajudicial': str(request.form['extrajudicial']),
            'pena_convencional': str(request.form['pena_convencional']),
            'capital_letra': str(request.form['capital_letra']),
            'tir_letra': str(request.form['tir_letra']),
            'obligado_solidario': str(request.form["obligado_solidario"]),
            'domicilio_acreditante': str(request.form["domicilio_acreditante"]),
            'apoderado': str(request.form["apoderado"]),
            'apoderado_acreditada': str(request.form["apoderado_acreditada"]),
            'ciudad_firma': str(request.form['ciudad_firma']),
            'ciudad_anexo': str(request.form['ciudad_anexo'])


        }


        if   kwargs['agregar']==2:
            credito_funcion = credito_global(kwargs['dias'], kwargs['tasa_ordinaria'], kwargs['yrs'],
                                       kwargs['principal'], kwargs['tasa_comision'], kwargs['startdate'], kwargs['accesorios'], kwargs['nombre'])
        elif kwargs['agregar']==0:
            credito_funcion = creditop(kwargs['dias'], kwargs['tasa_ordinaria'], kwargs['yrs'],
                                       kwargs['principal'], kwargs['tasa_comision'], kwargs['startdate'], kwargs['accesorios'], kwargs['nombre'])
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
            'fecha_inicio': credito_funcion[14],
            'fecha_vencimiento': credito_funcion[15],
            'pago_parcial': credito_funcion[16],
            'periodo': credito_funcion[17],
            'diasprint': credito_funcion[18],
            'diaprint': credito_funcion[19],
            'plazo': credito_funcion[20],
            'column_namesA': credito_funcion[21],
            'row_dataA': credito_funcion[22],
            'capital_inicial': credito_funcion[23],
            'tir_anexo': credito_funcion[24]
        }

        #vencimiento_pagare = datetime.date(str(kwargs['yrs']), str(kwargs['mes']), str(kwargs['days']))  + (relativedelta(years=args['years']))

        Hoy = date.today()
        now = datetime.now()
        dt_string = now.strftime("%d")
        dt_string2 = now.strftime("%m")
        dt_string3 = now.strftime("%Y")

        def meses(X):
            if X == '01':
                return 'enero'
            elif X == '02':
                return 'febrero'
            elif X == '03':
                return 'marzo'
            elif X == '04':
                return 'abril'
            elif X == '05':
                return 'mayo'
            elif X == '06':
                return 'junio'
            elif X == '07':
                return 'julio'
            elif X == '08':
                return 'agosto'
            elif X == '09':
                return 'septiembre'
            elif X == '10':
                return 'octubre'
            elif X == '11':
                return 'noviembre'
            elif X == '12':
                return 'diciembre'
        mesprint = meses(dt_string2)

    elif request.method == 'POST':
        # if request.form['submit_button'] == 'Agregar a BDD':
        if kwargs['Agregar'] == 1:
            args['data_frame'].to_sql(
                'arrendamientos', con=engine, schema=None, if_exists='append')


    return render_template("legal/credito/anexo_a_cp.html", **kwargs, **args, zip=zip, Hoy=Hoy, Dias=dt_string, Mes=mesprint, Año=dt_string3)

@legal_bp.route("/credito_prendario_pf", methods=["POST", "GET"])
def credito_prendario_pf():

    if request.method == "GET":
        return render_template("legal/credito/cuestionario_cp_pf.html")

    elif request.method == "POST":
        args = {
            'numero_contrato': str(request.form["numero_contrato"]),
            'acreditante': str(request.form["acreditante"]),
            'RFC_acreditante': str(request.form["RFC_acreditante"]),
            'domicilio_acreditante': str(request.form["domicilio_acreditante"]),
            'pagina_web': str(request.form["pagina_web"]),
            'apoderado_acreditante': str(request.form["apoderado_acreditante"]),
            'facultades': str(request.form["facultades"]),
            'poliza': str(request.form["poliza"]),
            'fecha_poliza': str(request.form["fecha_poliza"]),
            'fedatario': str(request.form["fedatario"]),
            'numero_notaria': str(request.form["numero_notaria"]),
            'entidad': str(request.form["entidad"]),
            'folio_mercantil': str(request.form["folio_mercantil"]),
            'lugar_inscripcion': str(request.form["lugar_inscripcion"]),
            'fecha_inscripcion': str(request.form["fecha_inscripcion"]),
            # 'denominacion': str(request.form["denominacion"]),
            # 'RFC_acreditada': str(request.form["RFC_acreditada"]),
            # 'nacionalidad': str(request.form["nacionalidad"]),
            # 'giro': str(request.form["giro"]),
            # 'telefonos': str(request.form["telefonos"]),
            # 'email': str(request.form["email"]),
            # 'domicilio_acreditada': str(request.form["domicilio_acreditada"]),
            # 'apoderado_acreditada': str(request.form["apoderado_acreditada"]),
            # 'instrumento_acreditada': str(request.form["instrumento_acreditada"]),
            # 'fecha_acreditada': str(request.form["fecha_acreditada"]),
            # 'fedatario_publico_acreditada': str(request.form["fedatario_publico_acreditada"]),
            # 'notaria_acreditada': str(request.form["notaria_acreditada"]),
            # 'entidad_acreditada': str(request.form["entidad_acreditada"]),
            # 'inscripcion_acreditada': str(request.form["inscripcion_acreditada"]),
            # 'lugar_inscripcion_acreditada': str(request.form["lugar_inscripcion_acreditada"]),
            # 'fecha_inscripcion_acreditada': str(request.form["fecha_inscripcion_acreditada"]),
            # 'actos_corporativos': str(request.form["actos_corporativos"]),
            # 'facultades_apoderado': str(request.form["facultades_apoderado"]),
            # 'poliza_apoderado': str(request.form["poliza_apoderado"]),
            # 'fecha_poliza_apoderado': str(request.form["fecha_poliza_apoderado"]),
            'cargo': str(request.form["cargo"]),
            # 'cargo_acreditada': str(request.form["cargo_acreditada"]),
            # Obligado Solidario
            'obligado_solidario': str(request.form["obligado_solidario"]),
            'RFC_obligado': str(request.form["RFC_obligado"]),
            'regimen_social': str(request.form["regimen_social"]),
            'nacionalidad_obligado': str(request.form['nacionalidad_obligado']),
            'ciudad_obligado': str(request.form['ciudad_obligado']),
            'curp': str(request.form['curp']),
            'ocupacion': str(request.form['ocupacion']),
            'telefono_obligado': str(request.form['telefono_obligado']),
            'email_obligado': str(request.form['email_obligado']),
            'domicilio_obligado': str(request.form['domicilio_obligado']),
            'estado_civil': str(request.form['estado_civil']),
            'ciudad_firma': str(request.form['ciudad_firma']),
            'testigo': str(request.form['testigo'])
        }

        hoy = date.today()
        now = datetime.now()
        dt_string = now.strftime("%d")
        dt_string2 = now.strftime("%m")
        dt_string3 = now.strftime("%Y")

        def meses(X):
            if X == '01':
                return 'enero'
            elif X == '02':
                return 'febrero'
            elif X == '03':
                return 'marzo'
            elif X == '04':
                return 'abril'
            elif X == '05':
                return 'mayo'
            elif X == '06':
                return 'junio'
            elif X == '07':
                return 'julio'
            elif X == '08':
                return 'agosto'
            elif X == '09':
                return 'septiembre'
            elif X == '10':
                return 'octubre'
            elif X == '11':
                return 'noviembre'
            elif X == '12':
                return 'diciembre'
        mesprint = meses(dt_string2)

        return render_template("legal/credito/credito_prendario_pf.html", **args, hoy=hoy, dias=dt_string, mes=mesprint, año=dt_string3)


@legal_bp.route("/anexo_a_cp_pf", methods=["POST", "GET"])
def anexocp_persona_fisica():

    if request.method == "GET":
        return render_template("legal/credito/cuestionario_anexoa_cp_pf.html")

    elif request.method == "POST":
        kwargs = {
            'dias': float(request.form["dias"]),
            'tasa_ordinaria': float(request.form["tasa_ordinaria_anual"]),
            'yrs': float(request.form["years"]),
            'principal': float(request.form["Principal"]),
            'tasa_comision': float(request.form["tasa_comision"]),
            'startdate': datetime.strptime(request.form["fechainicio"], "%Y-%m-%d").date(),
            'accesorios': float(request.form["acc"]),
            'nombre': str(request.form["nombre"]),
            # Información del Anexo a partir de aquí
            'numero_contrato': str(request.form["numero_contrato"]),
            'numero_anexo': str(request.form["numero_anexo"]),
            'dia_firma': str(request.form["dia_firma"]),
            'mes_firma': str(request.form["mes_firma"]),
            'año_firma': str(request.form["año_firma"]),
            'acreditante': str(request.form["acreditante"]),
            'denominacion': str(request.form["denominacion"]),
            'bien1_folio': str(request.form["bien1_folio"]),
            'bien1_descripcion': str(request.form["bien1_descripcion"]),
            'bien1_accesorios': str(request.form["bien1_accesorios"]),
            'bien_observaciones': str(request.form["bien1_observaciones"]),
            'bien1_precio': str(request.form["bien1_precio"]),
            'bien1_cantidad': str(request.form["bien1_cantidad"]),
            'bien2_folio': str(request.form["bien2_folio"]),
            'bien2_descripcion': str(request.form["bien2_descripcion"]),
            'bien2_accesorios': str(request.form["bien2_accesorios"]),
            'bien2_observacion': str(request.form["bien2_observacio"]),
            'bien2_precio': str(request.form["bien2_precio"]),
            'bien2_cantidad': str(request.form["bien2_cantidad"]),
            'moneda': str(request.form["moneda"]),
            'banco': str(request.form["banco"]),
            'CLABE': str(request.form["CLABE"]),
            'cuenta': str(request.form["cuenta"]),
            'destino': str(request.form['destino']),
            'comision_reestructuracion': str(request.form['comision_reestructuracion']),
            'comision_pagoanticipado': str(request.form['comision_pagoanticipado']),
            'extrajudicial': str(request.form['extrajudicial']),
            'pena_convencional': str(request.form['pena_convencional']),
            'capital_letra': str(request.form['capital_letra']),
            'tir_letra': str(request.form['tir_letra']),
            'obligado_solidario': str(request.form["obligado_solidario"]),
            'domicilio_acreditante': str(request.form["domicilio_acreditante"]),
            'apoderado': str(request.form["apoderado"]),
            'apoderado_acreditada': str(request.form["apoderado_acreditada"]),
            'ciudad_firma': str(request.form['ciudad_firma']),
            'ciudad_anexo': str(request.form['ciudad_anexo']),



        }

        credito_funcion = creditop(kwargs['dias'], kwargs['tasa_ordinaria'], kwargs['yrs'],
                                       kwargs['principal'], kwargs['tasa_comision'], kwargs['startdate'], kwargs['accesorios'], kwargs['nombre'])

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
            'fecha_inicio': credito_funcion[14],
            'fecha_vencimiento': credito_funcion[15],
            'pago_parcial': credito_funcion[16],
            'periodo': credito_funcion[17],
            'diasprint': credito_funcion[18],
            'diaprint': credito_funcion[19],
            'plazo': credito_funcion[20],
            'column_namesA': credito_funcion[21],
            'row_dataA': credito_funcion[22],
            'capital_inicial': credito_funcion[23],
            'tir_anexo': credito_funcion[24]
        }

        #vencimiento_pagare = datetime.date(str(kwargs['yrs']), str(kwargs['mes']), str(kwargs['days']))  + (relativedelta(years=args['years']))

        Hoy = date.today()
        now = datetime.now()
        dt_string = now.strftime("%d")
        dt_string2 = now.strftime("%m")
        dt_string3 = now.strftime("%Y")

        def meses(X):
            if X == '01':
                return 'enero'
            elif X == '02':
                return 'febrero'
            elif X == '03':
                return 'marzo'
            elif X == '04':
                return 'abril'
            elif X == '05':
                return 'mayo'
            elif X == '06':
                return 'junio'
            elif X == '07':
                return 'julio'
            elif X == '08':
                return 'agosto'
            elif X == '09':
                return 'septiembre'
            elif X == '10':
                return 'octubre'
            elif X == '11':
                return 'noviembre'
            elif X == '12':
                return 'diciembre'
        mesprint = meses(dt_string2)

    # elif request.method == 'POST':
        # if request.form['submit_button'] == 'Agregar a BDD':
        # if kwargs['Agregar'] == 1:
        #    args['data_frame'].to_sql(
        #        'arrendamientos', con=engine, schema=None, if_exists='append')

    return render_template("legal/credito/anexocppf.html", **kwargs, **args, zip=zip, Hoy=Hoy, Dias=dt_string, Mes=mesprint, Año=dt_string3)
