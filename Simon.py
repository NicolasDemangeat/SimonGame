#!/usr/bin/env python3
########################################################################
# Filename    : Simon.py
# Description : file de base
# auther      : darwin
# modification: 24/12/2022
########################################################################
from gpiozero import *
from time import sleep
from signal import pause
from random import *
from lcd_api import LcdApi
from i2c_lcd import I2cLcd

pts=0

I2C_ADDR = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

lcd = I2cLcd(1, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

leds = LEDBoard(red=17, blue=27, green=5)
leds.off()
redBut = Button(18)
blueBut = Button(23)
greenBut = Button(24)
resetBut = Button(25)
arrRandLed = []
bz = TonalBuzzer(22)

def gameOver(pts, leds):
    lcd.clear()
    for i in range(3):
        bz.value = 1
        leds.red.on()
        lcd.putstr(' GAME OVER ')
        lcd.move_to(0,1)
        lcd.putstr(f' SCORE: {pts} ')
        sleep(0.4)
        leds.red.off()
        leds.blue.on()
        bz.value = 0
        sleep(0.4)
        leds.blue.off()
        leds.green.on()
        bz.value = -1
        sleep(0.4)
        leds.green.off()
    bz.stop()
    sleep(0.5)
    leds.off()
    lcd.clear()
    sleep(0.1)
    lcd.putstr(' PUSH RESET')
    lcd.move_to(0,1)
    lcd.putstr(' BUTTON')
    resetBut.wait_for_press()
    lcd.clear()
    lcd.putstr('Nouvelle Partie')
    sleep(1)
    lcd.clear()
    loop()

def activeBuzzer(led):
    if led.pin.number == 17:
        bz.value=1
    elif led.pin.number == 27:
        bz.value=0
    elif led.pin.number == 5:
        bz.value=-1
    
def defineLcdOutput(led):
    if led.pin.number == 17:
        lcd.putstr(' ROUGE  ')
    elif led.pin.number == 27:
        lcd.putstr('  BLEU  ')
    elif led.pin.number == 5:
        lcd.putstr('  VERT  ')    
    
def loop():
    pts=0
    arrRandLed=[]
    while not resetBut.is_pressed:        
        sleep(0.5)
        arrRandLed.append(choice(leds))
        sleep(0.1)
        for led in arrRandLed:
            activeBuzzer(led)
            defineLcdOutput(led)
            led.on()
            sleep(0.5)
            bz.stop()
            led.off()
            lcd.clear()
            sleep(0.3)
        lcd.putstr(' A TON TOUR !')
        lcd.move_to(0,1)
        lcd.putstr(f' SCORE: {pts} ')

        for led in arrRandLed:
            playerInputOk = False
            while playerInputOk == False:
                if led.pin.number == 17:
                    if blueBut.is_pressed or greenBut.is_pressed:
                        led.on()
                        gameOver(pts, leds)
                    elif redBut.is_pressed:
                        while redBut.is_pressed:
                            led.on()
                            activeBuzzer(led)
                            defineLcdOutput(led)
                        sleep(0.2)
                        bz.stop()
                        led.off()
                        lcd.clear()
                        playerInputOk = True
                    else:
                        led.off()
                elif led.pin.number == 27:
                    if redBut.is_pressed or greenBut.is_pressed:
                        led.on()
                        gameOver(pts, leds)
                    elif blueBut.is_pressed:
                        while blueBut.is_pressed:
                            led.on()
                            activeBuzzer(led)
                            defineLcdOutput(led)
                        sleep(0.2)
                        bz.stop()
                        led.off()
                        lcd.clear()
                        playerInputOk = True
                    else:
                        led.off()
                elif led.pin.number == 5:
                    if blueBut.is_pressed or redBut.is_pressed:
                        led.on()
                        gameOver(pts, leds)
                    elif greenBut.is_pressed:
                        while greenBut.is_pressed:
                            led.on()
                            activeBuzzer(led)
                            defineLcdOutput(led)
                        sleep(0.2)
                        bz.stop()
                        led.off()
                        lcd.clear()
                        playerInputOk = True
                    else:
                        led.off()
                        bz.stop()
        pts+=1
        

if __name__ == '__main__':     # Program entrance
    print ('Program is starting...')
    loop()