from machine import Pin
import time

sensor = Pin(33, Pin.IN)
buzzer = Pin(25, Pin.OUT)

def read_sensor():
    while True:
        if sensor.value() == 1:
            print("Movimento detectado!")
            buzzer.on()
            time.sleep(0.1)
            buzzer.off()
            buzzer.on()
            time.sleep(0.1)
            buzzer.off()
            
        else:
            print("Nenhum movimento")
            buzzer.on()
            time.sleep(2)
            
        time.sleep(1)
        
read_sensor()