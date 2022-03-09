import json

P = print

class CommonUtils:
	
	def get_jsonvalue(self, jsonobject, key):
		
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