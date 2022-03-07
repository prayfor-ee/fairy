#find info in database
import common as C
import apikey as API_KEY
import requesturl as REQUEST_URL

import datetime
import requests
import json

#단기예보
#request_server = http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst

class DataManager:

	def __init__(self):
		pass

	def request_weather(self):
		#단기예보
		request_url = REQUEST_URL.DATA_GO_VILAGE_FCST

		#초단기예보
		#request_url = REQUEST_URL.DATA_GO_ULTRA_SRT_FCST

		today = datetime.datetime.today()
		base_date = today.strftime("%Y%m%d") # "20220307" == 기준 날짜
		base_time = "0500" # 날씨 값

		nx = "62"
		ny = "123"
		
		params = {'serviceKey' : API_KEY.DATA_GO_DECODING_KEY, 
		#'pageNo' : '50', 
		#'numOfRows' : '12', #Total 12 / 
		'dataType' : 'json', 
		'base_date' : base_date, 
		'base_time' : base_time, 
		'nx' : nx, 
		'ny' : ny }

		res = requests.get(request_url, params=params)
		
		if res.status_code == 200 :#normal
			C.P(f"res.status_code [{res.status_code}]")
			#C.P(f"res.content [{res.content}]")
			items = res.json().get('response').get('body').get('items')
			C.P(f"items [{items}]")
		else:
			C.P("error! because ")#, res.json())

		#C.P(f"res.content [{res.content}]")

#params ={'serviceKey' : '서비스키', 'pageNo' : '1', 'numOfRows' : '1000', 'dataType' : 'XML', 'base_date' : '20210628', 'base_time' : '0500', 'nx' : '55', 'ny' : '127' }

#response = requests.get(url, params=params)
#print(response.content)
		#items = res.json().get('response').get('body').get('items')