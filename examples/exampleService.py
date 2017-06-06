from mrlpy.mservice import MService

class ExampleService(MService):

	#Basic constructor of service, should have this signature but not required
	def __init__(self, name=""):
		#REALLY REALLY REALLY IMPORTANT TO CALL THIS, otherwise service is not registered, name not allocated, everything blows up
		super(ExampleService, self).__init__(name)

	#Normal method declarations. MService handles messaging and invocation of methods, so nothing special is needed
	def doSomething(self):
		Print "Doing something interesting"
	
	#etc.
