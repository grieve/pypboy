from pypboy import BaseModule
from pypboy.modules.data import local_map
from pypboy.modules.data import world_map
from pypboy.modules.data import quests
from pypboy.modules.data import misc
from pypboy.modules.data import radio


class Module(BaseModule):

	label = "DATA"

	submodules = [
		local_map.Module(),
		world_map.Module(),
		quests.Module(),
		misc.Module(),
		radio.Module()
	]

	def __init__(self, *args, **kwargs):
		super(Module, self).__init__(*args, **kwargs)
