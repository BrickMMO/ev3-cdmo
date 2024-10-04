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
import random

# Create your objects here.
ev3 = EV3Brick()
ev3.speaker.set_speech_options(None, 'm1')
ev3.speaker.beep()

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.
mailbox_on = True
video_on = True
lull_on = True

if mailbox_on == True:
    ev3.speaker.say("Blue Tooth")

    server = BluetoothMailboxServer()
    mailbox_status = TextMailbox("", server)
    server.wait_for_connection(2)

    wait(2000)

    ev3.speaker.say("Connected")
    ev3.speaker.say("Found Hubs")
else:
    ev3.speaker.say("Blue Tooth Off")

hub = "hub-a"
room_current = "ready"
ip = "10.12.1.105:8888"
# ip = "10.12.1.129"

# print("http://" + ip + "/queue.php?next=argonaut.mp4")
# response = urequests.get("http://" + ip + "/queue.php?next=argonaut.mp4")
# print(response)

animation = 20
button_delay = 150

# Initialize EV3 touch sensor and motors
# Argonaut Fill Line
# Wheeler Bioreactor
# Wheeler Screen
# Global Lights
# Hub ls RIGHT most hub
# Usualy Hub DELTA
motorA = Motor(Port.A)
motorB = Motor(Port.B)
motorC = Motor(Port.C)
motorD = DCMotor(Port.D)

# Truen lights on
# motorD.dc(100)

'''
# Testing interactive components
motorA.dc(-60)
motorB.dc(60)
motorC.dc(80)

wait(5000)

motorA.dc(0)
motorB.dc(0)        
motorC.dc(0)

exit
'''

button_argonaut = TouchSensor(Port.S1)
button_wheeler = TouchSensor(Port.S2)

def button_beep():

    ev3.speaker.beep()

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
    motorC.dc(0)

    print("end of stop_all")

def argonaut():

    global button_delay, room_current, mailbox_on, mailbox_status

    wait(button_delay)
    if(button_argonaut.pressed() != True):
        return False
    elif(room_current == "argonaut"):
        return False

    stop_all()

    button_beep()

    print("argonaut")
    room_current = "argonaut"

    if mailbox_on == True:
        try:
            mailbox_status.send("argonaut")
        except:
            print("Error with argonaut mailbox")

    if video_on == True:
        print("TEST")
        response = urequests.get("http://" + ip + "/queue.php?next=fill-finish.mp4")
        print(response)

    counter = 0

    motorA.dc(-60)

    while counter < 10 * animation:
        wait(100)
        counter += 1
        if check_buttons():
            counter = 1000 * animation

    print("end of argonaut")

    stop_all()
    

def wheeler():

    global button_delay, room_current, mailbox_on, mailbox_status

    wait(button_delay)
    if(button_wheeler.pressed() != True):
        return False
    elif(room_current == "wheeler"):
        return False

    stop_all()

    button_beep()

    print("wheeler")
    room_current = "wheeler"

    if mailbox_on == True:
        try:
            mailbox_status.send("wheeler")
        except:
            print("Error with wheeler mailbox")

    if video_on == True:
        print("TEST")
        response = urequests.get("http://" + ip + "/queue.php?next=downstream.mp4")
        print(response)

    counter = 0

    motorB.dc(60)
    motorC.dc(70)

    while counter < 10 * animation:
        wait(100)
        counter += 1
        if check_buttons():
            counter = 1000 * animation
        
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

    global room_current, mailbox_status

    while True:
        
        mailbox_status.wait()

        print("------------------------------")
        print(mailbox_status.read())
        print(room_current)

        if(mailbox_status.read() != room_current):

            stop_all()

            try:
                room_current = mailbox_status.read()
                mailbox_status.send(room_current)
            except:
                print("Error with thread mailbox")

if mailbox_on == True:
    threading.Thread(target=mailbox).start()

def lull():

    global room_current

    lull_random_from = 30
    lull_random_to = 40

    lull_counter = 0
    lull_random = random.randint(lull_random_from,lull_random_to)
    lull_motor = random.randint(1,3)

    while True:

        print(room_current)
        print(lull_counter)
        print(lull_random)
        print(lull_motor)

        lull_counter += 1

        if room_current == "wheeler" or room_current == "argonaut":

            lull_counter = 0

        elif lull_counter > lull_random + 5: 

            lull_counter = 0
            lull_random = random.randint(lull_random_from,lull_random_to)
            lull_motor = random.randint(1,3)

            motorA.dc(0)
            motorB.dc(0)
            motorC.dc(0)

        elif lull_counter > lull_random: 

            if lull_motor == 1:
                motorA.dc(-60)
            elif lull_motor == 2:
                motorB.dc(60)
            elif lull_motor == 3:
                motorC.dc(70)
            
        wait(1000)

if lull_on == True:
    threading.Thread(target=lull).start()

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
