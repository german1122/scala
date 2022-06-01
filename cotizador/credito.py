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
from IPython.display import HTML

def creditop(dias, tasa_ordinaria_anual, years, P, tasa_comision, startdate,acc,nombre, **kwargs):
    if dias == 30:
        n = int(round(12*years, 0))
    elif dias == 7:
        n = int(round(51*years, 0))
    elif dias == 14:
        n= int(round(24*years,0))
    else:
        n = int(round(years*360/dias, 0))
    #startdate = datetime.date(annum, mes, dia)
    interes = tasa_ordinaria_anual * (dias/360)
    interes_sin_iva = interes/1.16
    iva = 0.16
    hoy = date.today()
    pago = P*(1+tasa_comision)*interes/(1-(1+interes)**(-n))
    pagop = [None] * (n+1)
    interest = [None] * (n+1)
    Capitalt = [None] * (n+1)
    Amortiz  = [None] * (n+1)
    Liquid   = [None] * (n+1)
    time     = [None] * (n+1)
    N =[None]*(n+1)
    N[0] = 0
    ivat =[None] * (n+1)
    accesorio = acc*(1+tasa_comision)*interes/(1-(1+interes)**(-n/years))
    accesorios = [None] * (n+1)
    interest[0] = 0
    Amortiz[0] = 0
    Capitalt[0] = (P+acc)*(1+tasa_comision)
    Liquid[0] = (P+acc)*(1+tasa_comision)
    accesorios[0] = 0
    if startdate != hoy:
        time[0] = startdate
    else:
        time[0] = hoy
    ivat[0] = 0
    pagop[0] = 0
    comision = tasa_comision*P
    Rentas_en_garantia = pago*(n*0.06)
    total_primer_pago = comision + Rentas_en_garantia + pago
    Flujo = np.array([None] * (n+1))
    Flujo_con_iva = np.array([None] * (n+1))
    #Eliminé las comisiones de los
    #flujos porque son un costo real del negocio que origina el cliente
    Flujo[0] = -P - comision
    Flujo_con_iva[0] = -P
    periodos = np.arange(1,n+2)
    def npv(irr, cfs, yrs):
        return np.sum(cfs / (1 + irr)**(yrs))
    from scipy.optimize import fsolve
    def irr(cfs, yrs, x0, **kwargs):
        return np.ndarray.item(fsolve(npv, x0=x0, args=(cfs, yrs), **kwargs))
    t_weeks = relativedelta(weeks=+1)
    t_months = relativedelta(months=+1)
    t_fifteen = relativedelta(day = 15)
    t_day = relativedelta(days = dias)
    t_monthday = relativedelta(months =+1, day = dias*2)
    Nombre = [None]*(n+1)
    dia = startdate.day
    for i in range (1,n+1):
        pagop[i] = pago+accesorio
        interest[i] = Capitalt[i-1]*interes_sin_iva
        ivat[i] = interest[i]*iva
        Amortiz[i] = pago - interest[i]-ivat[i] + accesorio
        if i in range(int(n/years),n-int(n/years)+1,int(n/years)):
            Capitalt[i] = Capitalt[i-1] - Amortiz[i] + acc*(1+tasa_comision)
        else:
            Capitalt[i] = Capitalt[i-1] - Amortiz[i]
        #Agregar "+ Capitalt[i]*0.1" para cobrar 10% del comisión al liquidar anticipadamente
        Liquid[i] = Capitalt[i-1]+interest[i] + ivat[i]
        Flujo[i] = pago-ivat[i]
        Flujo_con_iva[i] = pago
        accesorios[i] = accesorio
        if dias == 30:
            time[i] = time[i-1] + t_months + relativedelta(day = dia)
        elif dias == 7:
                time[i] = time[i-1] + t_weeks
        #Vamos a forzar que si dias ≤ dia, entonces salte al día más cercano de la quincena:
        elif dias == 15 and dias<=dia:
            if i == 1:
                time[i] = time[i-1] + relativedelta(day = 30)
            elif (i % 2) == 0:
                time[i] = time[i-1] + relativedelta(day = 15) + t_months
            else:
                time[i] = time[i-1] + relativedelta(day = 30)
        #Ahora lo mismo, pero en el caso dias > dia:
        elif dias == 15 and dias>dia:
            if i == 1:
                time[i] = time [i-1] + relativedelta(day = 15)
            elif (i % 2) == 0:
                time[i] = time [i-1] + relativedelta(day = 30)
            else:
                time[i] = time[i-1] + relativedelta(day = 15) + t_months

         #Vamos a forzar que si dias ≤ dia, entonces salte al día más cercano de la catorcena
        elif dias == 14 and dias<=dia:
            if i == 1:
                time[i] = time[i-1] + relativedelta(day = 28)
            elif (i % 2) == 0:
                time[i] = time[i-1] + relativedelta(day = 14) + t_months
            else:
                time[i] = time[i-1] + relativedelta(day = 28)
        #Ahora lo mismo, pero en el caso dias > dia:
        elif dias == 14 and dias>dia:
            if i == 1:
                time[i] = time [i-1] + relativedelta(day = 14)
            elif (i % 2) == 0:
                time[i] = time [i-1] + relativedelta(day = 28)
            else:
                time[i] = time[i-1] + relativedelta(day = 14) + t_months
        else:
            time[i] = time[i-1] + relativedelta(days = dias)
        N[i] = N[i-1] + 1
        Nombre = str(nombre)


    rentabilidad = round(((sum(interest) + sum(Amortiz) + comision)/(P + years*acc)-1)*(1/years), 3)

    df = pd.DataFrame(columns=["N", "Capital", "interés","IVA", "amortización","accesorios","pago", "liquidación", "ID", "fecha"])
    df['Capital'] = Capitalt
    df['interés'] = interest
    df['IVA'] = ivat
    df['amortización'] = Amortiz
    df['pago'] = pagop
    df['liquidación'] = Liquid
    df['fecha'] = time
    df['accesorios'] = accesorios
    df['N'] = N
    df['ID'] = Nombre

    df1 = pd.DataFrame(columns=["Capital", "interés","IVA", "amortización","accesorios","pago", "liquidación"])
    df1['Capital'] = Capitalt
    df1['interés'] = interest
    df1['IVA'] = ivat
    df1['amortización'] = Amortiz
    df1['pago'] = pagop
    df1['liquidación'] = Liquid
    #df1['fecha'] = time
    df1['accesorios'] = accesorios
    #df1['N'] = N


    #Tabla de Amortización de los Anexos "A":
    df1A = pd.DataFrame(columns=["Saldo Inicial", "Pago Interés Ordinario","IVA Intereses Ordinarios", "Pago Capital","Accesorios","Pago Parcial"])
    df1A['Saldo Final'] = Capitalt
    df1A['Pago Interés Ordinario'] = interest
    df1A['IVA Intereses Ordinarios'] = ivat
    df1A['Pago Capital'] = Amortiz
    df1A['Pago Parcial'] = pagop
    df1A['Saldo Inicial'] = Liquid
    #df1['fecha'] = time
    df1A['Accesorios'] = accesorios
    #df1['N'] = N


    df1 = df1.applymap("${0:,.2f}".format)
    dfN=pd.DataFrame(columns=["N"])
    dfN['N'] = N
    df2 =pd.DataFrame(columns=["Fecha"])
    df2['Fecha'] = time
    dfX=pd.concat([df1.reset_index(drop=True),df2.reset_index(drop=True)], axis=1)
    df3=pd.concat([dfN.reset_index(drop=True),dfX.reset_index(drop=True)], axis=1)
    #Creación de Data Frames sobre Periodos y Fechas de Pago Anexo
    df1A = df1A.applymap("${0:,.2f}".format)
    dfA=pd.DataFrame(columns=["Periodo"])
    dfA['Periodo'] = N
    df2A =pd.DataFrame(columns=["Fecha de Pago"])
    df2A['Fecha de Pago'] = time
    dfXA=pd.concat([df1A.reset_index(drop=True),df2A.reset_index(drop=True)], axis=1)
    df3A=pd.concat([dfA.reset_index(drop=True),dfXA.reset_index(drop=True)], axis=1)

    capital_print = "${:,.2f}".format(P)
    pago_print = "${:,.2f}".format(pago)
    desembolso_print = "${:,.2f}".format(sum(pagop))
    intereses_print = "${:,.2f}".format(round((sum(pagop) - comision-P - sum(ivat))/years), 3)
    tir_print = "{:.2f}%".format(round(100*irr(cfs=Flujo, yrs=periodos, x0=0.01)*(360/dias)), 3)
    cat_print = "{:.2f}%".format((1+irr(cfs=Flujo, yrs=periodos, x0=0.01))**(360/dias)-1)
    #cat_print = 0
    tiriva_print = "{:.2f}%".format(round(100*irr(cfs=Flujo_con_iva, yrs=periodos, x0=0.01)*(360/dias)), 3)
    costo_capital_print = "{:.2f}%".format(round(rentabilidad*100), 2)
    fecha = hoy
    acc_print = "${:,.2f}".format(round(accesorio, 2))
    comision_print = "{:.2f}%".format(tasa_comision*100)
    #tabla_html = df1.round(2).to_html(classes = 'data')

    titulos = df3.columns.values
    row_data = list(df3.round(1).values.tolist())
    #Creación de variables para columnas y filas de tabla de Anexo "A"
    titulosA = df3A.columns.values
    row_dataA = list(df3A.round(1).values.tolist())

    fecha_inicio = str(startdate)
    fecha_vencimiento = str(time[n])
    pago_parcial = "${:,.2f}".format(pagop[1])

    def periodo(Y):
        if Y == 30:
            return 'mensual'
        elif Y == 15:
            return 'quincenal'
        elif Y == 14:
            return 'catorcenal'
        elif Y == 7:
            return 'semanal'
        elif Y == 1:
            return 'diaria'

    per = periodo(dias)
    diasprint = str(dias)
    diaprint =str(dia)
    plazo = str(N[n])
    capital_inicial = "${:,.2f}".format(Capitalt[0])
    tasa_ordinaria_anualA="{:.2f}%".format(100*tasa_ordinaria_anual/1.16)
    interes_total = "${:,.2f}".format(sum(interest))
    tasa_global = (1/years)*sum(interest)/sum(Amortiz)


    #text_file = open("table.html", "w")
    #text_file.write(tabla_html)
    #text_file.close()
    #(normal)print("México, CDMX, a",hoy), print("A quien corresponda, extendemos la siguiente cotización de crédito simple por parte de Financiera Debitaria."), print("El primer pago incluye seis por ciento de rentas en garantía, comisión y la primera renta:"), print("{:,}".format(round(total_primer_pago, 2))), print("El pago mensual de este crédito es de:"), print("{:,}".format(round(pago, 2))), print("El desembolso total de este proyecto es de:"), print("{:,}".format(round(sum(pagop) + comision), 2)), print("Así, se pagarían en intereses el siguiente monto anual:"), print("{:,}".format(round((sum(pagop) + comision-P - sum(ivat))/years), 2)), print("La TIR anual del proyecto equivale a"), print('{:2f}%'.format(100*irr(cfs=Flujo, yrs=periodos, x0=0.01)*(360/dias))), print("La TIR anual, incluyendo IVA, del proyecto equivale a"), print('{:2f}%'.format(100*irr(cfs=Flujo_con_iva, yrs=periodos, x0=0.01)*(360/dias))), print("El CAT del proyecto, según Banxico, equivale a"), print('{:2f}%'.format(10*(1+irr(cfs=Flujo, yrs=periodos, x0=0.01))**(360/dias)-1)), print("El costo de capital anual del proyecto es de:"), print(rentabilidad), print("La tabla de pagos de este proyecto es la siguiente:"), print(df1.round(2))
    #(Eduardo)print("México, CDMX, a",hoy), print("A quien corresponda, extendemos la siguiente cotización de crédito simple por parte de Financiera Debitaria por un monto de", "{:,}".format(P), "."),print("El plazo de este proyecto es de ", years, "años."), print("El pago mensual de este crédito es de:"), print("{:,}".format(round(pago, 2))), print("El desembolso total de este proyecto es de:"), print("{:,}".format(round(sum(pagop) + comision), 2)), print("Así, se pagarían en intereses el siguiente monto anual:"), print("{:,}".format(round((sum(pagop) + comision-P - sum(ivat))/years), 2)), print("La TIR anual del proyecto equivale a"), print('{:2f}%'.format(100*irr(cfs=Flujo, yrs=periodos, x0=0.01)*(360/dias))), print("La TIR anual, incluyendo IVA, del proyecto equivale a"), print('{:2f}%'.format(100*irr(cfs=Flujo_con_iva, yrs=periodos, x0=0.01)*(360/dias))), print("El CAT anual del proyecto, según Banxico, equivale a"), print('{:2f}%'.format(10*(1+irr(cfs=Flujo, yrs=periodos, x0=0.01))**(360/dias)-1)), print("El costo de capital anual del proyecto es de:"), print('{:2f}%'.format(rentabilidad*100)), print("La tabla de pagos de este proyecto es la siguiente:"), print(df1.round(2))
    #(con IVA)print("México, CDMX, a",hoy), print("A quien corresponda, extendemos la siguiente cotización de crédito simple por parte de Financiera Debitaria por un monto de", "{:,}".format(P), "."),print("El plazo de este proyecto es de ", years, "años."), print("El pago mensual de este crédito es de:"), print("{:,}".format(round(pago, 2))), print("El desembolso total de este proyecto es de:"), print("{:,}".format(round(sum(pagop) + comision), 2)), print("Así, se pagarían en intereses el siguiente monto anual:"), print("{:,}".format(round((sum(pagop) + comision-P - sum(ivat))/years), 2)), print("La TIR anual del proyecto equivale a"), print('{:2f}%'.format(100*irr(cfs=Flujo, yrs=periodos, x0=0.01)*(360/dias))), print("La TIR anual, incluyendo IVA, del proyecto equivale a"), print('{:2f}%'.format(100*irr(cfs=Flujo_con_iva, yrs=periodos, x0=0.01)*(360/dias))), print("El CAT anual del proyecto, según Banxico, equivale a"), print('{:2%}'.format((1+irr(cfs=Flujo, yrs=periodos, x0=0.01))**(360/dias)-1)), print("El costo de capital anual bruto del proyecto es de:"), print('{:2f}%'.format(rentabilidad*100)), print("La tabla de pagos de este proyecto es la siguiente:"), print(df1.round(2))
    #print("México, CDMX, a",hoy), print("A quien corresponda, extendemos la siguiente cotización de crédito simple por parte de Financiera Debitaria por un monto de", "{:,}".format(P), "."),print("El plazo de este proyecto es de ", years, "años."), print("El pago mensual de este crédito es de:"), print("{:,}".format(round(pago, 2))), print("El desembolso total de este proyecto es de:"), print("{:,}".format(round(sum(pagop) + comision), 2)), print("Así, se pagarían en intereses el siguiente monto anual:"), print("{:,}".format(round((sum(pagop) + comision-P - sum(ivat))/years), 2)), print("La TIR anual del proyecto equivale a"), print('{:2f}%'.format(100*irr(cfs=Flujo, yrs=periodos, x0=0.01)*(360/dias))), print("El CAT anual del proyecto, según Banxico, equivale a"), print('{:2%}'.format((1+irr(cfs=Flujo, yrs=periodos, x0=0.01))**(360/dias)-1)), print("El costo de capital anual bruto del proyecto es de:"), print('{:3f}%'.format(rentabilidad*100)), print("La tabla de pagos de este proyecto es la siguiente:"), print(df1.round(2))
    #print("México, CDMX, a",hoy), print("A quien corresponda, extendemos la siguiente cotización de crédito simple por parte de Lourdes Barajas por un monto de", capital_print, "."),print("El plazo de este proyecto es de ", years, "años."), print("El pago mensual de este crédito es de:"), print(pago_print), print("El desembolso total de este proyecto es de:"), print(desembolso_print), print("Así, se pagarían en intereses el siguiente monto anual:"), print(intereses_print), print("La TIR anual del proyecto equivale a"), print(tir_print), print("El CAT anual del proyecto, según Banxico, equivale a"), print(cat_print), print("El costo de capital anual bruto del proyecto es de:"), print(costo_capital_print), print("La tabla de pagos de este proyecto es la siguiente:"), print(df1.round(2))
    #print("México, CDMX, a",hoy), print("A quien corresponda, extendemos la siguiente cotización de crédito simple por parte de Financiera Debitaria por un monto de", pago_print, "."),print("El plazo de este proyecto es de ", years, "años."), print("El pago mensual de este crédito es de:"), print(pago_print, print("El desembolso total de este proyecto es de:"), print(desembolso_print), print("Así, se pagarían en intereses el siguiente monto anual:"), print(intereses_print), print("La TIR anual del proyecto equivale a"), print(tir_print), print("El CAT anual del proyecto, según Banxico, equivale a"), print(cat_print), print("El costo de capital anual bruto del proyecto es de:"), print(costo_capital_print), print("La tabla de pagos de este proyecto es la siguiente:"), print(df1.round(2))
#creditop(dias, tasa_ordinaria_anual, years, P, tasa_comision, annum, mes, dia)
    return (fecha, capital_print, years, pago_print, desembolso_print, #0-4
        intereses_print, tir_print, cat_print,#5-7
        tiriva_print, costo_capital_print, row_data, #8-10
            titulos, acc_print, comision_print, fecha_inicio, #11-14
            fecha_vencimiento, pago_parcial, per, diasprint, diaprint, plazo, #15-20
             titulosA, row_dataA, capital_inicial, tasa_ordinaria_anualA, #21-24
             interes_total, df, tasa_global, time) #25-28
