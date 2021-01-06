## About Project

A data logger or a data acquisition system is an electronic device common in measurement application. The basic form of data logger is to capture and store the environment parameters over a period of time with incorporating sensors. This stand alone device measure, collect and store data on the Memory device. Raspberry-pi is used in this system to perform the job. The system is equipped with several sensors such as temperature, vibration, speed and current. The Raspberry-Pi system is used as a server to record and display data from several sensors and the measurements are transmitted via Wi-Fi to server. To work system properly without internet the both Raspberry Pi and Node MCU should be connected to the same network.

---

### Sensors

We have used the four sensors i.e. IR sensor, Current Sensor, Temperature Sensor and vibration Sensor

### Node MCU

Node MCU is Wi-Fi enabled Arduino like hardware IO. that can be code like Arduino. In this project we have used ESP32 version of Node MCU.
All the sensors are Connected to the Node MCU. It collects the data and then transmit the data towards the Raspberry Pi Server over Wi-Fi using MQTT Protocol.

The code in Sensor folder is burned into the Node MCU this entire code contains the codes to Connect the WIFI and transmit data towards the Raspberry Pi

**Sensors.ino**

```c++
const  char* ssid =  "WIFI_SSID"; // wifi ssid

const  char* password =  "WIFI_PASSWORD"; // wifi password

const  char* mqttServer =  "IP_ADDRESS_OF_RPI";
```

Replace the above with your Wi-Fi SSID, Wi-Fi Password and IP address of MQTT Server

### Raspberry Pi

Raspberry Pi is small and affordable computer that can be used to learn programming through fun and practical projects.
Here we used the python programs to read and store the data into DB.
we used Tkinter Python library to create GUI to display data.
other libraries are db-sqlite3 and paho-mqtt

**main.py**

```python
client.connect("IP_ADDRESS_OF_RPI", 1883)
```

**gui.py**

```python
client.connect("IP_ADDRESS_OF_RPI", 1883)
```

Replace with Your Raspberry Pi IP address
