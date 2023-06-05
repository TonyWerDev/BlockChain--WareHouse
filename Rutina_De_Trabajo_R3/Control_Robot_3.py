##########  Librerias  ##########
import cv2
import numpy as np
from time import sleep
import paho.mqtt.client as mqtt
from wlkata_mirobot import WlkataMirobot
import datetime;
from math import atan, atan2, cos, sin, sqrt, pi, acos
import numpy as np

# ocupado = "0"
orden = "0"

print("connecting...")
arm = WlkataMirobot(portname='COM6')
#arm = WlkataMirobot(portname='COM6')
print("connected... OK")

sleep(1)
print("Starting home routine...")

arm.home()
print("Home routine Done...")

topic1 = "/banda3"         
topic2 = "/xy3"
topic3 = "/pieza3"  
topic4 = "/orden"      
# topic5 = "/espera"   

def on_connect(client, userdata, flags, rc):
    print("Connected with Code:"+str(rc))
    # Subscribe Topic
    client.subscribe(topic2)
    client.subscribe(topic3)
    # client.subscribe(topic5)

def on_message(client, userdata, msg):
    global xya
    global ocupado 
    if msg.topic == topic2:
        var1 =  msg.payload.decode("utf-8")
        topico = msg.topic
        mensaje = str(var1)
        # print("--------------------------------------")
        # print("RECEPCION\t Topic1:",topico,"Msg:",mensaje)
        # print("--------------------------------------\n")
        xya = mensaje
        print(xya)

        
    if msg.topic == topic3:
        var1 =  msg.payload.decode("utf-8")
        topico = msg.topic
        mensaje = str(var1)
        print(var1)
        # print("--------------------------------------")
        # print("RECEPCION\t Topic1:",topico,"Msg:",mensaje)
        # print("--------------------------------------\n")
        if var1 == "1":
            rutina1(xya)
            client.publish(topic4, "1")
            print("publicado 1")
        elif var1 == "2":
            rutina2(xya)
            client.publish(topic4, "2")
            print("publicado 2")
        elif var1 == "3":
            rutina3(xya)
            client.publish(topic4, "3")
        elif var1 == "4":
            rutina4(xya)
            client.publish(topic4, "4")
        elif var1 == "5":
            rutina5(xya)
            client.publish(topic4, "5")
        elif var1 == "6":
            rutina6(xya)
            client.publish(topic4, "6")
        elif var1 == "7":
            rutina7(xya)
            client.publish(topic4, "7")
        elif var1 == "8":
            rutina8(xya)
            client.publish(topic4, "8")





def Banda():
    arm.set_conveyor_posi(450, speed = 2000)
    print("La pieza ha llegado")
    client.publish(topic1, "1")
    print(topic1)

def BandaR(): 
    arm.set_conveyor_posi(0, speed = 2000)
    print("La banda ha llegado")

###IZQ
def rutina1(xya):
    global orden 
    var = xya.split(",")
    x = int(var[0])
    y = int(var[1])
    Rx = 49.7623799+0.010209*(x)-0.5471*(y)
    Ry = 313.362186-0.42388323*(x)
    arm.set_tool_pose(Rx,Ry,50,0,0,190)
    sleep(2)
    arm.go_to_axis(b=-62)
    arm.set_tool_pose(Rx,Ry,38,0,0,190)
    arm.pump_on()
    sleep(3)
    arm.set_tool_pose(Rx,Ry,50,0,0,190)
    sleep(2)
    arm.go_to_axis(80.9,15,33,0,-60,0)
    arm.go_to_axis(47,19,26,0,-63,1)
    arm.go_to_axis(47,28,26,0,-63,1)
    arm.pump_off()
    sleep(1)
    arm.go_to_zero()
    BandaR()
    sleep(2)
    Banda()

def rutina2(xya):
    global orden
    var = xya.split(",")
    x = int(var[0])
    y = int(var[1])
    Rx = 49.7623799+0.010209*(x)-0.5471*(y)
    Ry = 313.362186-0.42388323*(x)
    arm.set_tool_pose(Rx,Ry,50,0,0,190)
    sleep(2)
    arm.go_to_axis(b=-65)
    arm.set_tool_pose(Rx,Ry,38,0,0,190)
    arm.pump_on()
    sleep(2)
    arm.set_tool_pose(Rx,Ry,50,0,0,190)
    sleep(2)
    arm.go_to_axis(83,8,33,0,-61,0)
    arm.go_to_axis(-48,32,14,0,-53,0)
    arm.go_to_axis(-48,36,14,0,-53,0)
    arm.pump_off()
    sleep(2)
    arm.go_to_zero()
    BandaR()
    sleep(2)
    Banda()

###IZQ
def rutina3(xya):
    global orden
    var = xya.split(",")
    x = int(var[0])
    y = int(var[1])
    Rx = 49.7623799+0.010209*(x)-0.5471*(y)
    Ry = 313.362186-0.42388323*(x)
    arm.set_tool_pose(Rx,Ry,50,0,0,190)
    sleep(2)
    arm.go_to_axis(b=-62)
    arm.set_tool_pose(Rx,Ry,38,0,0,190)
    arm.pump_on()
    sleep(2)
    arm.set_tool_pose(Rx,Ry,50,0,0,190)
    sleep(2)
    arm.go_to_axis(83,8,33,0,-61,0)
    arm.go_to_axis(47,19,26,0,-63,1)
    arm.go_to_axis(47,28,26,0,-63,1)
    arm.pump_off()
    sleep(2)
    arm.go_to_zero()
    BandaR()
    sleep(2)
    Banda()

def rutina4(xya):
    global orden
    var = xya.split(",")
    x = int(var[0])
    y = int(var[1])
    Rx = 49.7623799+0.010209*(x)-0.5471*(y)
    Ry = 313.362186-0.42388323*(x)
    arm.set_tool_pose(Rx,Ry,50,0,0,190)
    sleep(2)
    arm.go_to_axis(b=-62)
    arm.set_tool_pose(Rx,Ry,38,0,0,190)
    arm.pump_on()
    sleep(2)
    arm.set_tool_pose(Rx,Ry,50,0,0,190)
    sleep(2)
    arm.go_to_axis(83,8,33,0,-61,0)
    arm.go_to_axis(-48,28,6,0,-53,140)
    arm.go_to_axis(-48,41,6,0,-53,140)
    arm.pump_off()
    sleep(2)
    arm.go_to_zero()
    sleep(160)
    BandaR()
    Banda()

###IZQ
def rutina5(xya):
    global orden
    var = xya.split(",")
    x = int(var[0])
    y = int(var[1])
    Rx = 49.7623799+0.010209*(x)-0.5471*(y)
    Ry = 313.362186-0.42388323*(x)
    arm.set_tool_pose(Rx,Ry,50,0,0,190)
    sleep(2)
    arm.go_to_axis(b=-62)
    arm.set_tool_pose(Rx,Ry,38,0,0,190)
    arm.pump_on()
    sleep(2)
    arm.set_tool_pose(Rx,Ry,50,0,0,190)
    sleep(2)
    arm.go_to_axis(83,8,33,0,-61,0)
    arm.go_to_axis(47,19,26,0,-63,1)
    arm.go_to_axis(47,28,26,0,-63,1)
    arm.pump_off()
    sleep(2)
    arm.go_to_zero()
    BandaR()
    sleep(2)
    Banda()


def rutina6(xya):
    global orden
    var = xya.split(",")
    x = int(var[0])
    y = int(var[1])
    Rx = 49.7623799+0.010209*(x)-0.5471*(y)
    Ry = 313.362186-0.42388323*(x)
    arm.set_tool_pose(Rx,Ry,50,0,0,190)
    sleep(2)
    arm.go_to_axis(b=-62)
    arm.set_tool_pose(Rx,Ry,38,0,0,190)
    arm.pump_on()
    sleep(2)
    arm.set_tool_pose(Rx,Ry,50,0,0,190)
    sleep(2)
    arm.go_to_axis(83,8,33,0,-61,0)
    arm.go_to_axis(-48,32,14,0,-53,145)
    arm.go_to_axis(-48,36,14,0,-53,145)
    arm.pump_off()
    sleep(2)
    arm.go_to_zero()
    BandaR()
    sleep(2)
    Banda()

###IZQ
def rutina7(xya):
    global orden
    var = xya.split(",")
    x = int(var[0])
    y = int(var[1])
    Rx = 49.7623799+0.010209*(x)-0.5471*(y)
    Ry = 313.362186-0.42388323*(x)
    arm.set_tool_pose(Rx,Ry,50,0,0,190)
    sleep(2)
    arm.go_to_axis(b=-62)
    arm.set_tool_pose(Rx,Ry,38,0,0,190)
    arm.pump_on()
    sleep(2)
    arm.set_tool_pose(Rx,Ry,50,0,0,190)
    sleep(2)
    arm.go_to_axis(83,8,33,0,-61,0)
    arm.go_to_axis(49,19,26,0,-63,1)
    arm.go_to_axis(49,28,26,0,-63,1)
    arm.pump_off()
    sleep(2)
    arm.go_to_zero()
    BandaR()
    sleep(2)
    Banda()

def rutina8(xya):
    global orden
    var = xya.split(",")
    x = int(var[0])
    y = int(var[1])
    Rx = 49.7623799+0.010209*(x)-0.5471*(y)
    Ry = 313.362186-0.42388323*(x)
    arm.set_tool_pose(Rx,Ry,50,0,0,190)
    sleep(2)
    arm.go_to_axis(b=-62)
    arm.set_tool_pose(Rx,Ry,38,0,0,190)
    arm.pump_on()
    sleep(2)
    arm.set_tool_pose(Rx,Ry,50,0,0,190)
    sleep(2)
    arm.go_to_axis(83,8,33,0,-61,0)
    arm.go_to_axis(-48,32,14,0,-53,0)
    arm.go_to_axis(-48,36,14,0,-53,0)
    arm.pump_off()
    sleep(2)
    arm.go_to_zero()



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# client.connect("35.232.221.19",port=1883)
client.connect("broker.hivemq.com",port=1883, keepalive=200)

client.loop_start()

ban=input("Ya llegó:")
if ban == "s":
    Banda()
while True:
    sleep(1)
    