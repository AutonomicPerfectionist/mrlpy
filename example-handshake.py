from mrlpy import mcommand
from mrlpy.framework.runtime import Runtime
from mrlpy.utils import MRLListener, DescribeQuery

mcommand.setPort("8888")
mcommand.connect(id="obsidian", daemon=False)
Runtime.init_runtime()

# Add listener for describe
listener = MRLListener("describe", "runtime@obsidian", "onDescribe")
print(mcommand.sendCommand("runtime", "addListener", [listener], sender="runtime@obsidian"))
# mcommand.eventDispatch.add_event_listener(

# Add listener for registered
listener = MRLListener("registered", "runtime@obsidian", "onRegistered")
print(mcommand.sendCommand("runtime", "addListener", [listener], sender="runtime@obsidian"))

# Send describe
desc_query = DescribeQuery("obsidian", None, None)
print(mcommand.sendCommand("runtime@jealous-kyoko", "describe", ["fill-uuid", desc_query], sender="runtime@obsidian"))
print(mcommand.sendCommand("runtime@jealous-kyoko", "onDescribe", [Runtime.describe()], sender="runtime@obsidian"))

# class TestService(Service):
#         def __init__(self, name):
#                 super(TestService, self).__init__(name)

#         def test(self):
#                 print("TEST SUCCESSFUL")

# t = TestService("t")
