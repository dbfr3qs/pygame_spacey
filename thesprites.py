import pygame, random, os

# sprite module for spritemodules.py

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500	

class Block(pygame.sprite.Sprite):
	
	def __init__(self):
		
		pygame.sprite.Sprite.__init__(self)
		
		self.image = pygame.image.load(os.path.join("assets", "enemyBlue2.png")).convert()
		self.image.set_colorkey(BLACK)
		self.image = pygame.transform.scale(self.image, (30, 30))
		
		#get the dimensions of it
		self.rect = self.image.get_rect()
		
	def reset_pos(self):
		self.rect.y = random.randrange(-300, -30)
		self.rect.x = random.randrange(SCREEN_WIDTH)
		
	def update(self):
		self.rect.y += 2	
		if self.rect.y > SCREEN_HEIGHT + self.rect.height:
			self.reset_pos()
		
class Player(pygame.sprite.Sprite):

	move_left = False
	move_right = False
	move_up = False
	move_down = False	
	
	def __init__(self): #setup player sprite
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(os.path.join("assets","spaceship.png")).convert()
		self.image.set_colorkey(BLACK)
		#self.image.fill(RED)
		self.image = pygame.transform.scale(self.image, (30, 30))
		self.rect = self.image.get_rect()
		self.rect.x = SCREEN_WIDTH // 2
		self.rect.y = SCREEN_HEIGHT // 2

	def update(self):
		if self.move_left == True: 
			if self.rect.x > 0:
				self.rect.x-=4
		if self.move_right == True:
			if self.rect.x < 670:
				self.rect.x+=4
		if self.move_down == True:
			if self.rect.y < 470:
				self.rect.y+=4
		if self.move_up == True:
			if self.rect.y > 0:
				self.rect.y-=4			

class Bullet(pygame.sprite.Sprite): # bullet class
	
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([5, 5])
		self.image.fill(GREEN)
		self.rect = self.image.get_rect()
	
	def update(self):
		self.rect.y-=3
