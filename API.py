import requests


def get_map(coord: list, scale: float, type_map="map", pt=[]) -> requests.models.Response.content:
    """A function that returns the map in bit form based on the received coordinates"""
    # Parameter type_map may be also "map" and "sat,skl"
    api_server = "http://static-maps.yandex.ru/1.x/"
    map_params = {"ll": ",".join(list(map(str, coord))), "spn": ",".join([str(scale), str(scale)]), "l": type_map}
    if pt:
        pt = list(map(lambda x: ",".join([str(x[0]), str(x[1]), "flag"]), pt))
        map_params["pt"] = "~".join(pt)
    response = requests.get(api_server, params=map_params)
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


def get_address(address, add_postcode=False):
    address = (' ').join(address.split(", "))
    geocoder_request = "http://geocode-maps.yandex.ru/1.x"\
                       f"/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={address}, 1&format=json"
    response = requests.get(geocoder_request)
    if response:
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
        if add_postcode:
            if get_index(address):
                return toponym_address + ', ' + get_index(address)
            else:
                return toponym_address
        else:
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
            postcode = ''
        return postcode
    else:
        return None


def get_coords_to_address(coords):
    address = ",".join(list(map(str, coords)))
    geocoder_request = "http://geocode-maps.yandex.ru/1.x/?format=json" \
                       f"&apikey=40d1649f-0493-4b70-98ba-98533de7710b" \
                       f"&geocode={address}"
    response = requests.get(geocoder_request)
    if response:
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
        return toponym_address
    else:
        return None


def get_organization(coords):
    geocoder_request = f"https://search-maps.yandex.ru/v1/?text=" \
                       f"{coords}" \
                       f"&type=biz&lang=ru_RU&results=1&apikey=aa432ea9-1ced-493e-be4d-aac30e8ed950"
    response = requests.get(geocoder_request)
    if response:
        json_response = response.json()
        return json_response['features']
