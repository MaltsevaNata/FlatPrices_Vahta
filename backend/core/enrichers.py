import json
import requests

from models import RealEstate
from core import config


def enrich_data(data: RealEstate):
    address = data.address
    lat, lon = _get_coordinates(address)
    data.lat = lat
    data.lon = lon
    aqi, concentrations = _get_air_quality(lat, lon)
    data.AQI = aqi
    data.air_pollutant_concentration = concentrations
    return data


def _get_coordinates(address: str):
    token = config.DADATA_TOKEN
    print(token)
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
    return lat, lon


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