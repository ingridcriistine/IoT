import dht
from machine import Pin
import time
import urequests
import ujson
import network


# Configura o pino onde o DHT11 está conectado
dht_sensor = dht.DHT11(Pin(32))
led = Pin(14, Pin.OUT)
#button_Led = Pin(21, Pin.IN)

led_Tv = Pin(26, Pin.OUT)
#button_Tv = Pin(21, Pin.IN)
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
            
            getData()
            
            if led.value():
                light_value = True
            else:
                light_value = False
                
            if led_Tv.value():
                tv_value = True
            else:
                tv_value = False
            
            informacao = {
                "Temperatura" : temp,
                "Umidade" : hum,
                "Led" : light_value,
                "Tv" : tv_value
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
    

def getData():
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + SECRET_KEY
    }
    url = FIREBASE_URL + "/Ingrid.json"  # Coloque o seu nome

    response = urequests.get(url, headers=headers)
    dictionary = ujson.loads(response.text)
    print("Light:", dictionary["Led"])
    print("Televison:", dictionary["Tv"])
    response.close()
    
    if dictionary["Led"] :
        led.on()
        light_value = True
        
    else:
        led.off()
        light_value = False
        
    if dictionary["Tv"] :
        led_Tv.on()
        tv_value = True
    else:
        led_Tv.off()
        tv_value = False
    
conectarWifi()
while True:
    time.sleep(1)
    read_dht11()
    

