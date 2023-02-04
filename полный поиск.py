import os
import pprint
import sys
import pygame
import requests

def map_make(object):
    toponym_to_find = " ".join(object)
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}
    response = requests.get(geocoder_api_server, params=geocoder_params)
    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    # Координаты центра топонима:
    toponym_x = abs(float(toponym["boundedBy"]["Envelope"]["lowerCorner"].split()[0]) - float(toponym["boundedBy"]["Envelope"]["upperCorner"].split()[0]))
    toponym_y = abs(float(toponym["boundedBy"]["Envelope"]["lowerCorner"].split()[1]) - float(toponym["boundedBy"]["Envelope"]["upperCorner"].split()[1]))
    toponym_coodrinates = toponym["Point"]["pos"]
    # Долгота и широта:
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

    delta = [str(toponym_x), str(toponym_y)]
    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "spn": ",".join(delta),
        "l": "map",
        "pt": f"{','.join(toponym_coodrinates.split())},round"
    }
    return map_params

map_params = map_make(sys.argv[1:])
map_request = "http://static-maps.yandex.ru/1.x/"
# ... и выполняем запрос
response = requests.get(map_request, params=map_params)


if not response:
    print("Ошибка выполнения запроса:")
    print("Http статус:", response.status_code, "(", response.reason, ")")
    sys.exit(1)
map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)
pygame.init()
screen = pygame.display.set_mode((600, 450))
screen.blit(pygame.image.load(map_file), (0, 0))
pygame.display.flip()
while pygame.event.wait().type != pygame.QUIT:
    pass
pygame.quit()
os.remove(map_file)