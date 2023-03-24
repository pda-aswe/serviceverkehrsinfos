import paho.mqtt.client as mqtt
import os
import json
import travel

class Messenger:
    def __init__(self):
        self.connected = False

        #TravelService-Object erstellen
        self.travelService = travel.Travel()

        #aufbau der MQTT-Verbindung
        self.mqttConnection = mqtt.Client()
        self.mqttConnection.on_connect = self.__onMQTTconnect
        self.mqttConnection.on_message = self.__onMQTTMessage

        #Definition einer Callback-Funktion für ein spezielles Topic
        self.mqttConnection.message_callback_add("req/rideTime", self.__mailMQTTRideTimecallback)

    def connect(self):
        if not self.connected:
            try:
                docker_container = os.environ.get('DOCKER_CONTAINER', False)
                if docker_container:
                    mqtt_address = "broker"
                else:
                    mqtt_address = "localhost"
                self.mqttConnection.connect(mqtt_address,1883,60)
            except:
                return False
        self.connected = True
        return True
    
    def disconnect(self):
        if self.connected:
            self.connected = False
            self.mqttConnection.disconnect()
        return True

    def __onMQTTconnect(self,client,userdata,flags, rc):
        client.subscribe([("req/rideTime",0)])

    def __onMQTTMessage(self,client, userdata, msg):
        pass

    def __mailMQTTRideTimecallback(self,client, userdata, msg):
        try:
            travelData = json.loads(str(msg.payload.decode("utf-8")))
        except:
            print("Can't decode message")
            return
        
        reqKeys = ['from','to','transportType']

        if not all(key in travelData for key in reqKeys):
            print("not all keys available")
            return

        if travelData['transportType'] in ['car','pedestrian','bicycle']:
            try:
                fromlat = float(travelData['from']['lat'])
                fromlon = float(travelData['from']['lon'])
                tolat = float(travelData['to']['lat'])
                tolon = float(travelData['to']['lon'])
            except:
                print("error converting gps data")

            if -90 <= fromlat <= 90 and -180 <= fromlon <= 180 and -90 <= tolat <= 90 and -180 <= tolon <= 180:
                fromGPS = {"lat":fromlat,"lon":fromlon}
                toGPS = {"lat":tolat,"lon":tolon}
                if travelData['transportType'] == "car":
                    travelTime = self.travelService.travelTimeCar(fromGPS,toGPS)
                elif travelData['transportType'] == "bicycle":
                    travelTime = self.travelService.travelTimeBike(fromGPS,toGPS)
                elif travelData['transportType'] == "pedestrian":
                    travelTime = self.travelService.travelTimePedestrian(fromGPS,toGPS)
        elif travelData['transportType'] == 'public':
            travelTime = self.travelService.travelTimePublic(travelData['from'],travelData['to'])
        else:
            return

        if travelTime != -1:
            travelData["travelTime"] = travelTime
            self.mqttConnection.publish("rideTime",json.dumps(travelData))

    def foreverLoop(self):
        self.mqttConnection.loop_forever()