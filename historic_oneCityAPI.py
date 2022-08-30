'''
Author : Isabelle LE
collect historicque data of one ville
'''
import requests as req
import urllib
import json


def weather_api_call(requestURL, parameters):
    '''
    API call with requestURL and parameters
    :param requestURL: from get-single_weather
    :param parameters:
    :return:
    '''
    response = req.get(url=requestURL, params=parameters)
    print(response.url)
    if response.status_code != 200:
        print(response.json())
        exit()
    data = response.json()
    return json.dumps(data)


def get_single_weather(city="Paris",dateBegin="2022-08-28", dateEnd="2022-08-30", key="QRLSXGZEPLWWUC7JLBEQAVQSE", unit_group="metric",
                       elements="datetime,datetimeEpoch,name,address,resolvedAddress,latitude,longitude,temp,humidity,precip,solarradiation,solarenergy,conditions,icon,stations,source",
                       include="days%2Cobs", content_type="json"):
    """
    build single API url with below params
    :param city : str
    :param dateBegin : YYYY-MM-DD
    :param dateEnd : YYYY-MM-DD
    :param key: api_key QRLSXGZEPLWWUC7JLBEQAVQSE
    :param unit_group: metric °c,km
    :param max_distance(meters): max=200km or 200000m
    :param elements: values
    :param include: 4 options obs: station observation, remote: remote observation satellite/radar, fcst: forecast,Cobs: combination
    :param content_type:json
    :return:weather_api_call
    """
    requestURL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/" + urllib.parse.quote(city) + "/" + urllib.parse.quote(dateBegin) + "/" + urllib.parse.quote(dateEnd)
    parameters = {"key": key, "unitGroup": unit_group, "elements": elements, "include": include, "contentType": content_type}
    return weather_api_call(requestURL, parameters)


def main():
    key = "QRLSXGZEPLWWUC7JLBEQAVQSE"
    cities = ["paris"]
    for c in cities:
        get_single_weather_list = get_single_weather(c,"2022-08-28","2022-08-30",key, "metric",
                                                 "datetime,datetimeEpoch,name,address,resolvedAddress,latitude,longitude,temp,humidity,precip,solarradiation,solarenergy,conditions,stations,icon,source",
                                                 "days%2Cobs", "json")
        city_data = json.loads(get_single_weather_list)
        for station in city_data['days'][0]['stations']:
            data = json.loads(get_single_weather(station))
            json_station = data["stations"][station]
            for days in data["days"]:
                json_obj = days
                json_obj.update(json_station)
                json_formatted_str = json.dumps(json_obj, indent=10)
                station_data = json.loads(json_formatted_str)
                if station_data["solarradiation"] is None:
                    station_data['solarradiation'] = city_data['days'][0]['solarradiation']
                if station_data["solarenergy"] is None:
                    station_data['solarenergy'] = city_data['days'][0]['solarenergy']
                json_formatted_str = json.dumps(station_data, indent=10)
                print(json_formatted_str)

if __name__ == "__main__":
    main()
