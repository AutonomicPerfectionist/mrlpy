# MrlPy
This is a native-python API to the MyRobotLab robotics framework. MrlPy uses MRL's webgui service as the API hook point,
and is capable of creating and registering services written in native Python. In addition to this, MrlPy is also capable of
interpreting scripts written for MRL's Jython interpreter.

## APIs
MrlPy contains three different API tiers: the Command API, the Service API, and the Compatibility API.

### Command API
The lowest of the APIs is the Command API, represented by mrlpy.mcommand. The Command API
can be used for controlling MRL directly, as well as calling service methods and receiving feedback. The most important functions
are mcommand.sendCommand() and mcommand.callService(), leveraging MRL's message API and services API respectively.
mcommand.sendCommand() will return a status code of what happened, while mcommand.callService() will return whatever that service's
called method returned.

### Service API
The Service API is the next API tier. It is responsible for creating, registering, and syncing native Python services
with MRL In order to write a new service, one only needs to subclass the MService class, found in mrlpy.mservice.
MRL service calls can be made through mcommand.callService(), which also generates a proxy class for a returned service.
For example:
```python
ard = mrlpy.mcommand.callService("runtime", "createAndStart", ["ard", "Arduino"]
ard.connect("/dev/ttyUSB0")
#This works because mcommand.callService() generates a proxy service for any returned service.
```
### Compatibility API
The Compatibility API is the highest tier. This API was written so that scripts written for MRL's Jython interpreter would still
function. This API exposes the proxy org.myrobotlab.service.Runtime module, enabling calling of MRL's Runtime through the proxy.
The Compatibility API leverages the Service API to provide messaging and proxy service creation.
Compatibility scripts must be ran through the MCompatibilityService (***NOT YET IMPLEMENTED!!!***)
For example, this script is called test.py and was originally written for MRL's Jython interpreter.
```python
ai = Runtime.createAndStart("ai", "ProgramAB")
ai.startSession()
print ai.getResponse("Hello")
```
To run this, open a terminal and type this:
```bash
$ mcompat-run test.py
```

# Known Issues
1. Messaging to and from Service API only implemented in this project. PythonProxy has yet to implement the other half
2. Proxy classes aren't converted back to json when calling a service method that requires a Service Interface.
3. mcompat-run does not yet exist

# TODO: COMPLETE DOCUMENTATION  
