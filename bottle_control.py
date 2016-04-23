#!/usr/bin/python
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

#|R|a|s|p|b|e|r|r|y|P|i|.|c|o|m|.|t|w|
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# Copyright (c) 2015, raspberrypi.com.tw
# All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
#
# bottle_control.py
# a web ui to control car to move forward/backward/left/right
#
# Author : sosorry
# Date   : 08/01/2015

from bottle import *
import RPi.GPIO as GPIO
import time
import sys

Motor_Horizontal_Pin = 11
Motor_Vertical_Pin = 13

h_shift = 0.3
v_shift = 0.2

h_in_use = 0;
v_in_use = 0;

pause_time = 0.1

h_position = 7
v_position = 8

h_upperbound = 11
h_lowerbound = 3
v_upperbound = 11
v_lowerbound = 5

GPIO.setmode(GPIO.BOARD)
GPIO.setup(Motor_Horizontal_Pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Motor_Vertical_Pin, GPIO.OUT, initial=GPIO.LOW)


def init(pin):
    pwm = GPIO.PWM(pin, 50)
    return pwm

def changePostion(pwm, position):
    time.sleep(pause_time)
    pwm.start(position)
    time.sleep(pause_time)
    pwm.stop()
    #GPIO.cleanup()

time.sleep(1)
changePostion(init(Motor_Horizontal_Pin), h_position)
time.sleep(1)
changePostion(init(Motor_Vertical_Pin), v_position)

def turnUp(v):
    global v_position
    if v_position + v_shift < v_upperbound:
        v_position += v_shift
    else:
        v_position = v_upperbound
    changePostion(v, v_position)

def turnDown(v):
    global v_position
    if v_position - v_shift > v_lowerbound:
        v_position -= v_shift
    else:
        v_position = v_lowerbound
    changePostion(v, v_position)

def turnRight(h):
    global h_position
    if h_position + h_shift < h_upperbound:
        h_position += h_shift
    else:
        h_position = h_upperbound
    changePostion(h, h_position)

def turnLeft(h):
    global h_position
    if h_position - h_shift > h_lowerbound:
        h_position -= h_shift
    else:
        h_position = h_lowerbound
    changePostion(h, h_position)

@get('/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='static/js')

@get('/<filename:re:.*\.css>')
def javascripts(filename):
    return static_file(filename, root='static/css')

@route('/')
def index():
    output = template('view')
    return output

@route('/ajax', method='POST')
def ajax():
    arrow = request.forms.get("arrow")
    sys.stderr.write(arrow+'\n')

    if v_in_use == 0:
        v_in_use = 1
        if int(arrow) == 40:
            turnUp(init(Motor_Vertical_Pin))
        if int(arrow) == 38:
            turnDown(init(Motor_Vertical_Pin))
        v_in_use = 0

    if h_in_use == 0:
        h_in_use = 1
        if int(arrow) == 37:
            turnRight(init(Motor_Horizontal_Pin))
        if int(arrow) == 39:
            turnLeft(init(Motor_Horizontal_Pin))
        h_in_use = 0

try:
    run(host='0.0.0.0', port=745)

finally:
    GPIO.cleanup()
