"""
Python-equivalent of org.myrobotlab.service.Runtime. Methods that require
the actual MRL runtime instead just call the connected MRL instance, such as createAndStart.
Methods not needing the actual MRL runtime are reimplemented, such as getHelloResponse.
Runtime is a singleton, and so is not written inside of a class, unlike the real Runtime
(since Java requires everything to be a class, even if they are a singleton)
"""

import logging
from mrlpy import mcommand
from mrlpy.framework.service import Service
from mrlpy.utils import DescribeResults


class Runtime(Service):
    compatMode = False
    compatObj = None
    _runtime = None
    __log = logging.getLogger(__name__)

    def __init__(self, name="runtime"):
        if Runtime.getRuntime() is not None:
            raise ValueError(
                "Runtime is a singleton and there is already an instance.")
        super().__init__(name)

    @classmethod
    def createAndStart(cls, name, service_type):
        return mcommand.callService("runtime", "createAndStart", [name, service_type])

    @classmethod
    def shutdown(cls):
        mcommand.sendCommand("runtime", "shutdown", [])

    @classmethod
    def getRuntime(cls):
        return cls._runtime

    @classmethod
    def start(cls, name, service_type):
        return mcommand.callService("runtime", "start", [name, service_type])

    @classmethod
    def describe(cls, uuid="platform", query=None):
        results = DescribeResults()
        results.status = None
        results.id = "obsidian"
        results.registrations.append({"id": "obsidian", "name": "runtime",
                                      "typeKey": "org.myrobotlab.service.Runtime", "service": None, "state": "{}"})
        # results.registrations.append({"id": "obsidian", "name": "NativePython",
        #                               "typeKey": None, "service": None, "state": None})
        return results

    @classmethod
    def setCompat(cls, mode):
        cls.compatMode = mode

    @classmethod
    def setCompatServiceObject(cls, obj):
        cls.compatObj = obj

    @classmethod
    def init_runtime(cls):
        cls._runtime = Runtime()

    @classmethod
    def onDescribe(cls, results: DescribeResults):
        cls.__log.debug("Got describe results")

    def getHelloResponse(uuid, request):
        """
        Remote MRL will call this after we initiate contact, uuid will be unusuable until
        we replace it with our own generated uuid for the connected server (useful for multi-server connections
        but not for single-server connections)
        """
        response = {
            "id": "obsidian",
            "request": request,
            "services": [],
        }
        return response
