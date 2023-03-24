# Verkehrsinformations Service

## Datenstruktur des Topics req/rideTime für Autos, Fahrrad und zu Fuß
```json
{
   "from":{
    "lat" : 0.0,
    "lon" : 0.0
   },
   "to":{
    "lat" : 0.0,
    "lon" : 0.0
   },
   "transportType":"car|pedestrian|bicycle"
}
```
Es darf jeweils nur eine Transportart im Feld `transportType` stehen. Lat und lon müssen richtig definiert sein.

## Datenstruktur des Topics req/rideTime für ÖPNV
```json
{
   "from": "<Stations-ID>",
   "to": "<Stations-ID>",
   "transportType":"public"
}
```

## Datenstruktur des Topics rideTime für Autos, Fahrrad und zu Fuß
```json
{
   "from":{
    "lat" : 0.0,
    "lon" : 0.0
   },
   "to":{
    "lat" : 0.0,
    "lon" : 0.0
   },
   "transportType":"car|pedestrian|bicycle",
   "travelTime": 0
}
```
`travelTime` ist in Sekunden angegeben.

## Datenstruktur des Topics rideTime für ÖPNV
```json
{
   "from": "<Stations-ID>",
   "to": "<Stations-ID>",
   "transportType":"public",
   "travelTime": 0
}
```
`travelTime` ist in Sekunden angegeben.