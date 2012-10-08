from pypboy import BaseModule
from pypboy.modules.items import weapons
from pypboy.modules.items import apparel
from pypboy.modules.items import aid
from pypboy.modules.items import misc
from pypboy.modules.items import ammo


class Module(BaseModule):

	label = "ITEMS"

	submodules = [
		weapons.Module(),
		apparel.Module(),
		aid.Module(),
		misc.Module(),
		ammo.Module()
	]

	def __init__(self, *args, **kwargs):
		super(Module, self).__init__(*args, **kwargs)
