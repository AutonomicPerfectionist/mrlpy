"""
Python-equivalent of org.myrobotlab.service.Runtime. Methods that require
the actual MRL runtime instead just call the connected MRL instance, such as createAndStart.
Methods not needing the actual MRL runtime are reimplemented, such as getHelloResponse.
Runtime is a singleton, and so is not written inside of a class, unlike the real Runtime
(since Java requires everything to be a class, even if they are a singleton)
"""

import logging

import mrlpy.framework.runtime
from mrlpy import mcommand
from mrlpy.framework.service import Service
from mrlpy.utils import DescribeResults, Registration, MRLListener

runtime_id = "obsidian"


class Runtime(Service):
    compatMode = False
    compatObj = None
    _runtime = None
    __log = logging.getLogger(__name__)

    def __init__(self, name="runtime"):
        self.remote_id = None
        self.listeners = []
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

    def describe(self, uuid="platform", query=None):
        # Add listener for describe
        listener = MRLListener("describe", "runtime@obsidian", "onDescribe")
        mcommand.sendCommand("runtime", "addListener", [listener], sender="runtime@obsidian")

        # Add listener for registered
        listener = MRLListener("registered", "runtime@obsidian", "onRegistered")
        mcommand.sendCommand("runtime", "addListener", [listener], sender="runtime@obsidian")

        if query is not None:
            self.remote_id = query.id
        self.__log.info("Describing: " + str(query))
        results = DescribeResults()
        results.status = None
        results.id = runtime_id
        results.registrations.append({"id": runtime_id, "name": "runtime",
                                      "typeKey": "org.myrobotlab.service.Runtime", "service": "{}", "state": "{}"})
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

    def onRegistered(self, registration: Registration):
        self.__log.info(f"Registered service {registration.name}@{registration.id} (type {registration.typeKey})")

    def onDescribe(self, results: DescribeResults):
        self.__log.info("Got describe results")

    # def getHelloResponse(uuid, request):
    #     """
    #     Remote MRL will call this after we initiate contact, uuid will be unusuable until
    #     we replace it with our own generated uuid for the connected server (useful for multi-server connections
    #     but not for single-server connections)
    #     """
    #     response = {
    #         "id": "obsidian",
    #         "request": request,
    #         "services": [],
    #     }
    #     return response
