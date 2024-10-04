#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.iodevices import DCMotor                                 
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from pybricks.messaging import BluetoothMailboxClient, TextMailbox

import urequests
import threading
import random

# Create your objects here.
ev3 = EV3Brick()
ev3.speaker.set_speech_options(None, 'f2')
ev3.speaker.beep()

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.
mailbox_on = True
video_on = True
lull_on = True

if mailbox_on == True:
    ev3.speaker.say("Blue Tooth")

    client = BluetoothMailboxClient()
    mailbox_status = TextMailbox("", client)
    client.connect("delta")

    ev3.speaker.say("Connected")
else:
    ev3.speaker.say("Blue Tooth Off")

hub = "hub-c"
room_current = "ready"
ip = "10.12.1.105:8888"
# ip = "10.12.1.129"

animation = 20
button_delay = 150
elevator_position = "top"

# Initialize EV3 touch sensor and motors
# Biodextris Screen
# Biodextris Shaker
# Global Lights
# Hub ls LEFT most hub
# Usualy Hub FOXTROT
# ---
motorA = Motor(Port.A)
motorB = Motor(Port.B)
motorC = DCMotor(Port.C)
# motorD = Motor(Port.D)


# Truen lights on
motorC.dc(100)

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

def button_beep():

    ev3.speaker.beep()

def press(room_new):

    global room_current

    print("starting " + room_new)

    if(room_new == "biodextris"):
        biodextris()

def stop_all():

    global room_current, mailbox_on, mailbox_status
    room_current = "ready"

    motorA.dc(0)
    motorB.dc(0)
    
    print("end of stop_all")    

def biodextris():

    global button_delay, room_current, mailbox_on, mailbox_status

    wait(button_delay)
    if(button_biodextris.pressed() != True):
        return False
    elif(room_current == "biodextris"):
        return False

    stop_all()

    button_beep()

    print("biodextris")
    room_current = "biodextris"

    if mailbox_on == True:
        try:
            mailbox_status.send("biodextris")
        except:
            print("Error with biodextris mailbox")

    if video_on == True:
        response = urequests.get("http://" + ip + "/queue.php?next=process-development.mp4")

    counter = 0

    motorA.dc(40)
    motorB.dc(30)

    while counter < 10 * animation:
        wait(100)
        counter += 1
        if check_buttons():
            counter = 1000 * animation

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
            except:
                print("Error with thread mailbox")

if mailbox_on == True:
    threading.Thread(target=mailbox).start()

def lull():

    global room_current, elevator_position

    lull_random_from = 10
    lull_random_to = 15

    lull_counter = 0
    lull_random = random.randint(lull_random_from,lull_random_to)
    lull_motor = random.randint(1,2)
    # lull_motor = 3

    while True:

        print(room_current)
        print(lull_counter)
        print(lull_random)
        print(lull_motor)

        lull_counter += 1

        if room_current == "biodextris":

            lull_counter = 0

        elif lull_counter > lull_random + 5:

            lull_counter = 0
            lull_random = random.randint(lull_random_from,lull_random_to)
            lull_motor = random.randint(1,2)
            # lull_motor = 4

            motorA.dc(0)
            motorB.dc(0)
            # motorD.dc(0)

        elif lull_counter > lull_random: 

            if lull_motor == 1:
                motorA.dc(40)
            elif lull_motor == 2:
                motorB.dc(30)
            elif lull_motor == 3:
                
                # if elevator_position == "top":

                # elevator_position = "bottom"
                # motorD.run_until_stalled(-80, Stop.COAST, 50)
                print("bottom")

            elif lull_motor == 4:

                # elif elevator_position == "bottom":

                # elevator_position = "top"
                # motorD.run_until_stalled(80, Stop.COAST, 50)
                print("bottom")
            
        wait(1000)

if lull_on == True:
    threading.Thread(target=lull).start()

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
