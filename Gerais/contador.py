import machine
from machine import Pin
import time

# Configuração dos pinos do LCD
rs = Pin(13, Pin.OUT)
e = Pin(12, Pin.OUT)
d4 = Pin(14, Pin.OUT)
d5 = Pin(27 , Pin.OUT)
d6 = Pin(26, Pin.OUT)
d7 = Pin(25, Pin.OUT)
button = machine.Pin(2, machine.Pin.IN)
cont = 1

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

# Inicializa o LCD
lcd_init()


# Escreve no display
lcd_puts("    Contador")

# while True:
#     if  button.value() == 1:
#         time.sleep(0.1)
#         lcd_command(0x01)
#         time.sleep(0.1)
#         lcd_puts(f"Contagem: {cont}")
#         cont = cont+1
#         button_state = button.value()
#         print("estado_do_botao", button_state)
#         time.sleep(0.1)
#     

