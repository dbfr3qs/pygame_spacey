import pygame, random, thesprites, os
# a very simple space invaders type game
# requires the sprites


class Star(object): # background stars
	x_pos = 0
	y_pos = 0
	
	def __init__(self):
		self.x_pos = random.randrange(0, thesprites.SCREEN_WIDTH)
		self.y_pos = random.randrange(0, thesprites.SCREEN_HEIGHT)
		
	def update(self):
		self.y_pos+=1
		if self.y_pos > thesprites.SCREEN_HEIGHT:
			self.x_pos = random.randrange(0, thesprites.SCREEN_WIDTH)
			self.y_pos = -10 #random.randrange(0, thesprites.SCREEN_HEIGHT)

class Game(object):
	
	block_list = None
	all_sprites_list = None
	bullet_list = None
	player = None
	bulletnumber = 0
	time_passed = 0
	game_over = False
	score = 0
	ticker = 0
	star_list = None
	sprite_total = 0
	sprite_remainder = 0
	
	def __init__(self):
		
		self.score = 0
		self.game_over = False
		self.ticker = pygame.time.Clock()
		self.time_passed = 0
		self.block_list = pygame.sprite.Group()
		self.all_sprites_list = pygame.sprite.Group()
		self.bullet_list = pygame.sprite.Group()
		self.bulletnumber = 0
		self.star_list = []
		self.sprite_total = 8 # the most blocks on the screen at a time will be 20. The total for a level will be this added to sprite_remainder, ie 20+30=50.
		self.sprite_remainder = 40
		self.click_sound = pygame.mixer.Sound(os.path.join("assets", "laser.ogg")) # set up the laser sound
		
		pygame.mixer.music.load(os.path.join("assets", "Chiptune_Heros.mp3")) # load up the background music
		pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
		pygame.mixer.music.play()
		
		self.ticker.tick()
		
		for i in range(self.sprite_total): # set up enemy sprites
			self.block = thesprites.Block()
			
			self.block.rect.x = random.randrange(thesprites.SCREEN_WIDTH)
			self.block.rect.y = random.randrange(-800, thesprites.SCREEN_HEIGHT-500) # set them so they start above the screen initially
				
			self.block_list.add(self.block)
			self.all_sprites_list.add(self.block)
		
		for i in range(100): # set up 100 stars
			self.star = Star()
			self.star_list.append(self.star)
			
		self.player = thesprites.Player()
		self.all_sprites_list.add(self.player)
		
	def add_block(self): # add a single new block
		self.block = thesprites.Block()
					
		self.block.rect.x = random.randrange(thesprites.SCREEN_WIDTH)
		self.block.rect.y = random.randrange(-800, thesprites.SCREEN_HEIGHT-500) # set them so they start above the screen initially
						
		self.block_list.add(self.block)
		self.all_sprites_list.add(self.block)		
		
	def process_events(self): # all the events, key presses etc
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return True
			if event.type == pygame.MOUSEBUTTONDOWN:
				if self.game_over:
					self.__init__()
			if event.type == pygame.KEYDOWN: #if mouse button clicked and player is over a sprite remove it and increase the score
				if not self.game_over:
					if event.key == pygame.K_SPACE:
						self.bullet = thesprites.Bullet()
						self.bullet.rect.x = (self.player.rect.x+15)
						self.bullet.rect.y = self.player.rect.y
						self.all_sprites_list.add(self.bullet)
						self.bullet_list.add(self.bullet)
						self.click_sound.play() # play the laser sound
						self.bulletnumber+=1 #keep track of the number of bullets fired for score calculation
			if event.type == pygame.KEYDOWN:
				if not self.game_over:
					if event.key == pygame.K_LEFT:
						self.player.move_left = True
					if event.key == pygame.K_RIGHT:
						self.player.move_right = True
					if event.key == pygame.K_DOWN:
						self.player.move_down = True
					if event.key == pygame.K_UP:
						self.player.move_up = True
			if event.type == pygame.KEYUP: # stop moving if any of the arrow keys are depressed
				if not self.game_over:
					if event.key == pygame.K_LEFT:
						self.player.move_left = False
					if event.key == pygame.K_RIGHT:
						self.player.move_right = False
					if event.key == pygame.K_DOWN:
						self.player.move_down = False
					if event.key == pygame.K_UP:
						self.player.move_up = False
			if event.type == pygame.constants.USEREVENT:
				pygame.mixer.music.load(os.path.join("assets", "Chiptune_Heros.mp3")) # restart the background music once it reaches the end
				pygame.mixer.music.play()
								
	def run_logic(self):
		#runs once per frame, move the sprites and check if the game is over
		if not self.game_over:
			self.all_sprites_list.update()
			for i in range(100):
				self.star_list[i].update()
			
			for bullet in self.bullet_list: # check if bullet has hit a block
				self.blocks_hit_list = pygame.sprite.spritecollide(self.bullet, self.block_list, True)
				
				for block in self.blocks_hit_list:
					self.bullet_list.remove(self.bullet)
					self.all_sprites_list.remove(self.bullet)
					if self.sprite_remainder > 0: # if a block is killed add another
						self.add_block()
						self.sprite_remainder-=1
					self.score+=((self.score // self.bulletnumber) + 100) #calculate the score
					#print(self.score)
				
				if self.bullet.rect.y < -10: #move the bullet
					self.bullet_list.remove(self.bullet)
					self.all_sprites_list.remove(self.bullet)
				
			for block in self.block_list: # check if the player has run into a block if so kill the game
				self.blocks_hit_list = pygame.sprite.spritecollide(self.player, self.block_list, True)
				
				for block in self.blocks_hit_list:
					self.player.move_left = False
					self.player.move_right = False
					self.player.move_down = False
					self.player.move_up = False
					self.game_over = True
						
		if len(self.block_list) == 0:
			self.game_over = True
			
	def display_frame(self, screen): #screen stuff
		
		screen.fill(thesprites.BLACK)
		
		if self.game_over:
			font = pygame.font.SysFont("serif", 25)
			text = font.render("Game over, click to restart", True, thesprites.WHITE)
			center_x = (thesprites.SCREEN_WIDTH // 2) - (text.get_width() // 2)
			center_y = (thesprites.SCREEN_HEIGHT // 2) - (text.get_height() // 2)
			screen.blit(text, [center_x, center_y])
			pygame.mixer.music.stop() # stop the music when the game is over
			
		if not self.game_over:
			self.all_sprites_list.draw(screen)
			for i in range(100):
				# draw the stars
				pygame.draw.circle(screen, thesprites.WHITE, (self.star_list[i].x_pos, self.star_list[i].y_pos), 2)
		
		self.time_passed += self.ticker.get_time()
		
		if not self.game_over:
			if self.time_passed > 10000: # start decreasing the score after 10s
				if (self.time_passed % 100 == 10):	
					if (self.score > 0):
						self.score-=50	
					
		font = pygame.font.SysFont("serif", 15) 
		text = font.render("SCORE: " + str(self.score), True, thesprites.WHITE)
		screen.blit(text, [5, 475]) # print the score at the bottom left of the screen
			
		pygame.display.flip()
		
def main():
	
	pygame.init()
	
	size = [thesprites.SCREEN_WIDTH, thesprites.SCREEN_HEIGHT]
	screen = pygame.display.set_mode(size)
	
	pygame.display.set_caption("My Blocks")
	#pygame.mouse.set_visible(False)
	
	done = False	
	clock = pygame.time.Clock()
	
	game = Game()
	
	while not done:
		done = game.process_events()
		
		game.run_logic()
		
		game.display_frame(screen)
	
		clock.tick(60)		
			
 	pygame.quit()

if __name__ == "__main__":
	main()
