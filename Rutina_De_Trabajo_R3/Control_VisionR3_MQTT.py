##########  Librerias  ##########
import cv2
import numpy as np
from time import sleep
import paho.mqtt.client as mqtt
from wlkata_mirobot import WlkataMirobot
import datetime
from math import atan, atan2, cos, sin, sqrt, pi, acos
import numpy as np
import subprocess

l = 1
# cap = cv2.VideoCapture('rtsp://admin:Camera01_@10.50.70.178:554')
cap = cv2.VideoCapture("rtsp://admin:Camera02_@10.50.70.75:554")
# cap = cv2.VideoCapture('rtsp://admin:Camera03_@10.50.70.11:554') #--
# cap = cv2.VideoCapture('rtsp://admin:Camera04_@10.50.70.89:554')
# cap = cv2.VideoCapture('rtsp://admin:Camera05_@10.50.70.68:554')

font = cv2.FONT_HERSHEY_SIMPLEX

topic1 = "/banda3"
topic2 = "/xy3"
topic3 = "/pieza3"
topic4 = "/orden"


def on_connect(client, userdata, flags, rc):
    print("Connected with Code:" + str(rc))
    # Subscribe Topic
    client.subscribe(topic1)


def on_message(client, userdata, msg):
    if msg.topic == topic1:
        global l
        var1 = msg.payload.decode("utf-8")
        topico = msg.topic
        mensaje = str(var1)
        print(var1)
        # print("--------------------------------------")
        # print("RECEPCION\t Topic1:",topico,"Msg:",mensaje)
        # print("--------------------------------------\n")
        if var1 == "1":
            result = subprocess.run(
                ["python", "Sistema_De_VisionR3.py"], capture_output=True, text=True
            )
            xya = str(result.stdout.strip())
            print(xya)
            client.publish(topic2, xya)
            client.publish(topic3, l)
            l = l + 1
            if l == 10:
                exit()
            print(
                "--------------------------------------------------------------------"
            )


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# client.connect("35.232.221.19",port=1883)
client.connect("broker.hivemq.com", port=1883, keepalive=100)

client.loop_start()

while True:
    sleep(1)
