#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
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
server.wait_for_connection()

wait(1000)

hub = "hub1"
room_current = "ready"

button_delay = 150


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

    global button_delay

    wait(button_delay)
    if(button_fill_finish.pressed() != True):
        return False

    print("fill_finish")
    room_current = "fill_finish"
    mailbox_status.send("fill_finish")

    response = urequests.get("http://192.168.1.10:8888/queue.php?next=virtual.mp4")

    counter = 0

    motorA.dc(100)

    while counter < 100:
        wait(100)
        counter += 1
        if check_buttons():
            counter = 10000
        

    print("end of fill_finish")

    stop_all()
    

def process_development():

    global button_delay

    wait(button_delay)
    if(button_process_development.pressed() != True):
        return False

    print("process_development")
    room_current = "process_development"
    mailbox_status.send("process_development")

    response = urequests.get("http://192.168.1.10:8888/queue.php?next=drops.mp4")

    counter = 0

    motorB.dc(100)

    while counter < 100:
        wait(100)
        counter += 1
        if check_buttons():
            counter = 10000
        

    print("end of process_development")

    stop_all()

def check_buttons():

    global room_current, button_delay

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

def mailbox():

    global room_current

    while True:
        mailbox_status.wait()
        print(mailbox_status.read() + " - " + room_current)
        if(mailbox_status.read() != room_current):
            mailbox_status.send(room_current)
            stop_all()

threading.Thread(target=mailbox).start()

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

    wait(250)

# Write your program here.
ev3.speaker.beep()
