import os
import pprint
import sys
import pygame
import requests
import math

def lonlat_distance(a, b):
    degree_to_meters_factor = 111 * 1000 # 111 километров в метрах
    a_lon, a_lat = a
    b_lon, b_lat = b
    radians_lattitude = math.radians((a_lat + b_lat) / 2.)
    lat_lon_factor = math.cos(radians_lattitude)
    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor
    distance = math.sqrt(dx * dx + dy * dy)
    return int(distance // 1)


search_api_server = "https://search-maps.yandex.ru/v1/"
api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

address_ll = " ".join(sys.argv[1:])
geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
geocode_params = {"geocode": address_ll,
          "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
          "format": "json"
}
answer = requests.get(geocoder_api_server, geocode_params)
answer_json = answer.json()
toponym_coodrinates = ','.join((answer_json["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"].split()))

search_params = {
    "apikey": api_key,
    "text": "аптека",
    "lang": "ru_RU",
    "ll": toponym_coodrinates,
    "type": "biz"
}

response = requests.get(search_api_server, params=search_params)
# Преобразуем ответ в json-объект
json_response = response.json()
#pprint.pprint(json_response)
# Получаем первую найденную организацию.
aptecs = []
for i in range(10):
    organization = json_response["features"][i]
    org_name = organization["properties"]["CompanyMetaData"]["name"]
    # Получаем координаты ответа.
    point = [str(x) for x in organization["geometry"]["coordinates"]]
    org_point = ','.join(point)
    if "круглосуточно" in organization["properties"]["CompanyMetaData"]["Hours"]["text"]:
        color = "pm2gnm"
    elif organization["properties"]["CompanyMetaData"]["Hours"]["text"]:
        color = "pm2dbm"
    else:
        color = "pm2grm"
    aptecs.append(org_point + "," + color)


# Собираем параметры для запроса к StaticMapsAPI:
map_params = {
    "l": "map",
    # добавим точку, чтобы указать найденную аптеку
    "pt": f"{toponym_coodrinates},ya_ru~{'~'.join(aptecs)}"
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
# ... и выполняем запрос
response = requests.get(map_api_server, params=map_params)


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