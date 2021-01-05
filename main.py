from database import Database
import paho.mqtt.client as mqtt
import datetime
import time

# Creating Database
filename = "SILD_"+datetime.datetime.now().strftime("%Y%m%d_%H")+".db"
db = Database(filename)

def on_connect(client, userdata, flages,rc):
    print(f"Connected with result code {str(rc)}")
    client.subscribe("/SIDL/temperature")
    client.subscribe("/SIDL/current")
    client.subscribe("/SIDL/rpm")
    client.subscribe("/SIDL/vibration")

def on_message(client, userdata, msg):
    tm = datetime.datetime.now().strftime("%X")
    dt = datetime.datetime.now().strftime("%x")

    if msg.topic=="/SIDL/temperature":
        temperature = float(msg.payload)
        db.sensor_data_handler(msg.topic, (temperature, tm, dt))
        print(f"Temperature: {temperature} at {tm} {dt}")

    if msg.topic=="/SIDL/current":
        current = float(msg.payload)
        db.sensor_data_handler(msg.topic, (current, tm, dt))
        print(f"Current: {current} at {tm} {dt}")

    if msg.topic=="/SIDL/rpm":
        rpm = float(msg.payload)
        db.sensor_data_handler(msg.topic, (rpm, tm, dt))
        print(f"RPM: {rpm} at {tm} {dt}")

    if msg.topic=="/SIDL/vibration":
        vibration = float(msg.payload)
        db.sensor_data_handler(msg.topic, (vibration, tm, dt))
        print(f"Vibration: {vibration} at {tm} {dt}")

    time.sleep(2)
    
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("IP_ADDRESS_OF_RPI", 1883)
client.loop_forever()
