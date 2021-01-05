import paho.mqtt.client as mqtt
from tkinter import *
import datetime
import time

def on_connect(client, userdata, flages,rc):
    print(f"Connected with result code {str(rc)}")
    client.subscribe("/SIDL/temperature")
    client.subscribe("/SIDL/current")
    client.subscribe("/SIDL/rpm")
    client.subscribe("/SIDL/vibration")

def on_message(client, userdata, msg):
    date_label.config(text=datetime.datetime.now().strftime("%d-%b-%Y"))
    time_label.config(text=datetime.datetime.now().strftime("%I:%M:%S %p"))

    if msg.topic=="/SIDL/temperature":
        temperature_label.configure(text = str(float(msg.payload))+" \u2103")

    if msg.topic=="/SIDL/current":
        current_label.configure(text = str(float(msg.payload))+" Amps")

    if msg.topic=="/SIDL/rpm":
        rpm_label.configure(text = str(float(msg.payload))+" RPM")

    if msg.topic=="/SIDL/vibration":
        vibration_label.configure(text = str(float(msg.payload))+" Hz")
    
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("IP_ADDRESS_OF_RPI", 1883)

win = Tk()
win.title("Smart Industrial Data Logger")
win.geometry('320x250')
win.configure(background='#F5F5F5')

# Label Frame
label_frame = LabelFrame(win, text="Readings")
label_frame.grid(row=0, column=0, padx=20, pady=20)

# Temperature
Label(label_frame, text="TEMPERATURE :", height=2, width=12, padx=10).grid(row=0, column=0)
temperature_label = Label(label_frame, height=2, width=15, padx=10)
temperature_label.grid(row=0, column=1)

# Current
Label(label_frame, text="CURRENT :", height=2, width=12, padx=10).grid(row=1, column=0)
current_label = Label(label_frame, height=2, width=15, padx=10)
current_label.grid(row=1, column=1)

# RPM
Label(label_frame, text="RPM :", height=2, width=12, padx=10).grid(row=2, column=0)
rpm_label = Label(label_frame, height=2, width=15, padx=10)
rpm_label.grid(row=2, column=1)

# Vibration
Label(label_frame, text="RPM :", height=2, width=12, padx=10).grid(row=3, column=0)
vibration_label = Label(label_frame, height=2, width=15, padx=10)
vibration_label.grid(row=3, column=1)

# Time
time_label = Label(win)
time_label.grid(row=1, column=0, sticky=W, padx=20)
# Date
date_label = Label(win)
date_label.grid(row=2, column=0, sticky=W, padx=20)

client.loop_start()

win.mainloop()

