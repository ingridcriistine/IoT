# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 11:23 2024

@author: Ingrid
"""

import pyodbc
import time
import json
import requests

def InserirBD(sinal):
    server = 'server'
    database = 'Ingrid'
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';Trusted_Connection=yes')
    cursor = cnxn.cursor()
    cursor.execute(f"INSERT Record_list (Nome, Pontuação) values ('{sinal[0]}', {sinal[1]})")
    cursor.commit()
    print("Inserido com sucesso!")

def apresentar(sinal):
    print(f"Nome: {sinal[0]}")
    print(f"Pontuação: {sinal[1]}")

proxies = {'https': ""}

while True :
    
    url = ''
    info = json.loads(requests.get(url,proxies=proxies).content)

    nome = json.loads(requests.get(url,proxies=proxies).content)['Nome']
    pontuacao = json.loads(requests.get(url,proxies=proxies).content)['Pontos']

    valores = (nome, pontuacao)
    valorAnterior = valores

    #print(valores)
    apresentar(valores)
    InserirBD(valores)

