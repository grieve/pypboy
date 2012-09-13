import pygame
import game


class Scanlines(game.Entity):

    def __init__(self, width, height, gap, colours, *args, **kwargs):
        self.width = width
        self.height = height
        self.gap = gap
        self.colours = colours
        self.offset = 0
        super(Scanlines, self).__init__((width, height), *args, **kwargs)

    def render(self, *args, **kwargs):
        colour = 0
        area = pygame.Rect(0, self.offset, self.width, self.gap)
        while area.top <= self.height - self.gap:
            self.fill(self.colours[colour], area)
            area.move_ip(0, self.gap)
            colour += 1
            if colour >= len(self.colours):
                colour = 0
        self.offset += 1
        if self.offset >= self.gap:
            self.offset = 0
        super(Scanlines, self).render(self, *args, **kwargs)
