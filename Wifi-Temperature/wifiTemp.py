import dht
from machine import Pin
import time
import urequests
import ujson
import network


# Configura o pino onde o DHT11 está conectado
dht_sensor = dht.DHT11(Pin(32))
temp = 0
hum = 0

# Função principal para ler o sensor DHT11
def read_dht11():
    while True:
        try:
            dht_sensor.measure()
            temp = dht_sensor.temperature()
            hum = dht_sensor.humidity()
            print("Temperatura: {}°C  Umidade: {}%".format(temp, hum))
            
            informacao = {
                "Temperatura" : temp,
                "Umidade" : hum
            }
            
            time.sleep(1)
            enviarFire(informacao)
            
            
        except OSError as e:
            print("Falha na leitura do sensor:", e)
        
        # Aguarda dois segundos antes de ler novamente
        time.sleep(2)  


#Credenciais do WIFI
nome = ""
senha = ""

# Endereço do firebase
FIREBASE_URL = ""
SECRET_KEY = ""

def conectarWifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Conectando no WiFi...")
        wlan.connect(nome, senha)
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



conectarWifi()
while True:
    time.sleep(1)
    read_dht11()
    
