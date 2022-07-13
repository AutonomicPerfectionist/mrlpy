from mrlpy import mcommand
from mrlpy.framework.runtime import Runtime

Runtime.init_runtime()

mcommand.setPort("8888")
mcommand.connect(id="obsidian", daemon=False)
