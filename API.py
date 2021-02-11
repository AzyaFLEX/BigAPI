import requests


def get_map(coord: tuple, scale: float, type_map="map") -> requests.models.Response.content:
    # Parameter type_map may be also "map" and "sat,skl"
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={coord[0]},{coord[1]}&spn={scale},{scale}&l={type_map}"
    response = requests.get(map_request)
    if not response:
        return "Http статус:", response.status_code, "(", response.reason, ")"
    return response.content


def get_coords(address):
    address = (' ').join(address.split(", "))
    geocoder_request = "http://geocode-maps.yandex.ru/1.x"\
                       f"/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={address}, 1&format=json"
    response = requests.get(geocoder_request)
    if response:
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym_coodrinates = toponym["Point"]["pos"]
        return tuple(map(float, toponym_coodrinates.split()))
    else:
        return None


def get_address(address):
    address = (' ').join(address.split(", "))
    geocoder_request = "http://geocode-maps.yandex.ru/1.x"\
                       f"/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={address}, 1&format=json"
    response = requests.get(geocoder_request)
    if response:
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
        return toponym_address
    else:
        return None


def get_index(address):
    address = (' ').join(address.split(", "))
    geocoder_request = "http://geocode-maps.yandex.ru/1.x" \
                       f"/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={address}, 1&format=json"
    response = requests.get(geocoder_request)
    if response:
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        try:
            postcode = toponym["metaDataProperty"]["GeocoderMetaData"]["Address"]["postal_code"]
        except KeyError:
            postcode = None
        return postcode
    else:
        return None