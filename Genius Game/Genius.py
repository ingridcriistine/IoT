import machine
from machine import Pin,PWM
import time
import random
import urequests
import ujson
import network

#Credenciais do WIFI
nome = "Wifi"
senha = "senha"

# Endereço do firebase
FIREBASE_URL = "url"
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


#Programação do jogo

LED_yellow = Pin(27, Pin.OUT)
LED_red = Pin(14, Pin.OUT)
LED_blue = Pin(12, Pin.OUT)
LED_green = Pin(13, Pin.OUT)

BUTTON_yellow = Pin(21, Pin.IN)
BUTTON_red = Pin(19, Pin.IN)
BUTTON_blue = Pin(18, Pin.IN)
BUTTON_green = Pin(5, Pin.IN)

buzzer = Pin(32, Pin.OUT)


def turnOn_LED(led):
    led.on()
    time.sleep(0.5)
    led.off()
    
    return led

def turnOn_buzzer():
    time.sleep(0.5)
    buzzer.on()
    time.sleep_ms(90)
    buzzer.off()

def LEDS():
    
    while BUTTON_yellow.value() == 0 and BUTTON_red.value() == 0 and BUTTON_blue.value() == 0 and BUTTON_green.value() == 0:
        a = 0
        
    if BUTTON_yellow.value() == 1:
        turnOn_buzzer()
        turnOn_LED(LED_yellow)
        led = LED_yellow
        return led
        
    if BUTTON_red.value() == 1:
        turnOn_buzzer()
        turnOn_LED(LED_red)
        led = LED_red
        return led
        
    if BUTTON_blue.value() == 1:
        turnOn_buzzer()
        turnOn_LED(LED_blue)
        led = LED_blue
        return led
        
    if BUTTON_green.value() == 1:
        turnOn_buzzer()
        turnOn_LED(LED_green)
        led = LED_green
        return led

def game_over():
    
    for i in range(3):
        
        LED_green.on()
        LED_red.on()
        LED_blue.on()
        LED_yellow.on()
        
        time.sleep(0.5)
        
        LED_green.off()
        LED_red.off()
        LED_blue.off()
        LED_yellow.off()
        
        time.sleep(0.2)
        

def random_LED():
    sort_num = random.choice([LED_yellow, LED_red, LED_blue, LED_green])
    
    return sort_num

def buzzer_LED(led):
    
    if(led == LED_yellow):
        tone(buzzer, 261);
        
    buzzer.on()
    time.sleep(1)
    buzzer.off()

#Genius

cont = 0
acabou = False
leds_sort = []

name = input("Digite o seu nome: ")

while True:
    cont = cont  + 1
    answers = []
    
    print(f"ROUND {cont}")
    
    led_sort = random_LED()
    leds_sort.append(led_sort)
        
    for j in range(cont):
        turnOn_buzzer()
        turnOn_LED(leds_sort[j])
        print(leds_sort[j])
        
        
    for j in range(cont):
        answer = LEDS()
        
        if leds_sort[j] !=  answer:
            acabou = True
            print("GAME OVER")
            game_over()
            break
        
        
        print(f"Resposta: {answer}")
    
    time.sleep(0.2)
                            
    if(acabou):
        print(f"PONTOS: {cont-1}")
        break


    informacao = {
        
        "Nome" :  name,
        "Pontos" : cont-1
        
    }
    
    enviarFire(informacao)








    
