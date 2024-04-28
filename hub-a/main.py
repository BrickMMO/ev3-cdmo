#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.iodevices import DCMotor
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from pybricks.messaging import BluetoothMailboxServer, TextMailbox

import urequests
import threading

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.

server = BluetoothMailboxServer()
mailbox_status = TextMailbox("", server)
server.wait_for_connection(2)

wait(2000)

hub = "hub-a"
room_current = "ready"

button_delay = 150

# Create your objects here.
ev3 = EV3Brick()
ev3.speaker.beep()

# Initialize EV3 touch sensor and motors
motorA = Motor(Port.A)
motorB = Motor(Port.B)
# motorC = Motor(Port.C)
motorD = DCMotor(Port.D)

motorD.dc(100)

'''
# Testing interactive components
motorA.dc(-60)
motorB.dc(60)

wait(5000)

motorA.dc(0)
motorB.dc(0)
'''

button_argonaut = TouchSensor(Port.S1)
button_wheeler = TouchSensor(Port.S2)

def press(room_new):

    print("starting " + room_new)

    if(room_new == "argonaut"):
        argonaut()

    elif(room_new == "wheeler"):
        wheeler()

def stop_all():

    global room_current
    room_current = "ready"

    motorA.dc(0)
    motorB.dc(0)
    # motorC.dc(0)

    print("end of stop_all")

def argonaut():

    global button_delay, room_current

    wait(button_delay)
    if(button_argonaut.pressed() != True):
        return False
    elif(room_current == "argonaut"):
        return False

    stop_all()

    print("argonaut")
    room_current = "argonaut"
    mailbox_status.send("argonaut")

    response = urequests.get("http://10.12.1.105:8888/queue.php?next=argonaut.mp4")

    counter = 0

    motorA.dc(-60)

    while counter < 100:
        wait(100)
        counter += 1
        if check_buttons():
            counter = 10000

    print("end of argonaut")

    stop_all()
    

def wheeler():

    global button_delay, room_current

    wait(button_delay)
    if(button_wheeler.pressed() != True):
        return False
    elif(room_current == "wheeler"):
        return False

    stop_all()

    print("wheeler")
    room_current = "wheeler"
    mailbox_status.send("wheeler")

    response = urequests.get("http://10.12.1.105:8888/queue.php?next=wheeler.mp4")

    counter = 0

    motorB.dc(50)
    # motorC.dc(50)

    while counter < 100:
        wait(100)
        counter += 1
        if check_buttons():
            counter = 10000
        
    print("end of wheeler")

    stop_all()

def check_buttons():

    global room_current, button_delay

    if Button.CENTER in ev3.buttons.pressed():
        stop_all()
        return True

    elif(button_argonaut.pressed() == True and room_current != "argonaut"):
        print("button pressed")
        return True

    elif(button_wheeler.pressed() == True and room_current != "wheeler"):
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
            mailbox_status.send(room_current)

threading.Thread(target=mailbox).start()

# Create a loop to react to distance
while True:

    if Button.CENTER in ev3.buttons.pressed():
        break

    elif(button_argonaut.pressed() == True):
        stop_all()
        press("argonaut")

    elif(button_wheeler.pressed() == True):
        stop_all()
        press("wheeler")

    wait(250)

# Write your program here.
ev3.speaker.beep()
