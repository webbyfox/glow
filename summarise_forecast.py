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

	#data = {"cod":"200","message":0.1016,"city":{"id":6058560,"name":"London","coord":{"lon":-81.23304,"lat":42.983391},"country":"CA","population":0,"sys":{"population":0}},"cnt":14,"list":[{"dt":1434992400,"temp":{"day":80.08,"min":63.61,"max":80.08,"night":71.1,"eve":76.19,"morn":63.61},"pressure":991.3,"humidity":75,"weather":[{"id":501,"main":"Rain","description":"moderate rain","icon":"10d"}],"speed":10.07,"deg":242,"clouds":12,"rain":10.78},{"dt":1435078800,"temp":{"day":68.54,"min":51.66,"max":70.79,"night":51.66,"eve":66.51,"morn":70.79},"pressure":989.53,"humidity":86,"weather":[{"id":500,"main":"Rain","description":"light rain","icon":"10d"}],"speed":20.87,"deg":303,"clouds":12,"rain":0.81},{"dt":1435165200,"temp":{"day":71.55,"min":57.61,"max":71.55,"night":57.61,"eve":69.6,"morn":58.93},"pressure":1004.77,"humidity":0,"weather":[{"id":500,"main":"Rain","description":"light rain","icon":"10d"}],"speed":1.19,"deg":202,"clouds":57,"rain":0.55},{"dt":1435251600,"temp":{"day":72.16,"min":63.48,"max":72.16,"night":64.96,"eve":66.87,"morn":63.48},"pressure":1000.08,"humidity":0,"weather":[{"id":501,"main":"Rain","description":"moderate rain","icon":"10d"}],"speed":13.78,"deg":120,"clouds":74,"rain":4.21},{"dt":1435338000,"temp":{"day":72.79,"min":62.94,"max":72.79,"night":62.94,"eve":71.8,"morn":70.83},"pressure":991.68,"humidity":0,"weather":[{"id":501,"main":"Rain","description":"moderate rain","icon":"10d"}],"speed":13.13,"deg":286,"clouds":24,"rain":4.06},{"dt":1435424400,"temp":{"day":74.25,"min":60.67,"max":74.25,"night":60.67,"eve":73,"morn":64.27},"pressure":993.55,"humidity":0,"weather":[{"id":500,"main":"Rain","description":"light rain","icon":"10d"}],"speed":9.03,"deg":285,"clouds":5,"rain":0.58},{"dt":1435510800,"temp":{"day":67.5,"min":62.87,"max":68.86,"night":62.87,"eve":68.86,"morn":63.5},"pressure":993.33,"humidity":0,"weather":[{"id":501,"main":"Rain","description":"moderate rain","icon":"10d"}],"speed":9.98,"deg":84,"clouds":99,"rain":10.61},{"dt":1435597200,"temp":{"day":68.54,"min":62.15,"max":68.54,"night":62.15,"eve":63.32,"morn":64.18},"pressure":992.26,"humidity":0,"weather":[{"id":501,"main":"Rain","description":"moderate rain","icon":"10d"}],"speed":17.97,"deg":78,"clouds":90,"rain":7.46},{"dt":1435683600,"temp":{"day":63.54,"min":57.45,"max":63.54,"night":57.45,"eve":62.64,"morn":62.64},"pressure":993.63,"humidity":0,"weather":[{"id":502,"main":"Rain","description":"heavy intensity rain","icon":"10d"}],"speed":13.87,"deg":36,"clouds":83,"rain":24.41},{"dt":1435770000,"temp":{"day":75.56,"min":61.29,"max":75.56,"night":64.58,"eve":72.97,"morn":61.29},"pressure":999.64,"humidity":0,"weather":[{"id":500,"main":"Rain","description":"light rain","icon":"10d"}],"speed":12.81,"deg":272,"clouds":5,"rain":0.24},{"dt":1435856400,"temp":{"day":77.83,"min":67.12,"max":77.83,"night":71.76,"eve":77.72,"morn":67.12},"pressure":996.75,"humidity":0,"weather":[{"id":500,"main":"Rain","description":"light rain","icon":"10d"}],"speed":12.16,"deg":253,"clouds":15,"rain":1.28},{"dt":1435942800,"temp":{"day":84.09,"min":73.13,"max":84.09,"night":73.47,"eve":81.55,"morn":73.13},"pressure":998.42,"humidity":0,"weather":[{"id":800,"main":"Clear","description":"sky is clear","icon":"01d"}],"speed":15.42,"deg":260,"clouds":0},{"dt":1436029200,"temp":{"day":82.94,"min":72.64,"max":82.94,"night":72.64,"eve":80.96,"morn":73.87},"pressure":1002.15,"humidity":0,"weather":[{"id":500,"main":"Rain","description":"light rain","icon":"10d"}],"speed":10.52,"deg":249,"clouds":8,"rain":0.57},{"dt":1436115600,"temp":{"day":83.21,"min":70.79,"max":83.21,"night":70.79,"eve":82,"morn":74.08},"pressure":1002.08,"humidity":0,"weather":[{"id":500,"main":"Rain","description":"light rain","icon":"10d"}],"speed":4.1,"deg":226,"clouds":16}]}
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

	This is interesting. API Call has minor bug ?. When I passed unknow as city argument.It returns Emungalan weather data
	>>>python2.7 summarise_forecast.py unknown
	{'city': u'Emungalan', 'min': 52.23, 'forecasts': {u'Clear': ['2015-06-24', '2015-06-25', '2015-06-26', '2015-06-27', '2015-06-28', '2015-06-29', '2015-06-30', '2015-07-01', '2015-07-02', '2015-07-03', '2015-07-04', '2015-07-05', '2015-07-06', '2015-07-07']}, 'max': 87.55}

	>>>python2.7 -m unittest summarise_forecast
	..
	----------------------------------------------------------------------
	Ran 2 tests in 0.072s

	OK

	"""
    sys.exit(main())
