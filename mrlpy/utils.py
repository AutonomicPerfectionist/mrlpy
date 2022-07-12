import string
import random
from mrlpy.framework.deserializer import mrl_dataclass
from mrlpy.meventdispatch import MEventDispatch
from mrlpy.mevent import Message
'''
Utility methods and variables
'''

eventDispatch = MEventDispatch()

@mrl_dataclass
class DescribeResults(object):
    id: str
    uuid: str
    request: dict
    platform: object
    status: object
    registrations: list

    def __init__(self):
        self.id = ""
        self.uuid = ""
        self.request = {}
        self.platform = None
        self.status = None
        self.registrations = []


@mrl_dataclass
class MRLListener(object):
    topicMethod: str
    callbackName: str
    callbackMethod: str

    def __call__(self, ev):
        message = Message(self.callbackName, self.callbackMethod, ev.data)
        eventDispatch.dispatch_event(message)

    def __hash__(self) -> int:
        return 37 + self.topicMethod.__hash__() + self.callbackName.__hash__() + self.callbackMethod.__hash__()


@mrl_dataclass
class DescribeQuery(object):
    id: str
    uuid: str
    platform: object


def genID(size=6, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    '''
    Generate a random ID for creating unique names
    '''
    return ''.join(random.choice(chars) for _ in range(size))
