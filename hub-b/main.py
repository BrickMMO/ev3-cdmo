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

'''
client = BluetoothMailboxClient()
mailbox_status = TextMailbox("", client)
client.connect("delta")
'''

wait(1000)

hub = "hub-b"
room_current = "ready"

animation = 20
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
# motorA.dc(30)
# motorB.dc(50)
# motorC.dc(50)
motorD.dc(50)

wait(6000)

motorA.dc(0)
motorB.dc(0)
motorC.dc(0)
motorD.dc(0)

exit
'''

button_joinn = TouchSensor(Port.S1)
button_scorpius = TouchSensor(Port.S1)

def press(room_new):

    global room_current

    room_current = room_new
    print("starting " + room_current)

    if(room_current == "argonaut"):
        argonaut()

    elif(room_current == "wheeler"):
        wheeler()

    elif(room_current == "joinn"):
        joinn()

    elif(room_current ==  "scorpius"):
        scorpius()

    elif(room_current == "biodextris"):
        biodextris()

def stop_all():

    global room_current
    room_current = "ready"

    motorA.dc(0)

    # mailbox_status.send("reset")  
    # print("mailbox_status " + mailbox_status.read())

    print("end of stop_all")    

def joinn():

    global button_delay, room_current

    wait(button_delay)
    if(button_joinn.pressed() != True):
        return False

    print("joinn")
    room_current = "joinn"
    # mailbox_status.send("joinn")

    response = urequests.get("http://192.168.1.15:8888/queue.php?next=joinn.mp4")

    counter = 0

    motorA.dc(100)

    while counter < 10 * animation:
        wait(100)
        counter += 1
        if check_buttons():
            counter = 1000 * animation

    print("end of joinn")

    stop_all()

def scorpius():

    global button_delay, room_current

    wait(button_delay)
    if(button_scorpius.pressed() != True):
        return False

    print("scorpius")
    room_current = "scorpius"
    # mailbox_status.send("scorpius")

    response = urequests.get("http://192.168.1.15:8888/queue.php?next=scorpius.mp4")

    counter = 0

    motorA.dc(100)

    while counter < 10 * animation:
        wait(100)
        counter += 1
        if check_buttons():
            counter = 1000 * animation

    print("end of scorpius")

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

# threading.Thread(target=mailbox).start()

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
