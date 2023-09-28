import machine
import utime
import random
from lcd_api import LcdApi
from i2c_lcd import I2cLcd

pts = 0

sdaPIN = machine.Pin(0)
sclPIN = machine.Pin(1)

I2C_ADDR = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

i2c = machine.I2C(0,sda=sdaPIN, scl=sclPIN, freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

leds = {'red':machine.Pin(16, machine.Pin.OUT),
        'blue':machine.Pin(17, machine.Pin.OUT),
        'green':machine.Pin(18, machine.Pin.OUT),
        'yellow':machine.Pin(19, machine.Pin.OUT)}

redBut = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)
blueBut = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)
greenBut = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_UP)
yellowBut = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP)
resetBut = machine.Pin(25, machine.Pin.IN, machine.Pin.PULL_UP)

arrRandLed = []
bz_pin = machine.Pin(22, machine.Pin.OUT)
bz_pin.value(0)
bz = machine.Signal(bz_pin)

def gameOver(pts, leds):
    lcd.clear()
    for i in range(3):
        bz.value(1)
        leds['red'].on()
        lcd.putstr(' GAME OVER ')
        lcd.move_to(0, 1)
        lcd.putstr(f' SCORE: {pts} ')
        utime.sleep(0.4)
        leds['red'].off()
        leds['blue'].on()
        bz.value(0.5)
        utime.sleep(0.4)
        leds['blue'].off()
        leds['green'].on()
        bz.value(0)
        utime.sleep(0.4)
        leds['green'].off()
    utime.sleep(0.5)
    for led in leds.values():
        led.off()
    lcd.clear()
    utime.sleep(0.1)
    lcd.putstr(' PUSH RESET')
    lcd.move_to(0, 1)
    lcd.putstr(' BUTTON')
    while resetBut.value():
        utime.sleep(0.1)
    lcd.clear()
    lcd.putstr('Nouvelle Partie')
    utime.sleep(1)
    lcd.clear()
    loop()

def activeBuzzer(led):
    if led == leds['red']:
        bz.value(0.8)
    elif led == leds['blue']:
        bz.value(0.6)
    elif led == leds['green']:
        bz.value(0.4)
    elif led == leds['yellow']:
        bz.value(0.2)

def defineLcdOutput(led):
    if led == leds['red']:
        lcd.putstr(' ROUGE  ')
    elif led == leds['blue']:
        lcd.putstr('  BLEU  ')
    elif led == leds['green']:
        lcd.putstr('  VERT  ')
    elif led == leds['yellow']:
        lcd.putstr('  JAUNE  ')

def loop():
    pts = 0
    arrRandLed = []
    while True:
        utime.sleep(0.5)
        rng = random.randint(1, 4)
        if rng == 1:
            arrRandLed.append(leds['red'])
        if rng == 2:
            arrRandLed.append(leds['blue'])
        if rng == 3:
            arrRandLed.append(leds['green'])
        if rng == 4:
            arrRandLed.append(leds['yellow'])
        utime.sleep(0.1)
        for led in arrRandLed:
            activeBuzzer(led)
            defineLcdOutput(led)
            led.on()
            utime.sleep(0.5)
            bz.value(0)
            led.off()
            lcd.clear()
            utime.sleep(0.3)
        lcd.putstr(' A TON TOUR !')
        lcd.move_to(0, 1)
        lcd.putstr(f' SCORE: {pts} ')

        for led in arrRandLed:
            playerInputOk = False
            while not playerInputOk:
                if led == leds['red']:
                    if blueBut.value() == 1 or greenBut.value() == 1:
                        led.on()
                        gameOver(pts, leds)
                    elif redBut.value() == 1:
                        while redBut.value() == 1:
                            led.on()
                            activeBuzzer(led)
                            defineLcdOutput(led)
                        utime.sleep(0.2)
                        bz.value(0)
                        led.off()
                        lcd.clear()
                        playerInputOk = True
                    else:
                        led.off()
                        
                elif led == leds['blue']:
                    if redBut.value() == 1 or greenBut.value() == 1:
                        led.on()
                        gameOver(pts, leds)
                    elif blueBut.value() == 1:
                        while blueBut.value() == 1:
                            led.on()
                            activeBuzzer(led)
                            defineLcdOutput(led)
                        utime.sleep(0.2)
                        bz.value(0)
                        led.off()
                        lcd.clear()
                        playerInputOk = True
                    else:
                        led.off()
                        
                elif led == leds['green']:
                    if blueBut.value() == 1 or redBut.value() == 1:
                        led.on()
                        gameOver(pts, leds)
                    elif greenBut.value() == 1:
                        while greenBut.value() == 1:
                            led.on()
                            activeBuzzer(led)
                            defineLcdOutput(led)
                        utime.sleep(0.2)
                        bz.value(0)
                        led.off()
                        lcd.clear()
                        playerInputOk = True
                    else:
                        led.off()
                        
                elif led == leds['yellow']:
                    if blueBut.value() == 1 or redBut.value() == 1:
                        led.on()
                        gameOver(pts, leds)
                    elif yellowBut.value() == 1:
                        while yellowBut.value() == 1:
                            led.on()
                            activeBuzzer(led)
                            defineLcdOutput(led)
                        utime.sleep(0.2)
                        bz.value(0)
                        led.off()
                        lcd.clear()
                        playerInputOk = True
                    else:
                        led.off()
                        bz.value(0)

        pts += 1

if __name__ == '__main__':
    print('Program is starting...')
    loop()
