import paho.mqtt.client as mqtt
import time
import json

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



while True:
    try :   
        publish_topic = input("Publish Topic : ")
        
        #handling empty publish topics
        if not publish_topic:
            print ("Publish topic cannot be empty!")
            continue

        else:
            while True:
                try:
                    read_file_name = input("Read json file : ")

                    #Read json file
                    with open(read_file_name) as json_file:
                        sensor_out= json.load(json_file)
                    sensor_in=json.dumps(sensor_out)
                    
                    # Publish loop      
                    client.publish(publish_topic,sensor_in)
                    print(f"Published message '{sensor_in}' to topic '{publish_topic}'\n")
                      
                    # Wait for a moment to simulate some client activity
                    time.sleep(5)

                #key board interrupt "Ctrl + C" to publish a new topic    
                except KeyboardInterrupt: 
                    break

                #handling errors with read file
                except:
                    print("Read file does not exist or invalid format!")
                    print("Please enter a valid readfile")
                    continue

            continue       

    #Key-board interrupt to disconnect from MQTT broker
    except KeyboardInterrupt: 
            break
    
# Disconnect from the MQTT broker
client.loop_stop()
client.disconnect()

print("Disconnected from the MQTT broker")

