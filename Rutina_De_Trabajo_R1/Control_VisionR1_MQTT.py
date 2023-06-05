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

topic1 = "/banda"
topic2 = "/xyangulo"
topic3 = "/pieza"
topic4 = "/orden"

l = 1


def on_connect(client, userdata, flags, rc):
    print("Connected with Code:" + str(rc))
    # Subscribe Topic
    client.subscribe(topic1)
    client.subscribe(topic4)


def on_message(client, userdata, msg):
    global xya

    if msg.topic == topic1:
        global l
        var1 = msg.payload.decode("utf-8")
        topico = msg.topic
        mensaje = str(var1)
        print(var1)
        if var1 == "1":
            result = subprocess.run(
                ["python", "Sistema_De_VisionR1.py"], capture_output=True, text=True
            )
            xya = str(result.stdout.strip())
            print(xya)
            client.publish(topic2, xya)
            client.publish(topic3, l)
            l = l + 1
            if l == 6:
                exit()
            print(
                "--------------------------------------------------------------------"
            )


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# client.connect("35.232.221.19",port=1883)
client.connect("broker.hivemq.com", port=1883, keepalive=150)

client.loop_start()

while True:
    sleep(1)
