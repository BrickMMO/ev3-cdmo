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

# Create your objects here.
ev3 = EV3Brick()
ev3.speaker.set_speech_options(None, 'f1')
ev3.speaker.beep()

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.
mailbox_on = True

if mailbox_on == True:
    ev3.speaker.say("Blue Tooth")

    client = BluetoothMailboxClient()
    mailbox_status = TextMailbox("", client)
    client.connect("delta")

    ev3.speaker.say("Connected")
else:
    ev3.speaker.say("Blue Tooth Off")

hub = "hub-b"
room_current = "ready"
ip = "192.168.1.9:8888"

animation = 20
button_delay = 150

# Initialize EV3 touch sensor and motors
# JOINN Rocker
# Scorpius Sampler
# Scorpius Screen
# JOINN Bioreactor
motorA = Motor(Port.A)
motorB = Motor(Port.B)
motorC = Motor(Port.C)
motorD = Motor(Port.D)

'''
# Testing interactive components
motorC.dc(-40)

wait(30000)

motorA.dc(0)
motorB.dc(0)
motorC.dc(0)
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

    global room_current, mailbox_on, mailbox_status

    room_current = "ready"

    motorA.dc(0)
    motorB.dc(0)
    motorC.dc(0)
    motorD.dc(0)
    
    '''
    if mailbox_on == True:
        try:
            mailbox_status.send("ready")
        except:
            print("Error with stop all mailbox")
    '''
    
    print("end of stop_all")    

def joinn():

    global button_delay, room_current, mailbox_on, mailbox_status

    wait(button_delay)
    if(button_joinn.pressed() != True):
        return False
    elif(room_current == "joinn"):
        return False

    stop_all()

    print("joinn")
    room_current = "joinn"

    if mailbox_on == True:
        try:
            mailbox_status.send("joinn")
        except:
            print("Error with joinn mailbox")
    
    response = urequests.get("http://" + ip + "/queue.php?next=joinn.mp4")

    counter = 0

    motorA.dc(30)
    motorD.dc(50)

    while counter < 10 * animation:
        wait(100)
        counter += 1
        if check_buttons():
            counter = 1000 * animation

    print("end of joinn")

    stop_all()

def scorpius():

    global button_delay, room_current, mailbox_on, mailbox_status

    wait(button_delay)
    if(button_scorpius.pressed() != True):
        return False
    elif(room_current == "scorpius"):
        return False

    stop_all()

    print("scorpius")
    room_current = "scorpius"

    if mailbox_on == True:
        try:
            mailbox_status.send("scorpius")
        except:
            print("Error with scorpius mailbox")

    response = urequests.get("http://" + ip + "/queue.php?next=scorpius.mp4")

    counter = 0

    motorB.dc(35)
    motorC.dc(-40)    

    while counter < 10 * animation:
        wait(100)
        counter += 1
        if check_buttons():
            counter = 1000 * animation

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

    while True:

        global room_current, mailbox_status

        mailbox_status.wait()
        
        print("------------------------------")
        print(mailbox_status.read())
        print(room_current)

        if(mailbox_status.read() != room_current):

            stop_all()

            try:
                room_current = mailbox_status.read()
            except:
                print("Error with thread mailbox")

if mailbox_on == True:
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
