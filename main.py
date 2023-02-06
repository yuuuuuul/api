import os
import pprint
import sys
import pygame
import requests


address_ll = " ".join(sys.argv[1:])
geocoder_api_server = f"http://geocode-maps.yandex.ru/1.x/"
geocode_params = {"geocode": address_ll,
          "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
          "format": "json"
}
answer = requests.get(geocoder_api_server, geocode_params)
answer_json = answer.json()
#pprint.pprint(answer_json)
toponym_coodrinates = [float(x) for x in answer_json["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"].split()]
geocoder_api_server = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={str(toponym_coodrinates[0])},{str(toponym_coodrinates[1])}&kind=district&format=json"
dis = requests.get(geocoder_api_server)
dis_json = dis.json()
#pprint.pprint(dis_json)
print(dis_json["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["Address"]["Components"][5]["name"])




