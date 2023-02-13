'''A continuación definimos una función que toma como argumentos:

una lista con fechas, un datetime.date y dos data frames:

su resultado es entregar la concatenación de las tablas a partir del elemento
datetime.date, tomando en cuenta que ambos data frames contienen las mismas columnas '''

import pandas as pd
import numpy as np
import math
from datetime import date
from datetime import timedelta

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


def reestructurar(d, time, df, df2):
    def condition(x): return datetime.datetime.strptime(x[0], "%Y-%m-%d").date() == d
    #def condition(x): return x < d
    output = [idx for idx, element in enumerate(time) if condition(element)]
    r = output[0]
    dfhead = df.head(r)
    df3 = pd.concat([dfhead, df2.iloc[1: , :]])
    return(df3)

def merge_dict(d1, d2):
    dd = defaultdict(list)

    for d in (d1, d2):
        for key, value in d.items():
            if isinstance(value, list):
                dd[key].extend(value)
            else:
                dd[key].append(value)
    return dict(dd)
#dct1 = jsondict
#dct2 =json.loads(jsondatos)
#combined_dct = merge_dict(dct1, dct2)
#json_str3 = json.dumps(combined_dct)
