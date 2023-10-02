# MQTT_publisher_Subscriber
Developed a MQTT publisher and subscriber using python

## 01. Fullblown Publisher and Subscriber
Here, first I have implemented a publisher which reads a JSON file and publishes the content via MQTT. By giving a key-board interrupt (Ctrl + C), we can publish to a new topic. Next I have implemented a subscriber which allows to subscribe a topic and receive JSON objects via MQTT broker. Subscriber is allowed to subscribe new topics by giving key-board interrupts. The receiving JSON object content is displayed as well as written into a .json file specified by the subcriber.

## 02. Read Excel file and publish via MQTT
The previous publisher code is modified to read an Excel file (.xlsx), extract rows of data and create different JSON objects from each row and finally publish them to separate topics.
