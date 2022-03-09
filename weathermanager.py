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
		requestUrl = REQUEST_URL.DATA_GO_VILAGE_FCST

		#초단기예보
		#requestUrl = REQUEST_URL.DATA_GO_ULTRA_SRT_FCST

		today = datetime.datetime.today()
		base_date = today.strftime("%Y%m%d") #오늘 날짜

		time = common_utils.get_current_time("%H%M")
		base_time = self.get_basetime(time)	#base_time = "0500" # 날씨 값

		#ex) 분당 62 123
		nx = "62"
		ny = "123"
		
		#params ={"serviceKey" : "서비스키", "pageNo" : "1", "numOfRows" : "1000", "dataType" : "XML", "base_date" : "20210628", "base_time" : "0500", "nx" : "55", "ny" : "127" }
		params = {"ServiceKey" : API_KEY.DATA_GO_DECODING_KEY, 
		"pageNo" : "1", 
		"numOfRows" : "500", #when numOfRows is about 500, i can get TMN and TMX.
		"dataType" : "json", 
		"base_date" : base_date, 
		"base_time" : base_time, 
		"nx" : nx, 
		"ny" : ny }

		res = requests.get(requestUrl, params=params)
		
		if res.status_code == 200 :#normal
			#C.P(f"res.content [{res.content}]")
			jsonkeylist = ["response", "body", "items"]
			items = common_utils.get_jsonvalue(res.json(), jsonkeylist)
			#items = res.json().get("response").get("body").get("items")
			#C.P(f"items [{items}]")

			self.get_weather_info(items)
		else:
			C.P(f"ERROR : code [{res.status_code}] ")#, res.json())

		del common_utils
		#C.P(f"res.content [{res.content}]")

	def get_basetime(self, currenttime):
		time = 0
		if type(currenttime) != int:
			try:
				time = int(currenttime)
			except:
				C.P("ERROR : can not change type(int)")
		else:
			time = currenttime
		
		#- Base_time : 0200, 0500, 0800, 1100, 1400, 1700, 2000, 2300 (1일 8회)
		#- API 제공 시간(~이후) : 02:10, 05:10, 08:10, 11:10, 14:10, 17:10, 20:10, 23:10
		base_time = ""
		if time >= 0 and time < 200:
			base_time = "2300"
		elif time >= 200 and time < 500:
			base_time = "0200"
		elif time >= 500 and time < 800:
			base_time = "0500"
		elif time >= 800 and time < 1100:
			base_time = "0800"
		elif time >= 1100 and time < 1400:
			base_time = "1100"
		elif time >= 1400 and time < 1700:
			base_time = "1400"
		elif time >= 1700 and time < 2000:
			base_time = "1700"
		elif time >= 2000 and time < 2300:
			base_time = "2000"
		elif time >= 2300 and time < 2400:
			base_time = "2300"
		else:
			base_time = "0500"

		return base_time

	def get_weather_info(self, source):
		#source = {"item": [{"baseDate": "20220309", "baseTime": "0500", "category": "TMP", "fcstDate": "20220309", "fcstTime": "0600", "fcstValue": "1", "nx": 62, "ny": 123}, {"baseDate": ...
		common_utils = C.CommonUtils()
		item = common_utils.get_jsonvalue(source, "item")
		C.P(f"type [{type(item)}, item [{item}]")

		settingvalue = 0
		#infolist = ["TMP","UUU","VVV","VEC","WSD","SKY","PTY","POP","WAV","PCP","REH","SNO","TMN","TMX"]
		infodict = {"TMP" : False, 
						"UUU" : False,
						"VVV" : False,
						"VEC" : False,
						"WSD" : False,
						"SKY" : False,
						"PTY" : False,
						"POP" : False,
						"WAV" : False,
						"PCP" : False,
						"REH" : False,
						"SNO" : False,
						"TMN" : False,
						"TMX" : False}

				#for key, value in match_dict.items():
    			#	print(key, ":", value)
		weatherInfo = {}
		for data in item:
			if "category" in data:
				#C.P(f"data [{data["category"]}]")
				category = data["category"]
				if infodict[category] == True :	#There is no(?) need to check again about the information that has already been set.
					continue
				
				if "fcstValue" in data:
					fcstValue = data["fcstValue"]
					categoryStr = self.category_to_str(category)
					fcstInfo = self.fcstvalue_to_info(category, fcstValue)
					C.P(f"data [{categoryStr} : {fcstInfo}]")
					weatherInfo[categoryStr] = fcstInfo
					infodict[category] = True	# completed setting = true
					settingvalue = settingvalue + 1

			if len(infodict) == settingvalue:	# completed setting all the information.
				break
					
		del common_utils
		return weatherInfo

	def category_to_str(self, category):
#TMP : 1시간 온도
#UUU : 풍속(동서성분)
#VVV: 풍속(남북성분)
#VEC: 풍향
#WSD: 풍속
#SKY: 하늘상태
#PTY: 강수형태
#POP: 강수확률
#WAV: 파고
#PCP: 1시간 강수량
#REH: 습도
#SNO: 1시간 신적설
#TMN: 일 최저기온
#TMX: 일 최고기온
		match_dict = {"TMP" : "1시간온도", 
						"UUU" : "풍속(동서성분)",
						"VVV" : "풍속(남북성분)",
						"VEC" : "풍향",
						"WSD" : "풍속",
						"SKY" : "하늘상태",
						"PTY" : "강수형태",
						"POP" : "강수확률",
						"WAV" : "파고",
						"PCP" : "1시간강수량",
						"REH" : "습도",
						"SNO" : "1시간신적설",
						"TMN" : "일최저기온",
						"TMX" : "일최고기온"}
		if category in match_dict:
			return match_dict[category]

			
			
	def fcstvalue_to_info(self, category, fcstvalue):
#SKY: 하늘상태
#- 하늘상태(SKY) 코드 : 맑음(1), 구름많음(3), 흐림(4)
#PTY: 강수형태
#- 강수형태(PTY) 코드 : (초단기) 없음(0), 비(1), 비/눈(2), 눈(3), 빗방울(5), 빗방울눈날림(6), 눈날림(7) 
#                      (단기) 없음(0), 비(1), 비/눈(2), 눈(3), 소나기(4) 
#- 초단기예보, 단기예보 강수량(RN1, PCP) 범주 및 표시방법(값)
		if "SKY" == category:
			if fcstvalue == "1":
				fcstvalue = "맑음"
			elif fcstvalue == "3":
				fcstvalue = "구름많음"
			elif fcstvalue == "4":
				fcstvalue = "흐림"
			else:
				fcstvalue = "UnKnown"
		elif "PTY" == category:
			if fcstvalue == "0":
				fcstvalue = "없음"
			elif fcstvalue == "1":
				fcstvalue = "비"
			elif fcstvalue == "2":
				fcstvalue = "비/눈"
			elif fcstvalue == "3":
				fcstvalue = "눈"
			elif fcstvalue == "4":
				fcstvalue = "소나기"
			elif fcstvalue == "5":
				fcstvalue = "빗방울"
			elif fcstvalue == "6":
				fcstvalue = "빗방울/눈날림"
			elif fcstvalue == "7":
				fcstvalue = "눈날림"
			else:
				fcstvalue = "UnKnown"

		return fcstvalue

		