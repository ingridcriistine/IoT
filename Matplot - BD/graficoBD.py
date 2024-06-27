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
cont = 0
t = []
u = []
n = []

server = 'CA-C-0064V\SQLEXPRESS'
database = 'Ingrid'
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database + ';Trusted_Connection=yes')
cursor = cnxn.cursor()

#Função para ler a tabela
def ler(tipo):
    cursor.execute(f"SELECT {tipo} FROM Sensor")
    return cursor.fetchall()

# Criação do gráfico conectado com a tabela geral
# plt.scatter(ler('timestamp'), ler('Umidade'), color='red', label='Umidade')
# plt.scatter(ler('timestamp'), ler('Temperatura'), color='hotpink', label='Temperatura')
# plt.xlabel("Horário")
# plt.ylabel("Temperatura e umidade")
# plt.legend()
# plt.grid()
# plt.show()

#Criação do gráfico com dados em tempo real
while cont < 10:
    url = 'https://'
    info = json.loads(requests.get(url,proxies=proxies).content)

    temperatura = json.loads(requests.get(url,proxies=proxies).content)['Temperatura']
    umidade = json.loads(requests.get(url,proxies=proxies).content)['Umidade']
    #hora = json.loads(requests.get(url,proxies=proxies).content)['timestamp']
    now = datetime.datetime.now().strftime("%H:%M:%S")

    valores = (temperatura,umidade)
    print(valores)
    apresentar(valores)
    InserirBD(valores)

    cont = cont +1
    t.append(temperatura)    
    u.append(umidade)
    n.append(now)

plt.plot(t, linewidth=1, marker='o', markersize=5, color='red', label='Temperatura') 
plt.plot(u, linewidth=1, marker='o', markersize=5, color='purple', label='Umidade') 
plt.title("Banco de Dados")
plt.xlabel('Medição')
plt.ylabel('Valor')
plt.legend()
plt.xticks(rotation = 45)
plt.grid(axis='y', linestyle='dashed', zorder=1)

print("\nConcluido")

plt.show()
plt.close()
