import paho.mqtt.client as mqtt
import time
import json
import xlrd
import pandas as pd

# Load the Excel data into a Pandas DataFrame and form JSON objects
df = pd.read_excel('Data.xlsx')

json_objects = [] # empty list to store JSOn objects formed from row data

for _, row in df.iterrows():
    
    row_dict = row.to_dict()  # Convert each row to a dictionary        
    json_obj = row_dict  # Convert the dictionary to a JSON object  
    json_objects.append(json_obj)# Append the JSON object to the list

Topics_list=[]

for json_obj in json_objects:  # Print the generated JSON objects
    Topics_list.append(json_obj["Location"]) 
    print(Topics_list)

# Callback when the client connects to the MQTT broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker\n")
    else:
        print("Connection failed with code {rc}")

# Create an MQTT client instance
client = mqtt.Client("PythonPub")

# Set the callback function
client.on_connect = on_connect
broker_list = { 1:"broker.mqtt.cool", 2:"test.mosquitto.org", 3:"broker.hivemq.com", 4:"iot.eclipse.org", 5:"localhost"}
print("MQTT brokers :\n")
print (broker_list,"\n")

broker_key = int(input("Select the broker key: "))

#Selecting MQTT broker
def select_broker():
    try:
        broker_address = broker_list[broker_key]
    except:
        print("Invalid broker key!")
    else:
        return broker_address

broker_address = select_broker()
broker_port = 1883
keepalive = 60
qos = 0

# Connect to the MQTT broker
client.connect(broker_address, broker_port, keepalive)

# Start the MQTT loop to handle network traffic
client.loop_start()

# Publish messages to the respective topics
while True:
    try:
        for topic, message in zip(Topics_list, json_objects):
            json_message = json.dumps(message)  # Convert JSON object to a JSON string
            client.publish(topic, json_message)  # Publish the JSON string
        time.sleep(5)

    except KeyboardInterrupt: #press Ctrl + C
            print ("MQTT publisher stop\n")
            break
    
# Disconnect from the MQTT broker
client.disconnect()
print("Disconnected from the MQTT broker")
