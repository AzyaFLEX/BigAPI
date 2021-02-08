import requests


def get_map(coord: tuple, scale: float, type_map="sat") -> requests.models.Response.content:
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={coord[0]},{coord[1]}&" \
                  f"spn={scale},20&l={type_map}&geocode=Австралия "
    response = requests.get(map_request)

    if not response:
        return "Http статус:", response.status_code, "(", response.reason, ")"

    return response.content
