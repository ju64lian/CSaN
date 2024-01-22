import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
  if rc == 0:
    print("Connection success!")
    client.subscribe("raspberry/distance")
  else:
    print(f"Connection fail with code {rc}")

def on_message(client, userdata, msg):
  print(f"{msg.topic} {msg.payload.decode('UTF-8')}")

client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

client.connect("10.42.0.1", 1883, 60)

client.loop_forever()