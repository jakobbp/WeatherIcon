#!/usr/bin/env python

import datetime
import json
from urllib import request
from bottle import route, run, debug, static_file

SETTINGS_FILE_PATH = 'wi_settings.json'
THRESHOLDS_FILE_PATH = 'radiation_thresholds.json'

KEY_PORT = 'port'
KEY_DATA_SOURCE = 'dataSource'
KEY_AVERAGE_SAMPLES = 'averageSamples'
KEY_ERROR_TYPE = 'ERROR'

DATA_VALUE_SEPARATOR = ','
DATA_INDEX_MEASURED_RADIATION = 18
DATA_INDEX_MAX_RADIATION = 22

WEATHER_IMAGE_MAPPING = {
	KEY_ERROR_TYPE:     'img/error.png',
	'OVERCAST':         'img/overcast.png',
	'CLOUDY':           'img/cloudy.png',
	'SUNNY_TO_CLOUDY':  'img/sunny_to_cloudy.png',
	'SUNNY':            'img/sunny.png'
}


@route('/current')
def current_reading():
	single_value = calculate_average_over_n(1)
	print("Current ratio value: {}".format(single_value))
	return static_file(filename=get_image_for_ratio(single_value), root='.')


@route('/average')
def average_reading():
	average_value = calculate_average_over_n(int(get_settings()[KEY_AVERAGE_SAMPLES]))
	print("Average ratio value: {}".format(average_value))
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
	radiation_thresholds = get_radiation_thresholds()
	img_path = WEATHER_IMAGE_MAPPING[KEY_ERROR_TYPE]
	for rt in radiation_thresholds:
		if ratio <= rt[0]:
			img_path = WEATHER_IMAGE_MAPPING[rt[1]]
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


def get_radiation_thresholds():
	with open(THRESHOLDS_FILE_PATH) as thresholds_file:
		threshold_ratios = json.load(thresholds_file)
		radiation_thresholds = [(float(threshold_ratios[tr]), tr) for tr in threshold_ratios]
		radiation_thresholds.append((0.0, KEY_ERROR_TYPE))
		radiation_thresholds.sort(reverse=True)
		return radiation_thresholds


debug(True)
run(host='0.0.0.0', port=get_settings()[KEY_PORT])
