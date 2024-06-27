import dht
from machine import Pin
import time

# Configura o pino onde o DHT11 está conectado
dht_sensor = dht.DHT11(Pin(32))

# Configuração dos pinos
rs = Pin(13, Pin.OUT)
e = Pin(12, Pin.OUT)
d4 = Pin(14, Pin.OUT)
d5 = Pin(27 , Pin.OUT)
d6 = Pin(26, Pin.OUT)
d7 = Pin(25, Pin.OUT)

def pulse_enable():
    e.on()
    time.sleep_us(1)
    e.off()
    time.sleep_us(50)

def send_nibble(data):
    d4.value((data >> 0) & 1)
    d5.value((data >> 1) & 1)
    d6.value((data >> 2) & 1)
    d7.value((data >> 3) & 1)
    pulse_enable()

def send_byte(data, rs_value):
    rs.value(rs_value)
    send_nibble(data >> 4)  # Envia o nibble superior
    send_nibble(data & 0x0F)  # Envia o nibble inferior

def lcd_command(cmd):
    send_byte(cmd, 0)

def lcd_data(data):
    send_byte(data, 1)

def lcd_init():
    time.sleep(0.05)
    rs.off()
    e.off()
    send_nibble(0x03)
    time.sleep_ms(5)
    send_nibble(0x03)
    time.sleep_us(150)
    send_nibble(0x03)
    send_nibble(0x02)
    lcd_command(0x28)  # Função set: 4 bits, 2 linhas, 5x8 pontos
    lcd_command(0x0C)  # Display on, cursor off, blink off
    lcd_command(0x06)  # Entry mode set: incrementa e sem shift
    lcd_command(0x01)  # Limpa o display
    time.sleep_ms(2)

def lcd_puts(text):
    for char in text:
        lcd_data(ord(char))
        
def second_line():
    lcd_command(0x80 | 0X40)


# Função principal para ler o sensor DHT11
def read_dht11():
    while True:
        try:
            dht_sensor.measure()
            temp = dht_sensor.temperature()
            hum = dht_sensor.humidity()
            print("Temperatura: {}°C  Umidade: {}%".format(temp, hum))
            
            lcd_puts("  Temperatura: ")
            second_line()
            lcd_puts("      {} C ".format(temp))
            time.sleep(1)
            lcd_command(0x01)
            time.sleep(1)
            lcd_puts("    Umidade: ")
            second_line()
            lcd_puts("      {} % ".format(hum))
            time.sleep(1)
            lcd_command(0x01)
            time.sleep(1)
            
        except OSError as e:
            print("Falha na leitura do sensor:", e)
            lcd_puts("Falha na leitura do sensor:", e)
        
        # Aguarda dois segundos antes de ler novamente
        time.sleep(2)
    
        
# Inicializa o LCD
lcd_init()

# Chama a função principal
read_dht11()