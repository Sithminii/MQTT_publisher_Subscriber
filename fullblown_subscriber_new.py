import paho.mqtt.client as mqtt
import time
import json


# Callback when the client connects to the MQTT broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker\n")
    else:
        print("Connection failed with code {rc}")


# Callback when a message is received from the subscribed topic
def on_message(client, userdata, msg):
    print ("Message received " + "on "+ subscribe_topic + ": ")
    data = str(msg.payload.decode("utf-8"))
    print ("\n",data)
    data_in=json.loads(data)

    # Writing received data to a json file
    if write_file_name:
        try : 
            with open(write_file_name, 'a') as json_file:
                json.dump(data_in, json_file, indent=4)  # The 'indent' parameter adds pretty formatting
        except:
            print("Ivalid file format! Cannot write into the file!")

        
def select_broker():
    try:
        broker_address = broker_list[broker_key]
    except:
        print("Invalid broker key!")
    else:
        return broker_address
    
broker_list = { 1:"broker.mqtt.cool", 2:"test.mosquitto.org", 3:"broker.hivemq.com", 4:"iot.eclipse.org", 5:"localhost"}
print("MQTT brokers :\n")
print (broker_list,"\n")
    
# Create an MQTT client instance
client = mqtt.Client("PythonSub")

# Set the callback functions
client.on_connect = on_connect

# Connect to the MQTT broker
broker_key = int(input("Select the broker key: "))
broker_address = select_broker()
broker_port = 1883
keepalive = 60
qos = 0

client.connect(broker_address, broker_port, keepalive)
client.loop_start()

while True:

    try: 
        subscribe_topic = input ('Subscribe Topic : ')
        write_file_name = input("Write json file : ")
        
        if not subscribe_topic:
            print ("Subscribe topic cannot be empty!")
            continue
        
        while True:
            try:
                # Subscribe loop
                client.subscribe(subscribe_topic)
                client.on_message = on_message
                time.sleep(5)              
            #keyboard interrupt to subscribe a new topic. Press "Ctrl + C"                    
            except KeyboardInterrupt: 
                print ("Subscribe new topic\n")
                break
            
        continue
    
    #Keyboard interrupt to disconnect from MQTT broker
    except KeyboardInterrupt:
        break

# Disconnect from the MQTT broker    
client.loop_stop()
client.disconnect()

print("Disconnected from the MQTT broker")
