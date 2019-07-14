#!/usr/bin/env python

import datetime
import json
from urllib import request
from bottle import route, run, debug, static_file

SETTINGS_FILE_PATH = 'wi_settings.json'

KEY_PORT = 'port'
KEY_DATA_SOURCE = 'dataSource'
KEY_AVERAGE_SAMPLES = 'averageSamples'

DATA_VALUE_SEPARATOR = ','
DATA_INDEX_MEASURED_RADIATION = 18
DATA_INDEX_MAX_RADIATION = 22

IMG_TO_RATIO_MAPPING = [
	(0.0, 'img/error.png'),
	(0.5, 'img/overcast.png'),
	(0.7, 'img/cloudy.png'),
	(0.9, 'img/sunny_to_cloudy.png'),
	(2.0, 'img/sunny.png')
]


@route('/current')
def current_reading():
	single_value = calculate_average_over_n(1)
	return static_file(filename=get_image_for_ratio(single_value), root='.')


@route('/average')
def average_reading():
	average_value = calculate_average_over_n(int(get_settings()[KEY_AVERAGE_SAMPLES]))
	return static_file(filename=get_image_for_ratio(average_value), root='.')


def calculate_average_over_n(n):
	data_lines = get_data()
	if len(data_lines) < n:
		n = len(data_lines)
	if n > 0:
		try:
			ratio_sum = 0.0
			for line in data_lines[-n:]:
				ratio_sum += calculate_ratio_from_line(line)
			return ratio_sum/n
		except IOError:
			return 0.0
	else:
		return 0.0


def calculate_ratio_from_line(line):
	values = line.split(DATA_VALUE_SEPARATOR)
	return float(values[DATA_INDEX_MEASURED_RADIATION])/float(values[DATA_INDEX_MAX_RADIATION])


def get_image_for_ratio(ratio):
	IMG_TO_RATIO_MAPPING.sort()
	img_path = IMG_TO_RATIO_MAPPING[0][1]
	for img_mapping in IMG_TO_RATIO_MAPPING:
		if ratio <= img_mapping[0]:
			img_path = img_mapping[1]
	return img_path


def get_data():
	with request.urlopen(get_data_source()) as data:
		return [str(data_line) for data_line in data.readlines()]


def get_data_source():
	ds_template = get_settings()[KEY_DATA_SOURCE]
	current_date = datetime.datetime.now()
	return current_date.strftime(ds_template)


def get_settings():
	with open(SETTINGS_FILE_PATH) as settings_file:
		return json.load(settings_file)


debug(True)
run(host='0.0.0.0', port=get_settings()[KEY_PORT])
