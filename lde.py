from machine import Pin, PWM, I2C
import utime
import urandom

led = Pin(16, Pin.OUT)
btn = Pin(15, Pin.IN)

def my_handler(pin):
    print("IRQ with flags:", pin.irq().flags())

led.value(1)
utime.sleep(urandom.uniform(2, 5))
led.value(0)
btn.irq(trigger = Pin.IRQ_FALLING, handler = my_handler)
utime.sleep(1)
led.value(1)


si led == red:
    redbut.irc configurer avec handler sur une fonction qui fait continuer la partie
    blueBut.irc configurer avec handler sur gameover function