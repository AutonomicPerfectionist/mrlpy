import sys
import time
import atexit
import signal
import logging
from mrlpy.exceptions import HandshakeTimeout
from mrlpy import mcommand
from mrlpy import utils
from mrlpy.mevent import Message
from mrlpy.utils import MRLListener
from mrlpy.framework import runtime

"""Represents the base service class"""


class Service(object):
    name = ""

    # DEPRECATED, replaced with built-in handshake procedure
    handshakeSuccessful = False
    handshakeTimeout = 1
    handshakeSleepPeriod = 0.25
    createProxyOnFailedHandshake = True
    proxyClass = "PythonProxy"
    # End deprecated

    __log = logging.getLogger(__name__)

    def __init__(self, name=""):
        """
        Registers service with mcommand event registers and MRL service registry
        """

        self.mrl_listeners: dict[str, list[MRLListener]] = dict()

        if name == "":
            try:
                # Get name from args
                self.name = sys.argv[1]
            except IndexError:
                # No first argument
                # Need to auto-generate name
                self.name = utils.genID()
        else:
            self.name = name
        # self.connectWithProxy(True) #Proxy classes are not needed in Nixie
        mcommand.addEventListener(self.name, self.onMessage)
        mcommand.addEventListener(f"{self.name}@{runtime.runtime_id}", self.onMessage)
        # Will release service when Python exits. TODO Check to see if necessary with Messages2 API
        atexit.register(self.release)
        # signal.pause()

    def setProxyClass(self, proxy):
        self.proxyClass = proxy

    # Deprecated, handled in mcommand with builtin handshake facilities
    def connectWithProxy(self, tryagain=False):
        """
        Utility method used for getting initialization info from proxy and running handshake
        """
        # Can do this since it won't do anything if proxy already active
        mcommand.sendCommand("runtime", "createAndStart",
                             [self.name, self.proxyClass])
        # Useful for determining whether the proxy service has been created yet
        mrlRet = mcommand.callServiceWithJson(self.name, "handshake", [])
        self.__log.debug("mrlRet = " + str(mrlRet))
        # If we get to here, MRL is running because mcommand did not throw an exception TODO: Use mrlRet to determine
        #  if we need to create a proxy service Register this service with MRL's messaging system (Actually,
        #  with mcommand's event registers, which forward the event here) Proxy service forwards all messages to
        #  mcommand
        mcommand.addEventListener(self.name, self.onMessage)
        # BEGIN HANDSHAKE$
        start = time.time()
        lastTime = 0
        while (not self.handshakeSuccessful) and ((time.time() - start) < self.handshakeTimeout):
            time.sleep(self.handshakeSleepPeriod)
            lastTime = time.time()
            if lastTime - start >= self.handshakeTimeout:
                if self.createProxyOnFailedHandshake and tryagain:
                    self.__log.info("Proxy not active. Creating proxy...")
                    mcommand.sendCommand("runtime", "createAndStart", [
                        self.name, "PythonProxy"])
                    self.connectWithProxy()
                else:
                    raise HandshakeTimeout(
                        "Error attempting to sync with MRL proxy service; Proxy name = " + str(self.name))
        # END HANDSHAKE#

    def onMessage(self, e: Message):
        """
        Handles message invocation and parsing
        of params; WARNING: DO NOT OVERRIDE
        THIS METHOD UNLESS YOU KNOW WHAT YOU
        ARE DOING!!!!!!!
        """
        # Enables sending a return value back; Other half implemented in mcommand and proxy service
        ret = None
        # Invoke method with data
        if len(e.data) > 0:
            params = ','.join(map(str, e.data))
            self.__log.debug("Invoking: " + e.method + '(' + params + ')')
            ret = getattr(self, e.method).__call__(*e.data)
        else:
            self.__log.debug("Invoking: " + e.method + '()')
            ret = getattr(self, e.method).__call__()
        if e.method in self.mrl_listeners:
            for listener in self.mrl_listeners[e.method]:
                mcommand.sendCommand(listener.callbackName, listener.callbackMethod, [ret])

    def returnData(self, dat):
        mcommand.sendCommand(self.name, "returnData", [dat])

    # Deprecated, replaced with built-in handshake in mcommand

    def handshake(self):
        """
        Second half of handshake.

        Called by proxy during the handshake procedure.
        """

        self.__log.debug("Handshake successful.")
        self.handshakeSuccessful = True

    def release(self):
        """
        Utility method for releasing the proxy service;
        Also deletes this service
        """
        # mcommand.sendCommand("runtime", "release", [self.name])
        del self

    def outMessage(self, msg):
        if len(msg.sender) == 0:
            msg.sender = self.name
        mcommand.eventDispatch.dispatch_event(msg)

    def out(self, method, params=()):
        self.outMessage(Message(self.name, method, params))

    def addListener(self, *args, **kwargs):
        """
        Register a callback on a topic method.
        There are 2 ways to call this method, to account for the
        overloaded Java signature

        1. addListener(listener: MRLListener)
        2. addListener(topicMethod: str, callbackName: str, callbackMethod: str)

        You can pass the arguments either regularly or as keyword arguments,
        but you must be consistent. Don't pass some arguments regularly and
        others as keyword args.
        """

        if type(args[0]) == MRLListener:
            listener = args[0]
        elif 'listener' in kwargs:
            listener = kwargs['listener']
        elif len(args) >= 3:
            listener = MRLListener(args[0], args[1], args[2])
        else:
            listener = MRLListener(**kwargs)

        if listener.topicMethod in self.mrl_listeners:
            self.mrl_listeners[listener.topicMethod].append(listener)
        else:
            self.mrl_listeners.update({listener.topicMethod: [listener]})

    # Aliases to provide similar API to Java MRL, no functional difference in Python due to single thread design
    invoke = out
    invokeMessage = outMessage
