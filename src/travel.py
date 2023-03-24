import requests
import vvspy
import json
import os

class Travel:
    def __init__(self):
        self.baseURL = "https://www.mapquestapi.com/directions/v2/route?key="
        self.apiKey = self.__loadAPIKey()

    def __loadAPIKey(self):
        if os.path.exists('key.txt'):
            with open('key.txt') as f:
                return f.readline().strip('\n')
        else:
            print("api key file missing")
            quit()
    
    def __mapQuestRequest(self,fromGPS,toGPS,transportType):
        if transportType == "car":
            routeType = "fastest"
        elif transportType == "bicycle":
            routeType = "bicycle"
        elif transportType == "pedestrian":
            routeType = "pedestrian"
        else:
            return -1
         
        requestData = {
            "locations":[
                {
                    "latLng":{
                        "lat":fromGPS['lat'],
                        "lng":fromGPS['lon']
                    }
                },
                {
                    "latLng":{
                        "lat":toGPS['lat'],
                        "lng":toGPS['lon']
                    }
                }
            ],
            "options":{
                "routeType":routeType
            }
        }

        response = requests.post(self.baseURL+self.apiKey, json=requestData)
        if response.status_code == 200:
            try:
                travelData = json.loads(response.text)
            except:
                return -1

            if "route" in travelData:
                if "realTime" in travelData["route"]:
                    return travelData["route"]["realTime"]
            
        return -1

    def travelTimeCar(self,fromGPS,toGPS):
        return self.__mapQuestRequest(fromGPS,toGPS,"car")
    
    def travelTimeBike(self,fromGPS,toGPS):
        return self.__mapQuestRequest(fromGPS,toGPS,"bicycle")
    
    def travelTimePedestrian(self,fromGPS,toGPS):
        return self.__mapQuestRequest(fromGPS,toGPS,"pedestrian")

    def travelTimePublic(self,fromStation,toStation):
        trip = vvspy.get_trip(fromStation, toStation)
        return trip.duration