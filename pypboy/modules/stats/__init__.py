from pypboy import BaseModule
from pypboy.modules.stats import status
from pypboy.modules.stats import special
from pypboy.modules.stats import skills
from pypboy.modules.stats import perks
from pypboy.modules.stats import general


class Module(BaseModule):

	label = "STATS"

	submodules = [
		status.Module(),
		special.Module(),
		skills.Module(),
		perks.Module(),
		general.Module()
	]

	def __init__(self, *args, **kwargs):
		super(Module, self).__init__(*args, **kwargs)
