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

hub = "hub-b"
room_current = "ready"

button_delay = 150


# Create your objects here.
ev3 = EV3Brick()
ev3.speaker.beep()

# Initialize EV3 touch sensor and motors
motorA = Motor(Port.A)
motorB = Motor(Port.B)
motorC = Motor(Port.C)
motorD = Motor(Port.D)

'''
# Testing interactive components
motorB.dc(35)
motorC.dc(30)

wait(6000)

motorA.dc(30)
motorD.dc(50)
motorB.dc(0)
motorC.dc(0)

wait(6000)

motorA.dc(0)
motorD.dc(0)

exit
'''

button_joinn = TouchSensor(Port.S1)
button_scorpius = TouchSensor(Port.S2)

def press(room_new):

    global room_current

    print("starting " + room_new)

    if(room_new == "joinn"):
        joinn()

    elif(room_new ==  "scorpius"):
        scorpius()

def stop_all():

    global room_current
    room_current = "ready"

    motorA.dc(0)
    motorB.dc(0)
    motorC.dc(0)
    motorD.dc(0)
    
    # mailbox_status.send("ready")

    print("end of stop_all")    

def joinn():

    global button_delay, room_current

    wait(button_delay)
    if(button_joinn.pressed() != True):
        return False
    elif(room_current == "joinn"):
        return False

    stop_all()

    print("joinn")
    room_current = "joinn"
    mailbox_status.send("joinn")

    response = urequests.get("http://10.12.1.105:8888/queue.php?next=joinn.mp4")

    counter = 0

    motorA.dc(30)
    motorD.dc(50)

    while counter < 100:
        wait(100)
        counter += 1
        if check_buttons():
            counter = 10000

    print("end of joinn")

    stop_all()

def scorpius():

    global button_delay, room_current

    wait(button_delay)
    if(button_scorpius.pressed() != True):
        return False
    elif(room_current == "scorpius"):
        return False

    stop_all()

    print("scorpius")
    room_current = "scorpius"
    mailbox_status.send("scorpius")

    response = urequests.get("http://10.12.1.105:8888/queue.php?next=scorpius.mp4")

    counter = 0

    motorB.dc(35)
    motorC.dc(80)

    while counter < 100:
        wait(100)
        counter += 1
        if check_buttons():
            counter = 10000

    print("end of scorpius")

    stop_all()

def check_buttons():

    global room_current

    print("------------------------------")
    print("Checking buttons")
    print(room_current)

    if Button.CENTER in ev3.buttons.pressed():
        stop_all()
        return True

    elif(button_joinn.pressed() == True and room_current != "joinn"):
        print("button pressed")
        return True

    elif(button_scorpius.pressed() == True and room_current != "scorpius"):
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

    elif(button_joinn.pressed() == True):
        stop_all()
        press("joinn")

    elif(button_scorpius.pressed() == True):
        stop_all()
        press("scorpius")

    wait(250)

# Write your program here.
ev3.speaker.beep()
