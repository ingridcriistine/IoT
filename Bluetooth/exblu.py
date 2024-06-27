import ublue
import _thread
import time
from machine import Pin

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
        time.sleep(0.02)

#Inicia o processamento em 2 núcleos simultaneamente (multithreading)
_thread.start_new_thread(funcaoA,())
_thread.start_new_thread(funcaoB,())