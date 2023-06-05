##########  Librerias  ##########
import cv2
import numpy as np
from time import sleep
import paho.mqtt.client as mqtt
from wlkata_mirobot import WlkataMirobot
import datetime
from math import atan, atan2, cos, sin, sqrt, pi, acos
import numpy as np
from web3 import Web3
import json

##########  Conexión a WLKATA R2  ##########
print("connecting...")
arm = WlkataMirobot(portname="COM6")
print("connected... OK")

sleep(1)
print("Starting home routine...")

# Iniciar función Home
arm.home()
print("Home routine Done...")

# Definición de Topicos MQTT
topic1 = "/banda"
topic2 = "/xyangulo"
topic3 = "/pieza"
topic4 = "/orden"  # Topico Global
topico5 = "/espera"


# -----------------------------------------BlockChain----------------------------------------------
def escuchadoreventos(event):
    print(f"Evento recibido:")
    print(event["args"])


# Configuración de Conexión a Api (Alchemy)
alchemy_url = "https://eth-sepolia.g.alchemy.com/v2/8rVd-cW7Bk8qOkX2AmWCmBLDW1JhfYIA"
w3 = Web3(Web3.HTTPProvider(alchemy_url))

# Configuración de la Dirección Después del Despliegue
caller = "0xE159150671F5eCFA47862A0D39F74FbD6d25B98b"
private_key = "6dee9f69b52af1e4b566659c553be6bcd995623d58f51140f90b975c9c57f178"
contract_address = "0x8B35ad4Cd5Bd4d174fcBEB48486dAa14b73c1859"

# Referencia al Smart-Contract Desplegado con su ABI
contract = w3.eth.contract(
    address=contract_address, abi=json.load(open("PruebasF2.json"))
)

number = "0"  # Contador de eventos

filtro_evento = contract.events.Avance.create_filter(fromBlock="latest")


# Función de Recuperación de Orden
def blockchainRetrive():
    # Orden de recuperación
    number_saved = contract.functions.retrieve().call()
    print(f"El orden de las figuras es: {number_saved}")


# Función Para Almacenar en el Bloque
def blockchainStore(num):
    # nonce - Contador de transacciones dentro de un bloque
    nonce = w3.eth.get_transaction_count(caller)
    # test network id - llamar el id de la cadena para no confundirnos
    Chain_id = w3.eth.chain_id

    number = num
    # Construcción y Firma de Transacciones Sobre Datos de Angulo
    call_function = contract.functions.store(number).build_transaction(
        {"chainId": Chain_id, "from": caller, "nonce": nonce}
    )
    signed_tx = w3.eth.account.sign_transaction(call_function, private_key=private_key)
    print("Saving the number")
    send_tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    # Espera a que una Transacción se Reciba
    tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)
    print(tx_receipt)
    print("Transacion successful")

    # Número de Bloque actual
    print(w3.eth.block_number)

    # Print balance
    balance = w3.eth.get_balance(caller)
    print(w3.from_wei(balance, "ether"))


# -------------------------------------------------------------------------------------------------


# Función de Conexión
def on_connect(client, userdata, flags, rc):
    print("\nConnected with Code:" + str(rc))
    # Subscripción de Topico
    client.subscribe(topic2)
    client.subscribe(topic3)
    client.subscribe(topic4)  # Recibe de R3


# Función callback que se ejecuta cada que llega un mensaje
def on_message(client, userdata, msg):
    global xy  # Variable Para Almacenar (Posición y θ DM por T2)
    global ord
    if msg.topic == topic2:
        var1 = msg.payload.decode("utf-8")
        topico = msg.topic
        mensaje = str(var1)
        xy = var1

    # Selecciona la Rutina Según él No. pieza Interno
    if msg.topic == topic3:
        var1 = msg.payload.decode("utf-8")
        topico = msg.topic
        mensaje = str(var1)
        print("\nTopic3:", var1)
        print("\n", xy)
        if var1 == "1":
            print("\nRut1")
            rutinaTCh1(xy)
        elif var1 == "2":
            rutinaTCh2(xy)
        elif var1 == "3":
            rutinaTM(xy)
        elif var1 == "4":
            rutinaTG(xy)

    # Selecciona el Desplazamiento del Conveyor Según él No. Pieza Global
    if msg.topic == topic4:
        var1 = msg.payload.decode("utf-8")
        topico = msg.topic
        mensaje = str(var1)
        print("\nOrden", var1)
        ord = var1
        if var1 == "1":
            banda()
        elif var1 == "3":
            banda()
        elif var1 == "5":
            banda()
        elif var1 == "7":
            banda()


# Función para Desplegar Rutina de Triángulo Chico (No.1 - Global)
def rutinaTCh1(xya):
    # Separación del Método, en Tres Variables
    var = xya.split(",")
    print(var)
    x = int(var[0])
    y = int(var[1])
    angle = int(var[2])

    # Obtención de las Coordenadas del Centroide a Través de la Ecuación Resultante de una Regresión
    Rx = 162.019578391673 - (0.35830374801714 * (x)) + (0.0572896852842483 * (y))
    Ry = 129.525982656154 + (0.171996825300382 * (x)) + (0.229303180306981 * (y))
    Rz = 110.368838411743 + (0.0433762583113927 * (x)) - (0.198010720878643 * (y))

    # Inicio de Rutina de Triángulo Chico (No.1 - Global) - #Coordenada Final
    arm.p2p_interpolation(Rx, Ry, Rz + 20, 20, 0, 0)
    arm.go_to_axis(b=-58)
    arm.p2p_interpolation(z=Rz + 2)
    arm.pump_on()
    sleep(2)
    arm.p2p_interpolation(z=Rz + 80)
    g = 135 - angle
    arm.p2p_interpolation(199, -113.5, 72, 0, -10, g)
    arm.p2p_interpolation(192.6, -113, 45.7, 0, -10, g)
    arm.pump_off()
    arm.go_to_zero()


# Función Para Desplegar Rutina de Triángulo Chico (No.3 - Global)
def rutinaTCh2(xya):
    # Separación del Método, en Tres Variables
    var = xya.split(",")
    x = int(var[0])
    y = int(var[1])
    angle = int(var[2])

    # Obtención de las Coordenadas del Centroide a Través de la Ecuación Resultante de una Regresión
    Rx = 162.019578391673 - (0.35830374801714 * (x)) + (0.0572896852842483 * (y))
    Ry = 129.525982656154 + (0.171996825300382 * (x)) + (0.229303180306981 * (y))
    Rz = 110.368838411743 + (0.0433762583113927 * (x)) - (0.198010720878643 * (y))

    # Inicio de Rutina de Triángulo Chico (No.3 - Global) - #Coordenada Final
    arm.p2p_interpolation(Rx, Ry, Rz + 20, 20, 0, 0)
    arm.go_to_axis(b=-58)
    arm.p2p_interpolation(z=Rz + 2)
    arm.pump_on()
    sleep(2)
    arm.p2p_interpolation(z=Rz + 50)
    g = 50 - angle
    arm.p2p_interpolation(218.6, -85, 60.7, 0, -10, g)
    arm.p2p_interpolation(214.6, -85, 41.7, 0, -10, g)
    arm.pump_off()
    arm.go_to_zero()
    bandaR()


# Función Para Desplegar Rutina de Triángulo Mediano (No.5 - Global)
def rutinaTM(xya):
    # Separación del Método, en Tres Variables
    var = xya.split(",")
    x = int(var[0])
    y = int(var[1])
    angle = int(var[2])

    # Obtención de las Coordenadas del Centroide a Través de la Ecuación Resultante de una Regresión
    Rx = 162.019578391673 - (0.35830374801714 * (x)) + (0.0572896852842483 * (y))
    Ry = 129.525982656154 + (0.171996825300382 * (x)) + (0.229303180306981 * (y))
    Rz = 110.368838411743 + (0.0433762583113927 * (x)) - (0.198010720878643 * (y))

    # Inicio de Rutina de Triángulo Mediano (No.5 - Global) - #Coordenada Final
    arm.p2p_interpolation(Rx, Ry, Rz + 20, 20, 0, 0)
    arm.go_to_axis(b=-58)
    arm.p2p_interpolation(z=Rz + 2)
    arm.pump_on()
    sleep(2)
    arm.p2p_interpolation(z=Rz + 50)
    g = 85 - angle
    arm.p2p_interpolation(223.6, -65, 72.7, 0, -10, g)
    arm.p2p_interpolation(218.6, -61.5, 43.7, 0, -10, g)
    arm.pump_off()
    arm.go_to_zero()


# Función Para Desplegar Rutina de Triángulo Grande (No.7 - Global)
def rutinaTG(xya):
    # Separación del Método, en Tres Variables
    var = xya.split(",")
    x = int(var[0])
    y = int(var[1])
    angle = int(var[2])

    # Obtención de las Coordenadas del Centroide a Través de la Ecuación Resultante de una Regresión
    Rx = 162.019578391673 - (0.35830374801714 * (x)) + (0.0572896852842483 * (y))
    Ry = 129.525982656154 + (0.171996825300382 * (x)) + (0.229303180306981 * (y))
    Rz = 110.368838411743 + (0.0433762583113927 * (x)) - (0.198010720878643 * (y))

    # Inicio de Rutina de Triángulo Grande (No.7 - Global) - #Coordenada Final
    arm.p2p_interpolation(Rx, Ry, Rz + 20, 20, 0, 0)
    arm.go_to_axis(b=-58)
    arm.p2p_interpolation(z=Rz + 2)
    arm.pump_on()
    sleep(2)
    arm.p2p_interpolation(z=Rz + 70)
    g = 137 - angle
    arm.p2p_interpolation(239.6, -76, 50, 0, 0, g)
    arm.p2p_interpolation(234.6, -65, 20.7, 0, 0, g)
    arm.pump_off()
    arm.go_to_zero()

    exit()


# Función Para Mover el Conveyor
def banda():
    global ocupado
    ocupado = 1
    esp = str(ocupado)
    if esp == "1":
        print("Espera", esp)
    client.publish(topico5, esp)
    arm.set_conveyor_posi(-490, speed=2000, is_relative=True)
    client.publish(topic1, "1")  # Al terminar el movimiento publicar en T1


# Función Para Evitar el Movimiento de la Banda Si Aun Hay Una Pieza
def bandaTG():
    global ocupado
    ocupado = 1
    esp = str(ocupado)
    if esp == "1":
        print("Espera", esp)
    client.publish(topico5, esp)
    arm.set_conveyor_posi(-490, speed=2000, is_relative=True)
    client.publish(topic1, "1")


# Función Para Regresar el Conveyor a la Posición 0
def bandaR():
    global ocupado
    arm.set_conveyor_posi(0, speed=2000)
    ocupado = 0
    esp = str(ocupado)
    if esp == "0":
        print("Espera", esp)
    client.publish(topico5, esp)


# Creación de una instancia del cliente MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# client.connect("35.232.221.19",port=1883)
client.connect("broker.hivemq.com", port=1883, keepalive=150)

# Inicio del bucle de eventos del cliente MQTT
client.loop_start()

while True:
    ban = input("Ya llegó:")
    if ban == "s":
        banda()
    client.publish(topic1, "1")
    for event in filtro_evento.get_new_entries():
        escuchadoreventos(event)
    sleep(1)
