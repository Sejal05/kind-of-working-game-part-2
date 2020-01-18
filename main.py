import pygame
import sys
from os import path
from settings import *
from sprite import *
from tilemap import *

def draw_player_health(surf, x, y, pct): #pct - percentge of health
    if pct < 0:
        pct = 0
    BAR_LENGTH = 200
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)    # outline of health bar
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)             # colour of the health bar
    if pct > 0.6:
        col = GREEN                                             # if health is more than 60% it shows green
    elif pct > 0.3:                                             # more than 30% will show yellow and less will show red
        col = YELLOW
    else:
        col = RED
    pygame.draw.rect(surf, col, fill_rect)                      # draws the health bar onto screen
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_lives(surf, x, y, lives, img):      # draw lives onto screen
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)

class Game:
    def __init__(self):         # initialising pygame
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT)) # creating a window with width and height
        pygame.display.set_caption(TITLE)                               # the title of the game will display at the top
        self.clock = pygame.time.Clock()                                # keeps track of how the game is running
        self.load_data()
        self.font_name = pygame.font.match_font(FONT_NAME)
        self.level = 1

    def load_data(self):
        game_folder = path.dirname(__file__)
        self.dir = path.dirname(__file__)
        img_folder = path.join(self.dir, 'images')
        data_folder = path.join(game_folder, 'data')
        # load spritesheet image
        self.spritesheet = Spritesheet(path.join(img_folder, SPRITESHEETCAT)) #load spritesheet image
        self.player_mini_img = pygame.image.load(path.join(img_folder, LIFE_IMG))
        self.enemy_img = pygame.image.load(path.join(img_folder, ENEMY1_img))
        self.fire_img = pygame.image.load(path.join(img_folder, FIRE_IMG))
        self.heart_img = pygame.image.load(path.join(img_folder, HEART_IMG))
        self.item_images = {}
        for item in ITEM_IMAGES:
            self.item_images[item] = pygame.image.load(path.join(img_folder, ITEM_IMAGES[item]))

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.fires = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.hearts = pygame.sprite.Group()
        game_folder = path.dirname(__file__)
        data_folder = path.join(game_folder, 'data')
        self.map = TiledMap(path.join(data_folder, 'map1.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        for tile_object in self.map.tmxdata.objects:                        # loops for each object in the tilemap
            if tile_object.name == 'Player':
                self.player = Player(self, tile_object.x, tile_object.y)    # Spawns player is object is called 'Player'
            if tile_object.name == 'Enemy1':
                Enemy(self, vec(tile_object.x, tile_object.y))
            if tile_object.name == 'Wall':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name =='heart':
                Heart(self, vec(tile_object.x, tile_object.y))
            if tile_object.name in ['health']:
                Item(self, vec(tile_object.x, tile_object.y), tile_object.name)
        self.camera = Camera(self.map.width, self.map.height)  # spwans the camera

        self.camera = Camera(self.map.width, self.map.height)    # spwans the camera to the size of the map

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000 # keep running the game at the appropriate speed
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pygame.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)  # camera updates to track the player
        # player hits the item
        hits = pygame.sprite.spritecollide(self.player, self.items, False, pygame.sprite.collide_mask)
        for hit in hits:
            if hit.type == 'health' and self.player.health < PLAYER_HEALTH:
                hit.kill()
                self.player.add_heatlh(HEALTH_POTION_AMOUNT)
        # GAME OVER
        if pygame.sprite.spritecollide(self.player, self.hearts, self.hearts, False):
            self.show_go_screen()
        # enemies hit player
        hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
        for hit in hits:
            self.player.health -= ENEMY1_DAMAGE
            hit.vel = vec(0, 0)
            if self.player.health <= 0:
                self.gameOver()
                self.player.lives -= 1
                self.player.health = 100
        if self.player.lives == 0:
            self.playing = False

        if hits:
            self.player.pos += vec(ENEMY1_KNOCKBACK, 0)
        # when the punch hits the enemies
        hits = pygame.sprite.groupcollide(self.enemies, self.fires, False, True)
        for hit in hits:
            hit.health -= FIRE_DAMAGE
            hit.vel = vec(0, 0)


    def draw(self):
        pygame.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        for sprite in self.all_sprites:
            if isinstance(sprite, Enemy):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))   # applying the camera to the sprites

            pygame.draw.rect(self.screen, pygame.Color('#FF0000'), sprite.rect, 1)
        draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HEALTH) # HEALTH BAR
        draw_lives(self.screen, WIDTH - 100, 5, self.player.lives, self.player_mini_img)
        pygame.display.flip() # flipping the display would show the drawings

    def events(self):
        # catch all events here
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Checks for closing the window
                self.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)  # keep running the game at the appropriate speed
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pygame.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def show_start_screen(self):
        self.events()
        self.screen.fill(WHITE)
        self.draw_text(TITLE, 40, BLACK, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Can you reach the end to collect the heart to save your owner?", 22, BLACK, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press UP to Jump, LEFT and RIGHT to move and SPACE BAR to attack", 18, BLACK, WIDTH / 2, 350)
        pygame.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        self.events()
        self.screen.fill(WHITE)
        self.draw_text("Well Done! You have successfully completed the first level", 22, BLACK, WIDTH / 2,
                       HEIGHT / 2)
        pygame.display.flip()
        self.wait_for_key()

    def gameOver(self):
        self.events()
        self.screen.fill(WHITE)
        self.draw_text("You have lost a life!", 22, BLACK, WIDTH / 2,
                       HEIGHT / 2)
        pygame.display.flip()
        self.wait_for_key()

# create the game object  / game loop
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()