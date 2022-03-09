import json
import datetime

P = print

class CommonUtils:
	
	def get_current_time(self, formatted = '%Y%m%d%H%M%S'):
		"""get current time

		Args:
			formatted (str, optional): formatted time. Defaults to '%Y%m%d%H%M%S'.

		Returns:
			str: current time
		"""
		now = datetime.datetime.now()
		nowDate = now.strftime(formatted)
		return nowDate
		
	def get_jsonvalue(self, jsonobject, key):
		"""get json value from key

		Args:
			jsonobject (jsonObject): source json object
			key (str or list): get value from key

		Returns:
			str or object or list: value
		"""
		if type(key) == str:
			if key in jsonobject:
				return jsonobject.get(key)
		elif type(key) == list:
			if len(key) > 0:
				if len(key) == 1:
					strkey = key[0]
					return self.get_jsonvalue(jsonobject, strkey)

				if key[0] in jsonobject:
					depthjsonobject = jsonobject.get(key[0])
					del key[0]
					return self.get_jsonvalue(depthjsonobject, key)
				else:
					return ''
		return ''