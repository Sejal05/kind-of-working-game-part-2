import random
import pygame
vec = pygame.math.Vector2

# game options/settings
TITLE = "The Catastrophe!"

# Window size
WIDTH = 1024
HEIGHT = 608
FPS = 60     # how many times the screen will be updated
FONT_NAME = 'arial'
SPRITESHEETCAT = "cats.png"
SPRITESHEETENEMY1 = 'monster.png'
display = pygame.Surface((1024,608))

# Shooting settings
FIRE_IMG = 'fire.png'
FIRE_SPEED = 500
FIRE_LIFETIME = 1000
FIRE_RATE = 150
FIRE_OFFSET = vec(50, 50)
FIRE_DAMAGE = 25

#Life settings
LIFE_IMG = 'life.png'

# Enemy settings
ENEMY1_img = 'monster1.png'
ENEMY1_SPEED = 100
ENEMY1_HEALTH = 100
ENEMY1_DAMAGE = 5
ENEMY1_RANGE = 200
ENEMY1_KNOCKBACK = 30

# Player properties
PLAYER_IMG ='cat.png'
PLAYER_SPEED = 300
PLAYER_HEALTH = 100
PLAYER_ACC = 5  # acceleration of the sprite
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 1.1  # gravity
PLAYER_KICK = 25
PLAYER_HIT_RECT = pygame.Rect(0, 0, 40, 67)

# items
ITEM_IMAGES = {'health': 'health.png' }
HEALTH_POTION_AMOUNT = 20
BOB_RANGE = 15
BOB_SPEED = 0.3

# heart
HEART_IMG = 'heart.png'
MOVE_RANGE = 15
MOVE_SPEED = 0.3

# tile window
TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# defined colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (67, 140, 94)
GRASS = (66, 227, 109)
BLUE = (0, 0, 255)
SKY = (66, 173, 227)
YELLOW = (255, 255, 0)
LIGHTGREY = (100, 100, 100)
CYAN = (3, 252, 240)
CYAN2 = (52, 192, 235)
PURPLE = (146, 98, 103)