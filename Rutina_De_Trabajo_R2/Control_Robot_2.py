##########  Librerias  ##########
import cv2
import numpy as np
from time import sleep
import paho.mqtt.client as mqtt
from wlkata_mirobot import WlkataMirobot
import datetime;
from math import atan, atan2, cos, sin, sqrt, pi, acos
import numpy as np
from web3 import Web3
import json

print("connecting...")
arm = WlkataMirobot(portname='COM7')
#arm = WlkataMirobot(portname='COM6')
print("connected... OK")

sleep(1)
print("Starting home routine...")

arm.home()
print("Home routine Done...")

topic1 = "/banda2"         
topic2 = "/xyangulo2"
topic3 = "/pieza2"
topic4 = "/orden"
topico5 = "/espera"

#-----------------------------------------BlockChain----------------------------------------------
def escuchadoreventos(event):
    print(f'Evento recibido:')
    print(event['args'])

# # configuring conection to RCP
# infuraSepolia_url = "https://sepolia.infura.io/v3/60f27b6cdc644574a2d2073e619126fe"
# infuraFuji_url = "https://avalanche-fuji.infura.io/v3/60f27b6cdc644574a2d2073e619126fe"
# alchemy_url = "https://eth-sepolia.g.alchemy.com/v2/8rVd-cW7Bk8qOkX2AmWCmBLDW1JhfYIA"
# w3 = Web3(Web3.HTTPProvider(alchemy_url))

# #load contract as an object
# #info=json.load(open('storage.json'))

# # Adresses configuration after deploying
# caller = '0xE159150671F5eCFA47862A0D39F74FbD6d25B98b'
# private_key = '6dee9f69b52af1e4b566659c553be6bcd995623d58f51140f90b975c9c57f178'
# contract_address = '0xa9612b4ABb94F7290a8A13b6F08e6A901F1cc254'

# # contract instance - llamar al contrato
# contract = w3.eth.contract(address=contract_address, abi=json.load(open('PruebasF2.json')))

# number="5"

# filtro_evento = contract.events.Avance.create_filter(fromBlock='latest')

# def blockchainRetrive():
#     #Retrive order
#     number_saved = contract.functions.retrieve().call()
#     print(f'El orden de las figuras es: {number_saved}')

# def blockchainStore(num):
#     # nonce - Contador de transacciones dentro de un bloque
#     nonce = w3.eth.get_transaction_count(caller)
#     # test network id - llamar el id de la cadena para no confundirnos
#     Chain_id = w3.eth.chain_id

#     number = num
#     # building and signing transaction over Angle data
#     call_function = contract.functions.store(number).build_transaction({"chainId": Chain_id, "from": caller, "nonce": nonce})
#     signed_tx = w3.eth.account.sign_transaction(call_function, private_key=private_key)
#     print("Saving the number")
#     send_tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
#     # Wait for transaction receipt
#     tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)
#     print(tx_receipt)
#     print("Transacion successful")

#     # Current Block number
#     print(w3.eth.block_number)
#     # Print balance
#     balance = w3.eth.get_balance(caller)
#     print(w3.from_wei(balance, "ether"))
# #-------------------------------------------------------------------------------------------------

def on_connect(client, userdata, flags, rc):
    print("Connected with Code:"+str(rc))
    # Subscribe Topic
    client.subscribe(topic2)
    client.subscribe(topic3)
    client.subscribe(topic4)

def on_message(client, userdata, msg):
    global xy
    if msg.topic == topic2:
        var1 =  msg.payload.decode("utf-8")
        topico = msg.topic
        mensaje = str(var1)
        xy = var1

    if msg.topic == topic3:
        var1 =  msg.payload.decode("utf-8")
        topico = msg.topic
        mensaje = str(var1)
        print("Topic3:", var1)
        print(xy)
        if var1 == "1":
            print("Rut1")
            rutinaTCh1(xy)
        elif var1 == "2":
            rutinaTG(xy)
        elif var1 == "3":
            rutinaRom(xy)
        elif var1 == "4":
            rutinaTCh2(xy)
    
    if msg.topic == topic4:
        var1 =  msg.payload.decode("utf-8")
        topico = msg.topic
        mensaje = str(var1)
        print("\nOrden",var1)
        if var1 == "2":
            banda()
        elif var1 == "4":
            bandaTG()
        elif var1 == "6":
            banda()
        elif var1 == "8":
            banda()
                

def rutinaTCh1(xya): ##ya der
    var = xya.split(",")
    print(var)
    x = int(var[0])
    y = int(var[1])
    angle = int(var[2])
    Rx = -48.7833185512689+(0.51933692929887*(x))+(0.018239780117285*(y))
    Ry = -139.006775033623+(0.0388743403689171*(x))+(-0.493735216269548*(y))
    print(Rx, ", ", Ry)
    Rx = Rx-30
    arm.set_tool_pose(Rx,Ry,80,0,0,0)
    arm.go_to_axis(b=-65)
    arm.set_tool_pose(Rx,Ry,70.7,0,0,0)
    arm.pump_on()
    sleep(2)
    arm.p2p_interpolation(z=70.7+50)
    g = 100 - angle
    arm.p2p_interpolation(172.6,146,72.7,0,0,g)
    arm.p2p_interpolation(156.6,146,40.7,0,0,g)
    arm.pump_off()
    arm.p2p_interpolation(z=40.7+40)
    arm.go_to_zero()
    
    bandaR()

def rutinaTCh2(xya):  ##ya der
    var = xya.split(",")
    x = int(var[0])
    y = int(var[1])
    angle = int(var[2])
    Rx = -48.7833185512689+(0.51933692929887*(x))+(0.018239780117285*(y))
    Ry = -139.006775033623+(0.0388743403689171*(x))+(-0.493735216269548*(y))
    print(Rx, ", ", Ry)
    Rx = Rx-32
    arm.set_tool_pose(Rx,Ry,80,0,0,0)
    arm.go_to_axis(b=-65)
    arm.set_tool_pose(Rx,Ry,70.7,0,0,0)
    arm.pump_on()
    sleep(2)
    arm.p2p_interpolation(z=70.7+50)
    g = 97 - angle
    arm.p2p_interpolation(245.6,114,72,2,-5,g)
    arm.p2p_interpolation(245.6,114,52.3,2,-5,g)
    arm.pump_off()
    arm.p2p_interpolation(z=40.7+40)
    arm.go_to_zero()

def rutinaRom(xya):  ##ya punta abajo der
    var = xya.split(",")
    x = int(var[0])
    y = int(var[1])
    angle = int(var[2])
    Rx = -48.7833185512689+(0.51933692929887*(x))+(0.018239780117285*(y))
    Ry = -139.006775033623+(0.0388743403689171*(x))+(-0.493735216269548*(y))
    print(Rx, ", ", Ry)
    Rx = Rx-30
    arm.set_tool_pose(Rx,Ry,80,0,0,0)
    arm.go_to_axis(b=-65)
    arm.set_tool_pose(Rx,Ry,70.7,0,0,0)
    arm.pump_on()
    sleep(2)
    arm.p2p_interpolation(z=70.7+50)
    g = 86 - angle
    arm.p2p_interpolation(233.6,130,72.7,0,0,g)
    arm.p2p_interpolation(231.6,99.5,40.7,0,0,g)
    arm.pump_off()
    arm.p2p_interpolation(z=40.7+40)
    arm.go_to_zero()
    bandaR()

def rutinaTG(xya):
    var = xya.split(",")
    x = int(var[0])
    y = int(var[1])
    angle = int(var[2])
    Rx = -48.7833185512689+(0.51933692929887*(x))+(0.018239780117285*(y))
    Ry = -139.006775033623+(0.0388743403689171*(x))+(-0.493735216269548*(y))
    print(Rx, ", ", Ry)
    Rx = Rx-30
    arm.set_tool_pose(Rx,Ry,80,0,0,0)
    arm.go_to_axis(b=-65)
    arm.set_tool_pose(Rx,Ry,70.7,0,0,0)
    arm.pump_on()
    sleep(2)
    arm.p2p_interpolation(z=70.7+50)
    g = -81 - angle
    arm.p2p_interpolation(210.6,125,72.7,0,0,g)
    arm.p2p_interpolation(187,117,44.7,0,0,g)
    arm.pump_off()
    arm.p2p_interpolation(z=40.7+40)
    arm.go_to_zero()
    bandaR()    

def banda():
    global ocupado
    ocupado = 1
    esp = str(ocupado)
    client.publish(topico5,esp)
    arm.set_conveyor_posi(-490, speed=2000)
    client.publish(topic1, "1")

def bandaTG():
    global ocupado
    ocupado = 1
    esp = str(ocupado)
    client.publish(topico5,esp)
    arm.set_conveyor_posi(-475, speed=2000)
    client.publish(topic1, "1")

def bandaR():
    global ocupado
    arm.set_conveyor_posi(0, speed=2000)
    ocupado = 0
    esp = str(ocupado)
    client.publish(topico5,esp)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

#client.connect("35.232.221.19",port=1883)
client.connect("broker.hivemq.com",port=1883, keepalive=150)

client.loop_start()

while True:
    ban=input("Ya llegó:")
    if ban == "s":
        banda()
    # for event in filtro_evento.get_new_entries():
    #     escuchadoreventos(event)
    # sleep(1)