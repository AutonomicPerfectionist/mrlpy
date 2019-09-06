import logging
import time

class MEvent( object ):
    """
    Event object to use with MEventDispatch.
    """

    def __init__(self, event_type):
        """
        The constructor accepts an event type as string
        """
        self._type = event_type

    @property
    def type(self):
        """
        Returns the event type
        """
        return self._type

    @property
    def data(self):
        """
        Returns the data associated to the event
        """
        return self._data

"""Subclass of MEvent, used to represent MRL messages"""
class Message(MEvent):
	name = ""
	method = ""
	data = []
	msgID = 0
	srcID = "" #TODO add source ID
	sender = "" #Set by message creator
	log = logging.getLogger(__name__)



	def __init__(self, name, method, dat=[]):
		self.log.debug("Creating message structure")
		self.name = name
		self.log.debug("Name set: " + name)
		self.method = method
		self.log.debug("Method set: " + method)
		self.data = dat
		self.log.debug("Data set" )

		#UNIX epoch timestamp, any system capable of running mrlpy should have sub-second time
		#May not represent actual timeline of messages if connecting between two different systems
		self.msgID = int(time.time() * 1000)
		super(MrlMessage, self).__init__(name)
