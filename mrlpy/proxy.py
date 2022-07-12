'''
Base class for proxy services
'''

class Proxy(object):
	def __init__(self, classtype, name):
		self._type = classtype
		self.name = name
