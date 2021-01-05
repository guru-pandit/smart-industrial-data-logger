#include <WiFi.h>
#include <PubSubClient.h>


//WiFi Connection variables
const char* ssid = "WIFI_SSID";                   // wifi ssid
const char* password =  "WIFI_PASSWORD";         // wifi password
const char* mqttServer = "IP_ADDRESS_OF_RPI";    // IP address Raspberry Pi
const int mqttPort = 1883;
const char* mqttUser = "";      // if you don't have MQTT Username, no need input
const char* mqttPassword = "";  // if you don't have MQTT Password, no need input

//Temperature sensor variables
const double VCC = 3.3;             // NodeMCU on board 3.3v vcc
const double R2 = 10000;            // 10k ohm series resistor
const double adc_resolution = 1023; // 10-bit adc
const double A = 0.001129148;   // thermistor equation parameters
const double B = 0.000234125;
const double C = 0.0000000876741;


//Current variables
const int sensorIn = A0;
int mVperAmp = 185; // use 185 for 5A, 100 for 20A Module and 66 for 30A Module
double Voltage = 0;
double VRMS = 0;
double AmpsRMS = 0;

//RPM Variables
float value = 0;
float rev = 0;
int rpm;
int oldtime = 0;
int rtime;


//Function Declaration
int temperature_cal();
float current_cal();
int rpm_cal();
long vibration_cal();

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {

  Serial.begin(115200);
  
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi..");
  }
  Serial.println("Connected to the WiFi network");

  client.setServer(mqttServer, mqttPort);
  client.setCallback(callback);

  while (!client.connected()) {
    Serial.println("Connecting to MQTT...");

    if (client.connect("ESP8266Client", mqttUser, mqttPassword )) {

      Serial.println("connected");

    } else {

      Serial.print("failed with state ");
      Serial.print(client.state());
      delay(2000);

    }
  }
  attachInterrupt(14, isr, RISING);
}

void callback(char* topic, byte* payload, unsigned int length) {

  Serial.print("Message arrived in topic: ");
  Serial.println(topic);

  Serial.print("Message:");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }

  Serial.println();
  Serial.println("-----------------------");

}

void loop() {
  if (!client.loop())
    client.connect("ESP8266Client");
  
  char temp[16];//temperature
  char current[16];//current
  char rpm[16];//RPM
  void isr();
  char vibration[16];//Vibration

  dtostrf(temperature_cal(),1,2,temp);

  Voltage = current_cal();
  VRMS = (Voltage/2.0) *0.707; // sq root
  AmpsRMS = (VRMS * 1000)/mVperAmp;
  float Wattage = (220*AmpsRMS)-18;
  dtostrf(AmpsRMS,1,2,current);

  dtostrf(vibration_cal(),10,2,vibration);
  
  dtostrf(rpm_cal(),1,2,rpm);

  client.publish("/SIDL/temperature", temp);
  client.publish("/SIDL/current",current);
  client.publish("/SIDL/rpm",rpm);
  client.publish("/SIDL/vibration",vibration);
  delay(1000);

}


//Temperature Fuction
int temperature_cal(){
  double Vout, Rth, temperature, adc_value; 
  
  adc_value = analogRead(36);
  Vout = (adc_value * VCC) / adc_resolution;
  Rth = (VCC * R2 / Vout) - R2;
  temperature = (1 / (A + (B * log(Rth)) + (C * pow((log(Rth)),3))));   // Temperature in kelvin
  temperature = temperature - 273.15;  // Temperature in degree celsius
  return temperature;
}


//Current Function
float current_cal(){
  float result;

  int readValue; //value read from the sensor
  int maxValue = 0; // store max value here
  int minValue = 1024; // store min value here

  uint32_t start_time = millis();

  while((millis()-start_time) < 1000){
    readValue = analogRead(sensorIn);
    
    if (readValue > maxValue){
      maxValue = readValue;
    }
    if (readValue < minValue){
      minValue = readValue;
    }
  }

  // Subtract min from max
  result = ((maxValue - minValue) * 5)/1024.0;

  return result;
}


//RPM Function
int rpm_cal(){
  delay(100);
  detachInterrupt(14);
  rtime = millis()-oldtime;
  rpm = (rev/rtime)*60000*3;
  oldtime = millis();
  rev = 0;
  attachInterrupt(14, isr, RISING);
  return rpm;
}

void isr(){
  rev++;
}


//Vibration function
long vibration_cal(){
  delay(10);
  long measurement=pulseIn (34, HIGH);  //wait for the pin to get HIGH and returns measurement
  return measurement;
}
