import time
import urllib2
import json
import sys

import unittest

def get_weather_forecast(city):
	"""
	Return 14 days weather based on city
	parameter: city (string)
	return response data (dict)
	"""
	WEATHER_FEED_URL = 'http://api.openweathermap.org/data/2.5/forecast/daily?q=%s&units=imperial&cnt=14'%city
	response = urllib2.urlopen(WEATHER_FEED_URL)

	if response:
		data = json.load(response)

	if 'cod' in data and data['cod']=='404':
		return "No data found for this city..."

	return trim_data(data)


def trim_data(data):
	"""
	Triming data for response
	parameter: Json data (dict)
	return dict
	"""

	result_data, forecasts = {}, {}
	max_temp, min_temp = [],[]

	result_data['city'] = data['city']['name']

	for data in data['list']:
		max_temp.append(data['temp']['max'])
		min_temp.append(data['temp']['min'])
		if data['weather'][0]['main'] in forecasts:
		    forecasts[str(data['weather'][0]['main'])].append(epos_to_strftime(data['dt']))
		else:
		    forecasts[data['weather'][0]['main']]=[epos_to_strftime(data['dt'])]

	result_data['max'] = max(max_temp)
	result_data['min'] = min(min_temp)
	result_data['forecasts'] = forecasts

	return result_data

def epos_to_strftime(epoch_time):
	"""
	Converting epoch time to string formated date
	parameter

	"""
	return time.strftime('%Y-%m-%d', time.localtime(epoch_time))

def main(argv=None):
	try:
		if argv is None:
			argv = sys.argv
		return get_weather_forecast(argv[1:][0])
	except:
		return "No parameter provided"

class DefaultUnitTesting(unittest.TestCase):
	"""
	Basic unit testing
	"""

	def test_json_response(self):
		self.assertEqual(isinstance(get_weather_forecast('Paris'),dict), True)

	def test_json_response_with_unknown_city(self):
		self.data = get_weather_forecast('Pariasds')
		self.assertEqual(get_weather_forecast('Pariasds'), 'No data found for this city...')



if __name__ == "__main__":
    """
    >>>python2.7 summarise_forecast.py Paris
    {'city': u'Paris', 'min': 69.1, 'forecasts': {u'Clear': ['2015-06-23', '2015-06-24', '2015-06-25', '2015-07-03'], u'Rain': ['2015-06-26', '2015-06-27', '2015-06-28', '2015-06-29', '2015-06-30', '2015-07-01', '2015-07-02', '2015-07-04', '2015-07-05', '2015-07-06']}, 'max': 93.51}

    >>>python2.7 summarise_forecast.py unknowncity
    No data found for this city...

    # This is interesting. API Call has minor bug ?. When I passed 'unknown' as city argument.It returns Emungalan weather data
    >>>python2.7 summarise_forecast.py unknown
    {'city': u'Emungalan', 'min': 52.23, 'forecasts': {u'Clear': ['2015-06-24', '2015-06-25', '2015-06-26', '2015-06-27', '2015-06-28', '2015-06-29', '2015-06-30', '2015-07-01', '2015-07-02', '2015-07-03', '2015-07-04', '2015-07-05', '2015-07-06', '2015-07-07']}, 'max': 87.55}


    >>>python2.7 -m unittest summarise_forecast
    ..
    ----------------------------------------------------------------------
    Ran 2 tests in 0.072s

    OK
    """
    sys.exit(main())
