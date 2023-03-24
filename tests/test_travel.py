from src import travel
from unittest.mock import patch, ANY, mock_open

@patch("builtins.open")
@patch("os.path.exists")
@patch.object(travel.Travel, '_Travel__mapQuestRequest')
def test_travelTimePedestrian(mock_mapQuestRequest,mock_exists,mock_open):
    obj = travel.Travel()
    gpsCoord = {"lat":3.0,"lon":4.0}

    obj.travelTimePedestrian(gpsCoord,gpsCoord)
    mock_mapQuestRequest.assert_called_with(gpsCoord,gpsCoord,'pedestrian')


@patch("builtins.open")
@patch("os.path.exists")
@patch.object(travel.Travel, '_Travel__mapQuestRequest')
def test_travelTimeBike(mock_mapQuestRequest,mock_exists,mock_open):
    obj = travel.Travel()
    gpsCoord = {"lat":3.0,"lon":4.0}

    obj.travelTimeBike(gpsCoord,gpsCoord)
    mock_mapQuestRequest.assert_called_with(gpsCoord,gpsCoord,'bicycle')


@patch("builtins.open")
@patch("os.path.exists")
@patch.object(travel.Travel, '_Travel__mapQuestRequest')
def test_travelTimeCar(mock_mapQuestRequest,mock_exists,mock_open):
    obj = travel.Travel()
    gpsCoord = {"lat":3.0,"lon":4.0}

    obj.travelTimeCar(gpsCoord,gpsCoord)
    mock_mapQuestRequest.assert_called_with(gpsCoord,gpsCoord,'car')

@patch("builtins.open")
@patch("os.path.exists")
@patch("vvspy.get_trip")
def test_travelTimePublic(mock_getTrip,mock_exists,mock_open):
    obj = travel.Travel()

    obj.travelTimePublic("start","stop")
    mock_getTrip.assert_called_with("start","stop")


@patch("builtins.open")
@patch("os.path.exists")
@patch("requests.post")
def test_mapQuestRequest(mock_request,mock_exists,mock_open):
    obj = travel.Travel()
    gpsCoord = {"lat":3.0,"lon":4.0}
    requestData = {
            "locations":[
                {
                    "latLng":{
                        "lat":3.0,
                        "lng":4.0
                    }
                },
                {
                    "latLng":{
                        "lat":3.0,
                        "lng":4.0
                    }
                }
            ],
            "options":{
                "routeType":"fastest"
            }
        }

    obj._Travel__mapQuestRequest(gpsCoord,gpsCoord,"car")
    mock_request.assert_called_with(ANY,json=requestData)

@patch('builtins.open', new_callable=mock_open, read_data='test')
@patch("os.path.exists")
def test_loadAPIKey(mock_exists,mock_open):
    obj = travel.Travel()

    string_read = obj._Travel__loadAPIKey()
    assert string_read == "test"