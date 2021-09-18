import eventlet
eventlet.monkey_patch()

import requests
from geopy.distance import geodesic

import json
import math

from models import RealEstate
from core import config


def enrich_data(data: RealEstate):
    address = f"{data.region}, {data.address}"
    lat, lon = _get_coordinates(address)
    data.lat = lat
    data.lon = lon
    aqi, concentrations = _get_air_quality(lat, lon)
    data.AQI = aqi
    data.air_pollutant_concentration = concentrations
    city_center_coordinates = {"Moscow": [55.7522, 37.6156], "SaintPetersburg": [59.9375, 30.3086]}
    city_center = city_center_coordinates[data.region]
    azimuth = _get_azimuth(lat, lon, city_center)
    data.azimuth = azimuth
    center_distance = _get_distance(lat, lon, city_center)
    data.distance = center_distance
    print(data)
    return data


def _get_coordinates(address: str):
    token = config.DADATA_TOKEN
    response = requests.post(config.DADATA_URL,
                             data=json.dumps({'query': address}),
                             headers={'Content-Type': 'application/json',
                                                       'Accept': 'application/json',
                                                       'Authorization': f"Token {token}"})
    assert response.status_code == 200
    response_json = json.loads(response.text)
    address_data = response_json["suggestions"][0]["data"]
    lat = address_data["geo_lat"]
    lon = address_data["geo_lon"]
    print(f"LAT: {lat}, LON: {lon}")
    return float(lat), float(lon)


def _get_air_quality(lat: float, lon: float):
    api_url = f"{config.OWM_URL}air_pollution?lat={lat}&lon={lon}&appid={config.OWM_TOKEN}"
    response = requests.get(api_url)
    assert response.status_code == 200
    response_json = json.loads(response.text)
    air_data = response_json["list"][0]
    aqi = air_data["main"]["aqi"]
    concentrations = air_data["components"]
    print(f"AQI: {aqi} concentr: {concentrations}")
    return aqi, concentrations


def _get_azimuth(lat, lng, city_center):
    llat1 = city_center[0]
    llong1 = city_center[1]
    llat2 = lat
    llong2 = lng

    lat1 = llat1 * math.pi / 180
    lat2 = llat2 * math.pi / 180
    long1 = llong1 * math.pi / 180
    long2 = llong2 * math.pi / 180

    cl1 = math.cos(lat1)
    cl2 = math.cos(lat2)
    sl1 = math.sin(lat1)
    sl2 = math.sin(lat2)
    delta = long2 - long1
    cdelta = math.cos(delta)
    sdelta = math.sin(delta)

    y = math.sqrt(math.pow(cl2 * sdelta, 2) + math.pow(cl1 * sl2 - sl1 * cl2 * cdelta, 2))
    x = sl1 * sl2 + cl1 * cl2 * cdelta
    ad = math.atan2(y, x)

    x = (cl1 * sl2) - (sl1 * cl2 * cdelta)
    y = sdelta * cl2
    z = math.degrees(math.atan(-y / x))

    if (x < 0):
        z = z + 180.

    z2 = (z + 180.) % 360. - 180.
    z2 = - math.radians(z2)
    anglerad2 = z2 - ((2 * math.pi) * math.floor((z2 / (2 * math.pi))))
    angledeg = (anglerad2 * 180.) / math.pi

    return round(angledeg, 2)


def _get_distance(lat, lon, city_center):
    distance = geodesic(city_center, [lat, lon]).meters
    return distance