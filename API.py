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


def get_coords(address):
	address = ' '.join(address.split(", "))
	geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apik" \
					   f"ey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={address}, 1&format=json"
	response = requests.get(geocoder_request)
	if response:
		json_response = response.json()
		toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
		toponym_coodrinates = toponym["Point"]["pos"]
		return tuple(map(float, toponym_coodrinates.split()))
	else:
		return None


def get_address(address):
	address = ' '.join(address.split(", "))
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
