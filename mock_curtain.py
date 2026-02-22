import paho.mqtt.client as mqtt


BROKER = "127.0.0.1"  
PORT = 1883                

MQTT_USER = "mqtt_user"
MQTT_PASS = "mqtt1234"

CMD_TOPIC = "home/curtain/command"
STATE_TOPIC = "home/curtain/state"

state = "CLOSED"


def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker")
    client.subscribe(CMD_TOPIC)
    client.publish(STATE_TOPIC, state, retain=True)

def on_message(client, userdata, msg):
    global state
    command = msg.payload.decode()
    print("Received command:", command)

    if command == "OPEN":
        state = "open"
    elif command == "CLOSE":
        state = "closed"
    elif command == "STOP":
        state = "stopped"

    client.publish(STATE_TOPIC, state, retain=True )
    print("Current state:", state)

client = mqtt.Client()
client.username_pw_set(MQTT_USER, MQTT_PASS)

client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT)
client.loop_forever()
