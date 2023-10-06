from machine import Pin, PWM, I2C
import utime
import random
from lcd_api import LcdApi
from i2c_lcd import I2cLcd

# LCD screen
sdaPIN = Pin(0)
sclPIN = Pin(1)
I2C_ADDR = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16
i2c = I2C(0,sda=sdaPIN, scl=sclPIN, freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

# Leds dict
leds = {'red':Pin(16, Pin.OUT), 
        'blue':Pin(17, Pin.OUT), 
        'green':Pin(18, Pin.OUT), 
        'yellow':Pin(19, Pin.OUT)} 

# Buttons for leds and reset
redBut = Pin(15, Pin.IN, Pin.PULL_UP)
blueBut = Pin(14, Pin.IN, Pin.PULL_UP)
greenBut = Pin(13, Pin.IN, Pin.PULL_UP)
yellowBut = Pin(12, Pin.IN, Pin.PULL_UP)
resetBut = Pin(21, Pin.IN)

# note frequences
LA=440
SOL=391
FA=349
MI=329
DUTY=32767
bz = PWM(Pin(22, Pin.OUT))

# Var for game loop
pts = 0
arrRandLed = []
playerInputOk = False

def gameOver(pin):
    global pts
    global leds
    lcd.clear()
    lcd.putstr(' GAME OVER ')
    lcd.move_to(0, 1)
    lcd.putstr(f' SCORE: {pts} ')
    for i in range(3):
        bz.duty_u16(DUTY)
        bz.freq(LA)
        leds['red'].on()
        utime.sleep(0.4)
        leds['red'].off()
        leds['blue'].on()       
        bz.freq(SOL)
        utime.sleep(0.4)
        leds['blue'].off()
        leds['green'].on()
        bz.freq(FA)
        utime.sleep(0.4)
        leds['green'].off()
        leds['yellow'].on()
        bz.freq(MI)
        utime.sleep(0.4)
        leds['yellow'].off()
        stopBuzzer()
    utime.sleep(0.5)
    for led in leds.values():
        led.off()
    lcd.clear()
    utime.sleep(0.1)
    lcd.putstr(' PUSH RESET')
    lcd.move_to(0, 1)
    lcd.putstr(' BUTTON')
    while resetBut.value() == 0:
        utime.sleep(0.1)
    lcd.clear()
    lcd.putstr('Nouvelle Partie')
    utime.sleep(1)
    lcd.clear()
    pts = 0
    arrRandLed = []
    loop(pts, arrRandLed)

def choice(x):
    return x[random.randrange(0, len(x))]

def activeBuzzer(led):
    bz.duty_u16(DUTY)
    if led == leds['red']:
        bz.freq(LA)
    elif led == leds['blue']:
        bz.freq(SOL)
    elif led == leds['green']:
        bz.freq(FA)
    elif led == leds['yellow']:
        bz.freq(MI)

def stopBuzzer():
    bz.duty_u16(0)

def win(pin, led):
    global playerInputOk
    led.on()
    activeBuzzer(led)
    defineLcdOutput(led)
    utime.sleep(0.3)
    led.off()
    stopBuzzer()
    playerInputOk = True

def defineLcdOutput(led):
    if led == leds['red']:
        lcd.putstr(' ROUGE  ')
    elif led == leds['blue']:
        lcd.putstr('  BLEU  ')
    elif led == leds['green']:
        lcd.putstr('  VERT  ')
    elif led == leds['yellow']:
        lcd.putstr(' JAUNE ')

def simonTurn(pts, arrRandLed):
    utime.sleep(0.2)
    arrRandLed.append(choice([led for led in leds.values()]))
    utime.sleep(0.1)
    for led in arrRandLed:
        activeBuzzer(led)
        defineLcdOutput(led)
        led.on()
        utime.sleep(0.5)
        stopBuzzer()
        led.off()
        lcd.clear()
        utime.sleep(0.3)
    lcd.putstr(' A TON TOUR !')
    lcd.move_to(0, 1)
    lcd.putstr(f' SCORE: {pts} ')

def test(pin):
    print(f'ok {pin}')

def loop(pts, arrRandLed):
    global playerInputOk
    
    while True:
        simonTurn(pts, arrRandLed)
        for led in arrRandLed:
            playerInputOk = False
            while not playerInputOk:
                utime.sleep(0.1)
                if led == leds['red']:
                    print('dans red')
                    blueBut.irq(trigger=Pin.IRQ_FALLING, handler=gameOver)
                    greenBut.irq(trigger=Pin.IRQ_FALLING, handler=gameOver)
                    yellowBut.irq(trigger=Pin.IRQ_FALLING, handler=gameOver)
                    redBut.irq(trigger=Pin.IRQ_FALLING, handler=lambda pin, arg=led: win(pin, arg))
                elif led == leds['blue']:
                    print('dans red')
                    blueBut.irq(trigger=Pin.IRQ_FALLING, handler=lambda pin, arg=led: win(pin, arg))
                    greenBut.irq(trigger=Pin.IRQ_FALLING, handler=gameOver)
                    yellowBut.irq(trigger=Pin.IRQ_FALLING, handler=gameOver)
                    redBut.irq(trigger=Pin.IRQ_FALLING, handler=gameOver)
                elif led == leds['green']:
                    print('dans red')
                    blueBut.irq(trigger=Pin.IRQ_FALLING,handler=gameOver)
                    greenBut.irq(trigger=Pin.IRQ_FALLING,handler=lambda pin, arg=led: win(pin, arg))
                    yellowBut.irq(trigger=Pin.IRQ_FALLING,handler=gameOver)
                    redBut.irq(trigger=Pin.IRQ_FALLING,handler=gameOver)
                elif led == leds['yellow']:
                    print('dans red')
                    blueBut.irq(trigger=Pin.IRQ_FALLING,handler=gameOver)
                    greenBut.irq(trigger=Pin.IRQ_FALLING,handler=gameOver)
                    yellowBut.irq(trigger=Pin.IRQ_FALLING,handler=lambda pin, arg=led: win(pin, arg))
                    redBut.irq(trigger=Pin.IRQ_FALLING,handler=gameOver)

        pts += 1

if __name__ == '__main__':
    print('Program is starting...')
    loop(pts, arrRandLed)
            
                # if led == leds['red']:
                #     if blueBut.value() == 1 or greenBut.value() == 1 or yellowBut.value() == 1:
                #         led.on()
                #         gameOver()
                #     elif redBut.value() == 1:
                #         while redBut.value() == 1:
                #             led.on()
                #             activeBuzzer(led)
                #             defineLcdOutput(led)
                #         utime.sleep(0.2)
                #         bz.duty_u16(0)
                #         led.off()
                #         lcd.clear()
                #         playerInputOk = True
                #     else:
                #         led.off()
                        
                # elif led == leds['blue']:
                #     if redBut.value() == 1 or greenBut.value() == 1 or yellowBut.value() == 1:
                #         led.on()
                #         gameOver()
                #     elif blueBut.value() == 1:
                #         while blueBut.value() == 1:
                #             led.on()
                #             activeBuzzer(led)
                #             defineLcdOutput(led)
                #         utime.sleep(0.2)
                #         bz.duty_u16(0)
                #         led.off()
                #         lcd.clear()
                #         playerInputOk = True
                #     else:
                #         led.off()
                        
                # elif led == leds['green']:
                #     if blueBut.value() == 1 or redBut.value() == 1 or yellowBut.value() == 1:
                #         led.on()
                #         gameOver()
                #     elif greenBut.value() == 1:
                #         while greenBut.value() == 1:
                #             led.on()
                #             activeBuzzer(led)
                #             defineLcdOutput(led)
                #         utime.sleep(0.2)
                #         bz.duty_u16(0)
                #         led.off()
                #         lcd.clear()
                #         playerInputOk = True
                #     else:
                #         led.off()
                        
                # elif led == leds['yellow']:
                #     if blueBut.value() == 1 or redBut.value() == 1 or greenBut.value() == 1:
                #         led.on()
                #         gameOver()
                #     elif yellowBut.value() == 1:
                #         while yellowBut.value() == 1:
                #             led.on()
                #             activeBuzzer(led)
                #             defineLcdOutput(led)
                #         utime.sleep(0.2)
                #         bz.duty_u16(0)
                #         led.off()
                #         lcd.clear()
                #         playerInputOk = True
                #     else:
                #         led.off()
                #         bz.duty_u16(0)

