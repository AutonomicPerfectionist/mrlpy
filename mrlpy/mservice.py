global mcommand
global sys
import mcommand
import sys
import time
from mrlpy.exceptions import HandshakeTimeout

"""Represents the base service class"""


class MService (object):
	name = ""	
	handshakeSuccessful = False
	handshakeTimeout = 1000 
	handshakeSleepPeriod = 0.25

	######################################
	#Register service with mcommand event#
	# registers and mrl service registry #
	######################################
	def __init__(self, name=""):
		if name == "":
			#Get name from args
			self.name = sys.argv[2]
		else:
			self.name = name
		#Useful for determining whether the proxy service has been created yet
		mrlRet = mcommand.callServiceWithJson(name, "handshake", [])

		#If we get to here, MRL is running because mcommand did not throw an exception

		#TODO: Use mrlRet to determine if we need to create a proxy service

		#Register this service with MRL's messaging system (Actually, with mcommand's event registers, which forward the event here)
		#Proxy service forwards all messages to mcommand
		mcommand.addEventListener(self.name, self.onEvent)

		#BEGIN HANDSHAKE$
		start = time.time()
		lastTime = 0
		while not self.handshakeSuccessful or (time.time() - start) < self.handshakeTimeout:
			lastTime = time.time()
			time.sleep(self.handshakeSleepPeriod)
		if lastTime - start >= timeout:
			raise HandshakeTimeout("Error attempting to sync with MRL proxy service; Proxy name = " + str(self.name))
		#END HANDSHAKE#

	#########################################
	#Handles message invocation and parsing #
	#of params; WARNING: DO NOT OVERRIDE	#
	#THIS METHOD UNLESS YOU KNOW WHAT YOU	#
	#ARE DOING!!!!!!!			#
	#########################################
	def onEvent(self, e):
		#Enables sending a return value back; Other half implemented in mcommand and proxy service
		ret = None
		#Invoke method with data
		try:
			params = ','.join(map(str, e.data))
			print "Invoking: " + e.method + '(' + params + ')'
			ret = eval('self.' + e.method + '(' + params + ')')
		except Exception:
			print "Invoking: " + e.method + '()'
                        ret = eval('self.' + e.method + '()')
		return ret

	##########################
	#Second half of handshake#
	##########################
	def handshake(self):
		global handshakeSuccessful
		print "Handshake successful."
		handshake = True
