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
client.connect("bravo")

wait(1000)

hub = "hub2"
room_current = "ready"

button_delay = 150


# Create your objects here.
ev3 = EV3Brick()

# Initialize EV3 touch sensor and motors
motorA = Motor(Port.A)

button_upstream = TouchSensor(Port.S1)

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

    # mailbox_status.send("reset")  
    # print("mailbox_status " + mailbox_status.read())

    print("end of stop_all")    

def upstream():

    global button_delay, room_current

    wait(button_delay)
    if(button_upstream.pressed() != True):
        return False

    print("upstream")
    room_current = "upstream"
    mailbox_status.send("upstream")

    response = urequests.get("http://192.168.1.10:8888/queue.php?next=microscope.mp4")

    counter = 0

    motorA.dc(100)

    while counter < 100:
        wait(100)
        counter += 1
        if check_buttons():
            counter = 10000

    print("end of upstream")

    stop_all()

def check_buttons():

    global room_current

    if Button.CENTER in ev3.buttons.pressed():
        stop_all()
        return True

    elif(button_upstream.pressed() == True and room_current != "upstream"):
        stop_all()
        print("button pressed")
        return True

    return False

def mailbox():

    global room_current

    while True:
        mailbox_status.wait()
        print(mailbox_status.read() + " - " + room_current)
        if(mailbox_status.read() != room_current):
            stop_all()

threading.Thread(target=mailbox).start()

# Create a loop to react to distance
while True:

    if Button.CENTER in ev3.buttons.pressed():
        stop_all()
        break

    elif(button_upstream.pressed() == True):
        stop_all()
        press("upstream")

    wait(250)

# Write your program here.
ev3.speaker.beep()
