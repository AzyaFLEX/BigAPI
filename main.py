import requests


def get_coords(address):
    address = (' ').join(address.split(", "))
    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apik" \
                       f"ey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={address}, 1&format=json"
    response = requests.get(geocoder_request)
    if response:
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym_coodrinates = toponym["Point"]["pos"]
        return list(map(float, toponym_coodrinates.split()))
    else:
        return None


def get_address(address):
    address = (' ').join(address.split(", "))
    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apik" \
                       f"ey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={address}, 1&format=json"
    response = requests.get(geocoder_request)
    if response:
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
        return toponym_address
    else:
        return None