import pypboy
import config

from pypboy.modules.data import entities

class Module(pypboy.SubModule):

	label = "Radio"

	def __init__(self, *args, **kwargs):
		super(Module, self).__init__(*args, **kwargs)
		self.gnr = entities.GalaxyNewsRadio()
		self.add(self.gnr)
		self.gnr.play()

	def handle_event(self, event):
		if event.type ==  config.EVENTS['SONG_END']:
			if hasattr(self, 'active_station'):
				self.active_station.play_random()