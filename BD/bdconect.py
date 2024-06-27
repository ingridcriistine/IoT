# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 08:41:22 2024

@author: Ingrid
"""

import pyodbc
import time
import numpy as np
#import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import json
import requests
import datetime

def InserirBD(sinal):
    server = ''
    database = 'Ingrid'
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';Trusted_Connection=yes')
    cursor = cnxn.cursor()
    cursor.execute(f"INSERT Sensor (Temperatura, Umidade) VALUES ({sinal[0]},{sinal[1]})")
    cursor.commit()
    print("Inserido com sucesso!")

def apresentar(sinal):
    print(f"Temperatura: {sinal[0]}")
    print(f"Umidade: {sinal[1]}")


proxies = {'https': ""}

while True:
    url = 'https://'
    info = json.loads(requests.get(url,proxies=proxies).content)

    temperatura = json.loads(requests.get(url,proxies=proxies).content)['Temperatura']
    umidade = json.loads(requests.get(url,proxies=proxies).content)['Umidade']

    valores = (temperatura,umidade)
    #print(valores)
    apresentar(valores)
    InserirBD(valores)
    time.sleep(120)