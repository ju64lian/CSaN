#lib for mqtt
import paho.mqtt.client as mqtt
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

Trigger_OutputPin = 17
Echo_InputPin = 27

sleeptime = 0.4

GPIO.setup(Trigger_OutputPin, GPIO.OUT)
GPIO.setup(Echo_InputPin, GPIO.IN)
GPIO.output(Trigger_OutputPin, False)

measurement_counter = 0
duration_sum = 0 #take three measurements and divide by 3 for distance calculation

#Override connection Callback
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connection success")
        #subscribe to topic
        #client.subscribe("raspberry/myTopic")
        
        #Publish connection message, parameters: topic, payload, Quality of Service, retain message or not
        #client.publish("raspberry/myTopic2", payload="Raspberry subscribed to raspberry/myTopic!", qos=0, retain=False)
        #print("Published connection message to raspberry/myTopic2")
    else:
        print(f"Connection fail with code {rc}")

try:
    #Create Mqtt Client
    client = mqtt.Client()

    client.on_connect = on_connect
    #client.on_message = on_message

    #Parameters broker address, broker port number, keep-alive intervall
    client.connect("localhost", 1883, 60)

    print("Start sensor test!")

    while True:
        #start measurement with 10us long start signal
        #print("Current sensor signal = ", GPIO.input(Echo_InputPin))
        #print("Send start signal for measurement!")

        GPIO.output(Trigger_OutputPin, True)
        time.sleep(0.00001)
        GPIO.output(Trigger_OutputPin, False)

        #Measure Time of the input signal
        startTime = time.time()
        while GPIO.input(Echo_InputPin) == 0:
            #print("Wait for signal start")
            startTime = time.time()

        while GPIO.input(Echo_InputPin) == 1:
            endTime = time.time()
            #print("Wait for signal end")

        duration = endTime - startTime

        #Calculate distance with speed of sound
        distance = (duration * 34300) / 2

        #Check if distance within sensor bounds
        if distance < 2 or (round(distance) > 300):
            print("Distance not within valid sensor range!")
            measurement_counter = 0
            duration_sum = 0
        else:
            #Format distance for output
            if(measurement_counter >= 3):
                distance = format((duration_sum * 34300)/(2*3), '.2f')
                print("The distance is:",distance, "cm")
                #Publish distance to topic at broker
                client.publish("raspberry/distance", payload=distance, qos=0, retain=False)
                duration_sum = duration
                measurement_counter = 1
            else:
                duration_sum += duration
                measurement_counter += 1

        time.sleep(sleeptime)

except KeyboardInterrupt:
    GPIO.cleanup()



        
        
#def on_message(client, userdata, msg):
#    print(f"{msg.topic} {msg.payload}")

#use this to keep the programm running, stops if disconnect is called or program crashes
#client.loop_forever()

