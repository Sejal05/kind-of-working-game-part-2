import pygame
from settings import *
vec = pygame.math.Vector2
import pytweening as tween

def collide_with_walls(sprite, group, dir):
    if dir == 'x':  # if x collision
        hits = pygame.sprite.spritecollide(sprite, group, False)    # checks if hits between player and wall
        if hits:
            if sprite.vel.x > 0:                                                # if player hits to the left side of the wall
                sprite.pos.x = hits[0].rect.left - sprite.rect.width            # then player's position is whatever wall got hit - how wide sprite is ( to put us right against it)
            if sprite.vel.x < 0:                                                # if player hits to the right side of the wall
                sprite.pos.x = hits[0].rect.right                               # then player's position is at right hand side of wall
            sprite.vel.x = 0                                                    # player stops moving
            sprite.rect.x = sprite.pos.x                                        # the new player's position
    if dir == 'y':                                                              # if y collision
        hits = pygame.sprite.spritecollide(sprite, group, False)
        if hits:
            if sprite.vel.y > 0:                                                # if player is moving down
                sprite.pos.y = hits[0].rect.top - sprite.rect.height            # we should be on the top of the block -  player's height
            if sprite.vel.y < 0:                                                # if player is moving up
                sprite.pos.y = hits[0].rect.bottom                              # player should hit bottom of the wall
            sprite.vel.y = 0                                                    # player stops moving in y direction
            sprite.rect.y = sprite.pos.y                                        # the new player's position

class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pygame.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pygame.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pygame.transform.scale(image, (width // 2, height // 2))
        return image

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.waling = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.pos = vec(x, y)    # keeps track on what grid coordinate we are on
        self.last_fire = 0
        self.health = 100
        self.lives = 3
        self.hide_timer = pygame.time.get_ticks()
        self.offset = vec(10, 0)

    def load_images(self):
        self.standing_frames = [self.game.spritesheet.get_image(144, 288, 144, 144) ]
        for frame in self.standing_frames:
            frame.set_colorkey(BLACK)

        self.walk_frames_r = [self.game.spritesheet.get_image(0, 288, 144, 144),
                              self.game.spritesheet.get_image(148, 288, 144, 144),
                              self.game.spritesheet.get_image(292, 288, 144, 144),
                                                                                 ]

        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            frame.set_colorkey(BLACK)
            self.walk_frames_l.append(pygame.transform.flip(frame, True, False)) and frame.set_colorkey(BLACK)


    def animate(self):
        # walking animation
        now = pygame.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False

        if self.walking:
            if now - self.last_update > 40:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                center = self.rect.center
                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    self.image = self.walk_frames_l[self.current_frame]
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_SPACE]:
                        now = pygame.time.get_ticks()
                        if now - self.last_fire > FIRE_RATE:
                            self.last_fire = now
                            dir = vec(-1, 0)
                            pos = self.pos + FIRE_OFFSET
                            Fire(self.game, pos, dir)
                self.rect = self.image.get_rect()


        if self.jumping:
            if now - self.last_update > 40:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.jump_frames)
                self.image = self.jump_frames[self.current_frame]
                self.rect = self.image.get_rect()

        # idle animation
        if not self.jumping and not self.walking:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()

    def key_movement(self):
        self.acc = vec(0, PLAYER_GRAV)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.vel.x = -PLAYER_ACC
            if keys[pygame.K_SPACE]:
                    now = pygame.time.get_ticks()
                    if now - self.last_fire > FIRE_RATE:
                        self.last_fire = now
                        dir = vec(-1, 0)
                        pos = self.pos + FIRE_OFFSET
                        Fire(self.game, pos, dir)
        if keys[pygame.K_RIGHT]:
            self.vel.x = PLAYER_ACC
        if keys[pygame.K_UP]:
            self.jump()
        if keys[pygame.K_DOWN]:
            self.vel.y = PLAYER_ACC
        if self.acc.x != 0 and self.acc.y != 0:   # to move diagonally
            self.vx *= 0.7071
            self.vy *= 0.7071
        if keys[pygame.K_SPACE]:
            now = pygame.time.get_ticks()
            if now - self.last_fire > FIRE_RATE:
                self.last_fire = now
                dir = vec(1, 0)
                pos = self.pos + FIRE_OFFSET
                Fire(self.game, pos, dir)

    def jump(self):
        # jump only if standing on a platform
        # self.rect.y += 1
        # hits = pygame.sprite.spritecollide(self, self.game.walls, False)
        # self.rect.y -= 1
        # if hits:
        self.vel.y = -25
       # self.jumping = True

    def update(self):
        self.animate()
        self.acc = vec(0, PLAYER_GRAV)
        self.key_movement()
        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc  # self.game.dt
        self.rect.x = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')            # collide with walls in the x direction
        self.rect.y = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')            # collide with walls in the y direction

    def add_heatlh(self, amount):
        self.health += amount
        if self.health > PLAYER_HEALTH:
            self.health = PLAYER_HEALTH

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, pos):
        self.groups = game.all_sprites, game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.enemy_img.copy()
        self.rect = self.image.get_rect()
        self.health = 100
        self.rect.center = pos
        self.pos = pos
        self.tween = tween.easeInOutSine
        self.step = 0
        self.dir = 1

    def update(self):
        offset = BOB_RANGE * (self.tween(self.step / BOB_RANGE) - 0.5)
        self.rect.centerx = self.pos.x + offset * self.dir
        self.step += BOB_SPEED
        if self.step > BOB_RANGE:
            self.step = 0
            self.dir *= -1

    # self.find = self.game.player.pos - self.pos
        # self.acc = vec(ENEMY1_SPEED, 0)
        # self.acc += self.vel * -1
        # self.vel += self.acc * self.game.dt
        # self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        # self.rect.center = self.pos
        # collide_with_walls(self, self.game.walls, 'x')
        # collide_with_walls(self, self.game.walls, 'y')
        if self.health <= 0:
            self.kill()

    def draw_health(self):
        if self.health > 60:
            col = GREEN
        elif self.health > 30:
            col = YELLOW
        else:
            col = RED
        width = int(self.rect.width * self.health / ENEMY1_HEALTH)
        self.health_bar = pygame.Rect(0, 0, width, 7)
        if self.health < ENEMY1_HEALTH:
            pygame.draw.rect(self.image, col, self.health_bar)

class Fire(pygame.sprite.Sprite):
    def __init__(self, game, pos, dir):
        self.groups = game.all_sprites, game.fires
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.fire_img
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        self.vel = dir * FIRE_SPEED
        self.spwan_time = pygame.time.get_ticks()

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pygame.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pygame.time.get_ticks() - self.spwan_time > FIRE_LIFETIME:
            self.kill()

class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((TILESIZE, TILESIZE))  # making a surface
        self.image.fill(PURPLE)                            # fills with a colour
        self.rect = self.image.get_rect()
        self.x = x                                         # keeps track on what grid coordinate we are on
        self.y = y
        self.rect.x = x * TILESIZE                         # ksends the sprite to a particular location
        self.rect.y = y * TILESIZE

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, game, x, y, w, h):                   # Obstacles for the tiles
        self.groups = game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pygame.Rect(x, y, w, h)                 # creates a rectangle
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

class Item(pygame.sprite.Sprite):
    def __init__(self, game, pos, type):                    # find positing and type of item
        self.groups = game.all_sprites, game.items
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.item_images[type]
        self.rect = self.image.get_rect()
        self.type = type
        self.rect.center = pos
        self.pos = pos
        self.tween = tween.easeInOutSine
        self.step = 0
        self.dir = 1

    def update(self):
        # bobbing motion
        offset = BOB_RANGE * (self.tween(self.step / BOB_RANGE) - 0.5)
        self.rect.centery = self.pos.y + offset * self.dir
        self.step += BOB_SPEED
        if self.step > BOB_RANGE:
            self.step = 0
            self.dir *= -1

class Heart(pygame.sprite.Sprite):
    def __init__(self, game, pos):
        self.groups = game.all_sprites, game.hearts
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.heart_img
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.pos = pos
        self.tween = tween.easeInOutSine
        self.step = 0
        self.dir = 1

    def update(self):
        # bobbing motion
        offset = MOVE_RANGE * (self.tween(self.step / MOVE_RANGE) - 0.5)
        self.rect.centery = self.pos.y + offset * self.dir
        self.step += MOVE_SPEED
        if self.step > MOVE_RANGE:
            self.step = 0
            self.dir *= -1