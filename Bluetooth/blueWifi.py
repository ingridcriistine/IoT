import ublue
import _thread
import time
from machine import Pin
import urequests
import ujson
import network

#Credenciais do WIFI
nomeW = ""
senha = ""

# Endereço do firebase
FIREBASE_URL = ""
SECRET_KEY = ""

def conectarWifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Conectando no WiFi...")
        wlan.connect(nomeW, senha)
        while not wlan.isconnected():
            pass
    print("Wifi conectado... IP: {}".format(wlan.ifconfig()[0]))

def enviarFire(data):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + SECRET_KEY
    }
    url = FIREBASE_URL + "/Ingrid.json"  # Coloque o seu nome

    response = urequests.put(url, data=ujson.dumps(data), headers=headers)
    print("Firebase Response:", response.text)
    response.close()


#Dê um nome para o seu bluetooth
nome = "Ingrid"

#Seta o pino do led padrão da esp32, podendo ser 2 ou 22
led = Pin(2, Pin.OUT)

#Função obrigatória para iniciar o funcionamento do bluetooth
def funcaoA():
    ublue.ublueON(nome)

#Função facultativa para utilizar as informações recebidas
def funcaoB():
    while True:
        try:
            print(ublue.info)
            if (int(ublue.info) == 0): #Lógica invertida pois nessa esp32 usa-se o pull_up
                led.value(1)
            elif (int(ublue.info) == 1):
                led.value(0)
            
        except ValueError:
            print("Entre com um valor inteiro")
            ublue.info = 0
            
        time.sleep(2)

#Inicia o processamento em 2 núcleos simultaneamente (multithreading)
_thread.start_new_thread(funcaoA,())
_thread.start_new_thread(funcaoB,())

conectarWifi()


if (led.value == 0):
    informacao = {
        "LED": "Ligado"
    }
    
elif (led.value == 1):
    informacao = {
        "LED": "Desligado"
    }
    
    
enviarFire(informacao)


