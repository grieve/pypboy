import pypboy
import pygame
import game
import config


class Module(pypboy.SubModule):

	label = "Skills"

	def __init__(self, *args, **kwargs):
		super(Module, self).__init__(*args, **kwargs)