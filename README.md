# CSaN_MQTT
## Mqtt Broker Setup on Raspberry Pi
Install Mosquitto (Open-Source Mqtt Broker)
```
sudo apt install mosquitto mosquitto-clients
```
Set Mosquitto to autostart
```
sudo systemctl enable mosquitto
```
Create config file
```
sudo nano /etc/mosquitto/conf.d/local.conf
```
Add following rows to the config: 1883 is one of the default Mqtt Ports and with allow_anonymous=true we disable authentification when connecting to the broker for simplicity reasons
```
listener 1883
allow_anonymous true
```
Save config and restart mosquitto
```
sudo systemctl restart mosquitto
```
Test Mqtt locally (use to different shells for these two commands)
```
mosquitto_sub -t "#" -v
mosquitto_pub -t "testtopic" -m "testmessage"
```

## Create Mqtt Client on Raspberry/other Machines via Python
For the Mqtt-clients we use the paho mqtt client library for python, which provides all essential functions to setup a mqtt-client within a python script
```
sudo apt-get install python3-paho-mqtt
```
