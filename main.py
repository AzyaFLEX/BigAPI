import requests


def get_map(coord: list, scale: float, type_map="map", pt=None) -> requests.models.Response.content:
	"""A function that returns the map in bit form based on the received coordinates"""
	# Parameter type_map may be also "map" and "sat,skl"
	api_server = "http://static-maps.yandex.ru/1.x/"
	map_params = {"ll": ",".join(list(map(str, coord))), "spn": ",".join([str(scale), str(scale)]), "l": type_map}
	if pt:
		map_params["pt"] = ",".join([str(pt[0]), str(pt[1]), "pmwtm1"])
	response = requests.get(api_server, params=map_params)
	return response.content
