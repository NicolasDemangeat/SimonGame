# SimonGame

## Introduction

Lors de mon apprentissage de l'électronique je me suis lancé le défi de reproduire un de mes jeux d’enfance : . [le Simon](https://fr.wikipedia.org/wiki/Simon_(jeu))


J’ai commencé avec un [Raspberry pi 4](https://fr.wikipedia.org/wiki/Raspberry_Pi) et le code en Python que vous trouverez de le dossier   [Simon-RpiV1.0](/Simon-RP2040V1.0/)


Dans le but de ne pas mobiliser un Raspberry pi4 pour ce petit jeu, j’ai décidé de porter le code en utilisant MicroPython et d’utiliser un [Raspberry pico](https://fr.wikipedia.org/wiki/Raspberry_Pi_Pico)
Le code se trouve dans le dossier [Simon-RP2040V1.0](/Simon-RP2040V1.0/)

## Instructions

### Composants

- Un Raspberry pi 4 ou Raspberry pico
- 4 leds (rouge, bleu, jaune, vert)
- 4 resistance de 220ohms (ou plus)
- 4 boutons poussoirs de couleur correpondant aux leds
- 1 bouton poussoir 6x6x4
- 1 buzzer passif
- des cables
- 1 écran LCD1602 en i2c (optionnel)

![cablage](/simonrp2040.jpeg)

### Montage

- LCD SDA : PIN 0
- LCD SCL : PIN 1
- LED Rouge : PIN 16 OUT
- LED Bleu : PIN 17 OUT
- LED Verte : PIN 18 OUT
- LED Jaune : PIN 19 OUT
- Bouton Rouge : PIN 15 IN
- Bouton Bleu : PIN 14 IN
- Bouton Vert : PIN 13 IN
- Bouton Jaune : PIN 12 IN
- Bouton Reset : PIN 21 IN
- Buzzer : PWM PIN 22 OUT

## TODO

- Schema de cablage
- Ameliorer le code
- Design 3D
- Gestion de l'alimentation par batterie avec interrupteur
