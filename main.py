import requests


def get_map(coord: list, scale: float, type_map="map") -> requests.models.Response.content:
	# Parameter type_map may be also "map" and "sat,skl"
	api_server = "http://static-maps.yandex.ru/1.x/"
	map_params = {"ll": ",".join(list(map(str, coord))),
		      "spn": ",".join([str(scale), str(scale)]),
		      "l": type_map
	}
	response = requests.get(api_server, params=map_params)
	return response.content
