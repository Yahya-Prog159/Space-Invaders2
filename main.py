import pygame
from pygame import mixer
from pygame.locals import *
import random
import button

# initializing the mixer 
pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()

pygame.init()


# FPS
clock = pygame.time.Clock()
fps = 60


SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700
# SCREEN_WIDTH = 500
# SCREEN_HEIGHT = 650

# Define colors 
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Space Invaders2')


# Load button images
start_btn_img = pygame.image.load('img/pixel_art_start.png').convert_alpha()
exit_btn_img = pygame.image.load('img/pixel_art_exit.png').convert_alpha()


# Create the button instances
start_btn = button.Button(250, 450, start_btn_img, 1)
exit_btn = button.Button(250, 550, exit_btn_img, 1)



# Define fonts
font30 = pygame.font.SysFont('Constantia', 30)
font40 = pygame.font.SysFont('Constantia', 40)

# Load sounds
explosion_sfx = pygame.mixer.Sound('img/explosion.wav')
explosion_sfx.set_volume(.25)

explosion_sfx2 = pygame.mixer.Sound('img/explosion2.wav')
explosion_sfx2.set_volume(.25)

laser_sfx = pygame.mixer.Sound('img/laser.wav')
laser_sfx.set_volume(.25)


# Define Game variables
rows = 5
cols = 5
alien_cooldown = 1000
last_alien_shot = pygame.time.get_ticks()
countdown = 3
last_count = pygame.time.get_ticks()
game_over = 0# 0 means no game over, 1 means player wins, -1 means player has lost 



# Load image
bg = pygame.image.load('img/bg.png')

def draw_bg():
	screen.blit(bg, (0, 0))

# Function to draw  text
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y)) 


class Spaceship(pygame.sprite.Sprite):
	def __init__(self, x, y, health):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('img/spaceship.png')
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.health_start = health
		self.health_remaining = health
		self.last_shot = pygame.time.get_ticks()


	def update(self):
		# Set movement speed
		speed = 8

		# set the cooldown
		cooldown = 500 # milliseconds

		game_over = 0

		# Get key press
		key = pygame.key.get_pressed()
		if key[pygame.K_LEFT] and self.rect.left > 0:
			self.rect.x -= speed
		if key[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
			self.rect.x += speed

		# record current time 
		time_now = pygame.time.get_ticks()

		# Shoot
		if key[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
			laser_sfx.play()
			bullet = Bullets(self.rect.centerx, self.rect.top)
			bullets_group.add(bullet)
			self.last_shot = time_now


		# update mask
		self.mask = pygame.mask.from_surface(self.image)

		# Draw the health bar
		pygame.draw.rect(screen, red, (self.rect.x, (self.rect.bottom + 10), self.rect.width, 15))
		if self.health_remaining > 0:
			pygame.draw.rect(screen, green, (self.rect.x, (self.rect.bottom + 10), int(self.rect.width * (self.health_remaining / self.health_start)), 15))
		elif self.health_remaining <= 0:
			explosion = Explosion(self.rect.centerx, self.rect.centery, 3)
			explosion_group.add(explosion)
			self.kill()
			game_over = -1
		return game_over


# Create the Bullets
class Bullets(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('img/bullet.png')
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
	def update(self):
		self.rect.y -= 5
		if self.rect.bottom < 0:
			self.kill()
		if pygame.sprite.spritecollide(self, alien_group, True):
			self.kill()
			explosion_sfx.play()
			explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
			explosion_group.add(explosion)



# Create the Aliens
class Aliens(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('img/alien'+ str(random.randint(1, 5)) + '.png')
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.move_counter = 0
		self.move_direction = 1

	def update(self):
		self.rect.x += self.move_direction
		self.move_counter += 1
		if abs(self.move_counter) > 50:
			self.move_direction *= -1
			self.move_counter *= self.move_direction



# Create the Aliens Bullets
class Aliens_Bullets(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('img/alien_bullet.png')
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
	def update(self):
		self.rect.y += 2
		if self.rect.top > SCREEN_HEIGHT:
			self.kill()
		if pygame.sprite.spritecollide(self, spaceship_group, False, pygame.sprite.collide_mask):
			explosion_sfx2.play()
			self.kill()
			# reduce spaceship health
			spaceship.health_remaining -= 1
			explosion = Explosion(self.rect.centerx, self.rect.centery, 1)
			explosion_group.add(explosion)


# Create Explosion Bullets
class Explosion(pygame.sprite.Sprite):
	def __init__(self, x, y, size):
		pygame.sprite.Sprite.__init__(self)
		self.imgs = []
		for num in range(1, 6):
			img = pygame.image.load(f'img/exp{num}.png')
			if size == 1:
				img = pygame.transform.scale(img, (20, 20))
			if size == 2:
				img = pygame.transform.scale(img, (40, 40))
			if size == 3:
				img = pygame.transform.scale(img, (160, 160))
			self.imgs.append(img)
		self.index = 0	
		self.image = self.imgs[self.index]
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.counter = 0

	def update(self):
		explosion_speed = 3
		# update explosion animation
		self.counter += 1

		if self.counter >= explosion_speed and self.index < len(self.imgs) - 1:
			self.counter = 0
			self.index += 1
			self.image = self.imgs[self.index]

		# if the animation is complete, delete
		if self.index >= len(self.imgs) - 1 and self.counter >= explosion_speed:
			self.kill()



def reset_game():
    global countdown, last_count, game_over, spaceship, spaceship_group, bullets_group, alien_group, alien_bullet_group, explosion_group

    # Reset the countdown and last count time
    countdown = 3
    last_count = pygame.time.get_ticks()
    
    # Reset game over state
    game_over = 0
    
    # Clear existing sprite groups
    spaceship_group.empty()
    bullets_group.empty()
    alien_group.empty()
    alien_bullet_group.empty()
    explosion_group.empty()
    
    # Recreate player
    spaceship = Spaceship(int(SCREEN_WIDTH / 2), SCREEN_HEIGHT - 100, 3)
    spaceship_group.add(spaceship)
    
    # Recreate aliens
    create_aliens()





# Create sprite groups
spaceship_group = pygame.sprite.Group()
bullets_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()
alien_bullet_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()


def create_aliens():
	# generate aliens
	for row in range(rows):
		for item in range(cols):
			alien = Aliens(100 + item * 100, 100 + row * 70)
			alien_group.add(alien)

create_aliens()

# Create player
spaceship = Spaceship(int(SCREEN_WIDTH / 2), SCREEN_HEIGHT - 100, 3)
spaceship_group.add(spaceship)

font = pygame.font.Font('img/Pixeltype.ttf', 80)
txt = font.render('Space Invaders 2', 1, 'green')

run = True
start_game = False

while run:

	clock.tick(fps)

	# Draw the background
	draw_bg()

	if not start_game:
	
		screen.blit(txt, (100, 150))
		if start_btn.draw(screen):
			start_game = True
		if exit_btn.draw(screen):
			run = False
		
	else:

		if countdown == 0:
			# game_over = 0
			# Create random alien bullets
			# Record current time
			time_now = pygame.time.get_ticks()
			# Shoot
			if time_now - last_alien_shot > alien_cooldown and len(alien_bullet_group) < 5 and len(alien_group) > 0:
				attaking_alien = random.choice(alien_group.sprites())
				alien_bullet = Aliens_Bullets(attaking_alien.rect.centerx, attaking_alien.rect.bottom)
				alien_bullet_group.add(alien_bullet)
				last_alien_shot = time_now


			# Check if all the aliens have been killed
			if len(alien_group) == 0:
				game_over = 1

			if game_over == 0:
				# update sprite groups
				game_over = spaceship.update()
				bullets_group.update()
				alien_group.update()
				alien_bullet_group.update()

			if game_over != 0:
				if game_over == -1:
					draw_text('You Lose!', font40, white, int(SCREEN_WIDTH / 2 - 100), int(SCREEN_HEIGHT / 2))
				if game_over == 1:
					draw_text('You Win!', font40, white, int(SCREEN_WIDTH / 2 - 90), int(SCREEN_HEIGHT / 2))
				pygame.display.update()
				pygame.time.wait(2000)
				if game_over == -1:
					reset_game()
					start_game = False
					game_over = 0
				elif game_over == 1:
					reset_game()
					start_game = False
					game_over = 0





		if countdown > 0:
			draw_text('Get Ready!', font40, white, int(SCREEN_WIDTH / 2 - 85), int(SCREEN_HEIGHT / 2 + 50))
			draw_text(str(countdown), font40, white, int(SCREEN_WIDTH / 2 - 10), int(SCREEN_HEIGHT / 2 + 100))
			count_timer = pygame.time.get_ticks()
			if count_timer - last_count > 1000:
				countdown -= 1
				last_count = count_timer
				


		# Update explosion group
		explosion_group.update()


		# Draw sprite groups
		spaceship_group.draw(screen)
		bullets_group.draw(screen)
		alien_group.draw(screen)
		alien_bullet_group.draw(screen)
		explosion_group.draw(screen)

		# event handlers
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				if game_over != 0:
					reset_game()
					start_game = True

	pygame.display.update()


pygame.quit()
