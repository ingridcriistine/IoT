# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 15:19:12 2024

@author: liq1ct
"""

import requests
import pyodbc
import time
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd

def sinal():
    proxies = {'https': ''}
    url_temperatura = ''
    url_umidade = 'https://'
    temperatura = float(requests.get(url_temperatura, proxies=proxies).content)
    umidade = float(requests.get(url_umidade, proxies=proxies).content)
    return temperatura, umidade

def InserirBD(sinal):
    server = ''
    database = ''
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';Trusted_Connection=yes')
    cursor = cnxn.cursor()
    cursor.execute(f"INSERT Sensor (Temperatura, Umidade) VALUES ({sinal[0]},{sinal[1]})")
    cursor.commit()
    print("Inserido com sucesso!")

def apresentar(sinal):
    print(f"Temperatura: {sinal[0]}")
    print(f"Umidade: {sinal[1]}")


server = '' #Exemplo
database = ''
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';Trusted_Connection=yes')
cursor = cnxn.cursor()

cursor.execute("SELECT Temperatura, timestamp FROM Sensor")
row = cursor.fetchone()
lista=[]
listatempo=[]

while row:
    lista.append(row[0])
    listatempo.append(str(row[1]))
    row = cursor.fetchone()

def graficoLinha():
    df=pd.DataFrame({"Temperatura":lista, "Tempo":listatempo})
    df['Tempo'] = pd.to_datetime(df["Tempo"])
    sns.relplot(x="Tempo", y="Temperatura", data=df, kind="line")
    plt.title("Temperatura por Tempo")
    plt.xticks(rotation=90)
    print('gráfico')

while True:
    valores = (sinal[0],sinal[1])
    apresentar(valores)
    InserirBD(valores)
    time.sleep(120)
    graficoLinha()
    
