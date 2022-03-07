#find info in database
import common as C
import apikey as API_KEY
import requesturl as REQUEST_URL

import datatime
import requests
import json

#단기예보
#request_server = http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst

class DataManager:

	def __init__(self):
		pass

	def request_weather(self):
		#단기예보
		request_server = REQUEST_URL.DATA_GO_VILAGE_FCST

		#초단기예보
		#request_server = REQUEST_URL.DATA_GO_ULTRA_SRT_FCST