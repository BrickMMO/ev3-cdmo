#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

import urequests

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.

# server = BluetoothMailboxServer()
# server.wait_for_connection(1)

# mailbox_room = TextMailbox("", server)

hub = "hub1"
room_current = "ready"


# Create your objects here.
ev3 = EV3Brick()

# Initialize EV3 touch sensor and motors
motorA = Motor(Port.A)
motorB = Motor(Port.B)

button_fill_finish = TouchSensor(Port.S1)
button_process_development = TouchSensor(Port.S2)

def press(room_new):

    global room_current

    room_current = room_new
    print("starting " + room_current)

    if(room_current == "fill_finish"):
        fill_finish()

    elif(room_current == "process_development"):
        process_development()

    elif(room_current == "upstream"):
        upstream()

    elif(room_current ==  "downstream"):
        downstream()

    elif(room_current == "quality"):
        quality()

def stop_all():

    global room_current
    room_current = "ready"

    motorA.dc(0)
    motorB.dc(0)

    print("end of stop_all")

def fill_finish():

    print("fill_finish")

    response = urequests.get("http://192.168.1.10:8888/queue.php?next=virtual.mp4")

    counter = 0

    motorA.dc(100)

    while counter < 400:
        wait(25)
        counter += 1
        if check_buttons():
            counter = 10000
        

    print("end of fill_finish")

    stop_all()
    

def process_development():

    print("process_development")

    response = urequests.get("http://192.168.1.10:8888/queue.php?next=drops.mp4")

    counter = 0

    motorB.dc(100)

    while counter < 400:
        wait(25)
        counter += 1
        if check_buttons():
            counter = 10000
        

    print("end of process_development")

    stop_all()

def check_buttons():

    global room_current

    if Button.CENTER in ev3.buttons.pressed():
        stop_all()
        return True

    elif(button_fill_finish.pressed() == True and room_current != "fill_finish"):
        stop_all()
        print("button pressed")
        return True

    elif(button_process_development.pressed() == True and room_current != "process_development"):
        stop_all()
        print("button pressed")
        return True

    return False


# Create a loop to react to distance
while True:

    if Button.CENTER in ev3.buttons.pressed():
        break

    elif(button_fill_finish.pressed() == True):
        stop_all()
        press("fill_finish")

    elif(button_process_development.pressed() == True):
        stop_all()
        press("process_development")

    wait(100)

# Write your program here.
ev3.speaker.beep()
