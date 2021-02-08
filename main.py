import requests


def get_map(coord: tuple, scale: float, type_map="map") -> requests.models.Response.content:
    # Parameter type_map may be also "map" and "sat,skl"
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={coord[0]},{coord[1]}&spn={scale},{scale}&l={type_map}"
    response = requests.get(map_request)

    if not response:
        return "Http статус:", response.status_code, "(", response.reason, ")"

    return response.content
