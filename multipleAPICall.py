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
    # cities = ["PARIS MONTSOURIS","Vélizy"]
    cities = ["07156099999","07147099999","C1292","LFPV","07150099999","07149099999","LFPO","LFPB","D3623","07146099999","07157099999","07145099999","D3543"]
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
    cities = ["07156099999"]
    dict_filter = lambda x, y: dict([(i, x[i]) for i in x if i in set(y)])
    for c in cities:
        get_single_weather_list = get_single_weather( c,key, "metric",
                                                     "datetime,datetimeEpoch,name,address,resolvedAddress,latitude,longitude,temp,humidity,precip,solarradiation,solarenergy,conditions,stations,icon,source",
                                                     "Cobs", "json")
    city_data = json.loads(get_single_weather_list)
    for station in city_data['days'][0]['stations']:
        data = json.loads(get_single_weather(station))
        json_day = data["days"][0]
        # appending the data
        data.update(json_day)
        new_dict_keys = ("latitude", "longitude", "resolvedAddress", "address", "timezone", "tzoffset", "datetime", "datetimeEpoch","temp", "humidity", "precip", "solarradiation", "solarenergy", "conditions", "icon", "source", "stations")
        small_json = dict_filter(data, new_dict_keys)
        # JSON formatted str
        json_formatted_str = json.dumps(small_json, indent = 2)
        data = json.loads(json_formatted_str)
        if small_json["solarradiation"] is None:
            small_json['solarradiation'] = city_data['days'][0]['solarradiation']
        if small_json["solarenergy"] is None:
            small_json['solarenergy'] = city_data['days'][0]['solarenergy']
        json_formatted_str = json.dumps(data, indent = 2)
        print(json_formatted_str)
'''

if __name__ == "__main__":
    main()
