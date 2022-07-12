import sys
from mrlpy.service import Service
from mrlpy.framework.service import runtime

#Add Runtime to sys.modules under an alias for compatibility mode
sys.modules["org.myrobotlab.service.Runtime"] = runtime.Runtime

#Import under new alias for inclusion in script
from org.myrobotlab.service import Runtime

'''
Special service for running scripts in compatibility mode.
'''

#Puts Runtime in global namespace for use with the script

class MCompatibilityService(Service):
	def __init__(self, name=""):
		super(MCompatibilityService, self).__init__(name)

	def runScript(self, scriptFile):
		'''
		Runs a script inside this compat service, allowing full usage of Jython syntax
		
		scriptFile represents the location of the script.
		'''
		Runtime.setCompat(True)
		Runtime.setCompatServiceObject(self)
		execfile(str(scriptFile), globals(), locals())

	def subscribe(self):
		'''
		Implements python.subscribe()
		'''

		#TODO: Implement
		pass
