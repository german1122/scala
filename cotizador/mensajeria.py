

import pandas as pd
import numpy as np
import math
from datetime import date
from datetime import timedelta
import csv
from dateutil.relativedelta import relativedelta
from datetime import date, datetime
#from datetime import time
from dateutil.relativedelta import relativedelta
from sympy import Symbol, nsolve
#from datetime import date
from scipy.optimize import fsolve
#from datetime import datetime, date
import datetime
from IPython.display import HTML
from collections import defaultdict
import os
from email.mime.text import MIMEText


def mensajes(archivo, text, nombre, html):
        # Define the recipient list
    #file = open(archivo,encoding='utf-8')
    #file = open (os.path.expanduser("~/Documents/python/Mensajeria_automatica/lista.csv"))
    csvreader = csv.reader(archivo)
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
        nombre_receptor = row[5]
        # Define the message content
        message = MIMEText(text)
        message['Subject'] = 'Olimer Kptl'
        message['From'] = nombre_emisor

        # Create a connection to the SMTP server
        parttext = MIMEText(text,"plain")
        parthtml = MIMEText(html,"html")

        message.attach(parttext)
        message.attach(parthtml)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(emisor, clave)
            server.sendmail(emisor, receptor, message.as_string())

        # Close the connection to the SMTP server
        server.quit()
