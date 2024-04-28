#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from pybricks.messaging import BluetoothMailboxClient, TextMailbox

import urequests
import threading

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.

client = BluetoothMailboxClient()
mailbox_status = TextMailbox("", client)
client.connect("delta")

wait(1000)

hub = "hub-c"
room_current = "ready"

button_delay = 150


# Create your objects here.
ev3 = EV3Brick()
ev3.speaker.beep()

# Initialize EV3 touch sensor and motors
# Screen
motorA = Motor(Port.A)
# Shaker
motorB = Motor(Port.B)

'''
# Testing interactive components
motorA.dc(40)
motorB.dc(35)


wait(6000)

motorA.dc(0)
motorB.dc(0)

exit
'''

button_biodextris = TouchSensor(Port.S1)

def press(room_new):

    global room_current

    print("starting " + room_new)

    if(room_new == "biodextris"):
        biodextris()

def stop_all():

    global room_current
    room_current = "ready"

    motorA.dc(0)
    motorB.dc(0)
    
    # mailbox_status.send("ready")

    print("end of stop_all")    

def biodextris():

    global button_delay, room_current

    wait(button_delay)
    if(button_biodextris.pressed() != True):
        return False
    elif(room_current == "biodextris"):
        return False

    stop_all()

    print("biodextris")
    room_current = "biodextris"
    mailbox_status.send("biodextris")

    response = urequests.get("http://10.12.1.105:8888/queue.php?next=biodextris.mp4")

    counter = 0

    motorA.dc(40)
    motorB.dc(30)

    while counter < 100:
        wait(100)
        counter += 1
        if check_buttons():
            counter = 10000

    print("end of biodextris")

    stop_all()

def check_buttons():

    global room_current

    print("------------------------------")
    print("Checking buttons")
    print(room_current)

    if Button.CENTER in ev3.buttons.pressed():
        stop_all()
        return True

    elif(button_biodextris.pressed() == True and room_current != "biodextris"):
        print("button pressed")
        return True

    return False

def mailbox():

    global room_current

    while True:

        mailbox_status.wait()

        print("------------------------------")
        print(mailbox_status.read())
        print(room_current)

        if(mailbox_status.read() != room_current):

            stop_all()

            room_current = mailbox_status.read()

threading.Thread(target=mailbox).start()

# Create a loop to react to distance
while True:

    if Button.CENTER in ev3.buttons.pressed():
        stop_all()
        break

    elif(button_biodextris.pressed() == True):
        stop_all()
        press("biodextris")

    wait(250)

# Write your program here.
ev3.speaker.beep()
