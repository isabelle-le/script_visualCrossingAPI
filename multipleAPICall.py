import requests as req
import urllib
import json


def weather_api_call(requestURL, parameters):
    response = req.get(url=requestURL, params=parameters)
    # print(response.url)
    if response.status_code != 200:
        print(response.json())
        exit()
    data = response.json()
    return json.dumps(data)


def get_single_weather( station="paris", key="QRLSXGZEPLWWUC7JLBEQAVQSE", unit_group="metric",
                       elements="datetime,datetimeEpoch,name,address,resolvedAddress,latitude,longitude,temp,humidity,precip,solarradiation,solarenergy,conditions,icon,stations,source",
                       include="Cobs", content_type="json"):
    """
    :param station
    :param key: api_key QRLSXGZEPLWWUC7JLBEQAVQSE
    :param unit_group: metric °c,km
    :param max_distance(meters): max=200km or 200000m
    :param elements: values
    :param include: obs: station observation, remote: remote observation satellite/radar, fcst: forecast,Cobs: combination
    :param options:useobs,useremote
    :param content_type:json
    :return:weather_api_call
    """
    requestURL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/" + urllib.parse.quote(station) + "/" + urllib.parse.quote("yesterday")
    parameters = {"key": key, "unitGroup": unit_group, "elements": elements, "include": include, "contentType": content_type}
    return weather_api_call(requestURL, parameters)


def main():
    key ="RLNCXT8KTDLMAMYL3P967EEMG" #"QRLSXGZEPLWWUC7JLBEQAVQSE"
    cities = ["PARIS MONTSOURIS","Vélizy"]
    dict_filter = lambda x, y: dict([(i, x[i]) for i in x if i in set(y)])
    for c in cities:
        get_single_weather_list = get_single_weather( c,key, "metric",
                                                     "datetime,datetimeEpoch,name,address,resolvedAddress,latitude,longitude,temp,humidity,precip,solarradiation,solarenergy,conditions,stations,icon,source",
                                                     "Cobs", "json")
        city_data = json.loads(get_single_weather_list)
        # python object to be appended
        json_day = city_data["days"][0]
        # appending the data
        city_data.update(json_day)
        new_dict_keys = ("latitude", "longitude", "resolvedAddress", "address", "timezone", "tzoffset", "datetime", "datetimeEpoch","temp", "humidity", "precip", "solarradiation", "solarenergy", "conditions", "icon", "source", "stations")
        small_json = dict_filter(city_data, new_dict_keys)
        # JSON formatted str
        json_formatted_str = json.dumps(small_json, indent=2)
        print(json_formatted_str)

'''
def main():
    key = "QRLSXGZEPLWWUC7JLBEQAVQSE"
    get_single_weather_list = get_single_weather( "paris",key, "metric",
                                                 "datetime,datetimeEpoch,name,address,resolvedAddress,latitude,longitude,temp,humidity,precip,solarradiation,solarenergy,conditions,stations,icon,source",
                                                 "Cobs", "json")
    paris_data = json.loads(get_single_weather_list)
    # print(json.dumps(paris_data))
    for station in paris_data['days'][0]['stations']:
        data = json.loads(get_single_weather(station))
        json_obj = json.dumps(data["days"][0])
        # python object to be appended
        json_station = data["stations"][station]
        # parsing JSON string
        json_final = json.loads(json_obj)
        # appending the data
        json_final.update(json_station)
        # JSON formatted str
        json_formatted_str = json.dumps(json_final, indent=10)
        station_data = json.loads(json_formatted_str)
        if station_data["solarradiation"] is None:
            station_data['solarradiation'] = paris_data['days'][0]['solarradiation']
        if station_data["solarenergy"] is None:
            station_data['solarenergy'] = paris_data['days'][0]['solarenergy']
        json_formatted_str = json.dumps(station_data, indent=10)
        print(json_formatted_str)
'''

if __name__ == "__main__":
    main()
