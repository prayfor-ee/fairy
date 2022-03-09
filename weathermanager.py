#find info in database
import common as C
import apikey as API_KEY
import requesturl as REQUEST_URL

import datetime
import requests
import json

#단기예보
#request_server = http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst

class WeatherManager:

	def __init__(self):
		pass

	def get_location(self, text):
		#load excel or numbers file
		#find text
		#get nx ny 
		
		pass

	def request_weather(self):
		common_utils = C.CommonUtils()
		#단기예보
		request_url = REQUEST_URL.DATA_GO_VILAGE_FCST

		#초단기예보
		#request_url = REQUEST_URL.DATA_GO_ULTRA_SRT_FCST

		today = datetime.datetime.today()
		base_date = today.strftime("%Y%m%d") # "20220307" == 기준 날짜
		base_time = "0500" # 날씨 값

		time = common_utils.get_current_time('%H%M')
		C.P(f"time [{time}]")

		nx = "62"
		ny = "123"
		
		#params ={'serviceKey' : '서비스키', 'pageNo' : '1', 'numOfRows' : '1000', 'dataType' : 'XML', 'base_date' : '20210628', 'base_time' : '0500', 'nx' : '55', 'ny' : '127' }
		params = {'ServiceKey' : API_KEY.DATA_GO_DECODING_KEY, 
		'pageNo' : '1', 
		'numOfRows' : '12', #Total 12 / 
		'dataType' : 'json', 
		'base_date' : base_date, 
		'base_time' : base_time, 
		'nx' : nx, 
		'ny' : ny }

		res = requests.get(request_url, params=params)
		
		if res.status_code == 200 :#normal
			#C.P(f"res.content [{res.content}]")
			jsonkeylist = ['response', 'body', 'items']
			items = common_utils.get_jsonvalue(res.json(), jsonkeylist)
			#items = res.json().get('response').get('body').get('items')
			#C.P(f"items [{items}]")

			self.get_weather_info(items)
		else:
			C.P(f"ERROR : code [{res.status_code}] ")#, res.json())

		del common_utils
		#C.P(f"res.content [{res.content}]")

	def get_basetime(self, currenttime):
		#- Base_time : 0200, 0500, 0800, 1100, 1400, 1700, 2000, 2300 (1일 8회)
		#- API 제공 시간(~이후) : 02:10, 05:10, 08:10, 11:10, 14:10, 17:10, 20:10, 23:10
		return ''

	def get_weather_info(self, source):
		#source = {'item': [{'baseDate': '20220309', 'baseTime': '0500', 'category': 'TMP', 'fcstDate': '20220309', 'fcstTime': '0600', 'fcstValue': '1', 'nx': 62, 'ny': 123}, {'baseDate': ...
		common_utils = C.CommonUtils()
		item = common_utils.get_jsonvalue(source, 'item')
		C.P(f"type [{type(item)}, item [{item}]")
		for data in item:
			if 'category' in data:
				#C.P(f"data [{data['category']}]")
				if 'fcstValue' in data:
					C.P(f"data [{data['category']} : {data['fcstValue']}]")
		del common_utils