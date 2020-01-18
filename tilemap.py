import pygame
import os
from settings import *
import pytmx


class Map:
    def __init__(self, filename):
        self.data = []
        with open(filename, 'rt') as f:         # load the file name and read
            for line in f:                      # for each line
                self.data.append(line.strip())  # adds in the program

        self.tilewidth = len(self.data[0])      # how many tiles wide the map
        self.tileheight = len(self.data)        # how many tiles long for the map
        self.width = self.tilewidth * TILESIZE  # pixel width
        self.height = self.tileheight * TILESIZE

# load the tmx file
class TiledMap:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth                # width of map
        self.height = tm.height * tm.tileheight             # height of map
        self.tmxdata = tm                                   # refer to data as tm

    def render(self, surface):                              # takes a pygame surface and draw the tiles onto a map
        ti = self.tmxdata.get_tile_image_by_gid             # command to find an image to with a certain tile
        for layer in self.tmxdata.visible_layers:           # going through each visible layer
            if isinstance(layer, pytmx.TiledTileLayer):     # if layer is tiled
                for x, y, gid, in layer:                    # get the x, y and gid
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth,     # if it is a tile then draw it onto map
                                            y * self.tmxdata.tileheight))

    def make_map(self):
        temp_surface = pygame.Surface((self.width, self.height))  # creates a surface to draw the map onto
        self.render(temp_surface)
        return temp_surface


# a camera for the moving sprite
class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)      # the size of the camera
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)  # retuns the sprite entity and moves the camera to where the new camera coordiantes are

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)         # returns the rectangle moved by the camera's offset

    # where the camera will be shifting to / updating to where the sprite is moving
    def update(self, target):
        x = -target.rect.x + int(WIDTH / 2)  # moves the map in the other direction to where the sprite is moving
        y = -target.rect.y + int(HEIGHT / 2)

        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - WIDTH), x)  # right
        y = max(-(self.height - HEIGHT), y)  # bottom
        self.camera = pygame.Rect(x, y, self.width, self.height) # camera rectangle is constant


