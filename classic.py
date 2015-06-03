# classic.py
# Edward Ahn + esahn + Section H

import pygame
from pygame.locals import *
from pygameAnimationClass import PygameAnimationClass
from sprites import *
import os

class Classic(PygameAnimationClass):

	# reads contents in file called filename (from class notes)
	@staticmethod
	def readFile(filename, mode="rt"):
	    # rt = "read text"
	    with open(filename, mode) as fin:
	        return fin.read()

	# writes a file with filename and contents (from class notes)
	@staticmethod
	def writeFile(filename, contents, mode="wt"):
	    # wt = "write text"
	    with open(filename, mode) as fout:
	        fout.write(contents)

	# constructs instance of classic mode
	def __init__(self, windSpeed, music, strength, rangeFactor):
	    super(Classic, self).__init__()
	    self.title = "PANDAMONIUM"
	    self.music = music
	    self.windSpeed = windSpeed
	    self.strength = strength
	    self.rangeFactor = rangeFactor

	# plays background music
	# music source: Two Dots IOS game theme song
	# https://www.youtube.com/watch?v=PeDLgq23jfU
	def playTheme(self):
		if (not self.music): return
		pygame.mixer.music.stop()
		try:
			pygame.mixer.music.load("theme1.ogg")
			pygame.mixer.music.play(-1)
		except: return

	# plays background music
	# music source: Two Dots IOS game theme song
	# https://www.youtube.com/watch?v=MTtXCroWpwU
	def playMusic(self):
		if (not self.music): return
		pygame.mixer.music.stop()
		try:
			pygame.mixer.music.load("theme2.ogg")
			pygame.mixer.music.play(-1)
		except: return

	# initializes all important variables to classic mode
	def initAnimation(self):
	    self.leaf = Leaf(self.width, self.height, self.windSpeed, self.strength)
	    self.player = Player(self.width, self.height)
	    self.basket = Basket(self.width,self.height)
	    self.allSprites = pygame.sprite.RenderPlain((
	    	self.player,self.basket,self.leaf))
	    self.isGameOver = False
	    # need at least this distance to be able to blow on the leaf
	    self.offset = max(self.player.rect.size)
	    # blow will stop affecting leaf once leaf reaches this max
	    self.rangeOfBlow = 1.2*self.offset*self.rangeFactor
	    self.counter = 0 # counts seconds; blows only last 1 seconds
	    self.score = 0
	    self.highScore = self.getHighScore()

	# inits only some var; called when player scores and game isn't over yet
	def partialInit(self):
		self.leaf = Leaf(self.width, self.height, self.windSpeed, self.strength)
		self.player = Player(self.width, self.height)
		self.basket = Basket(self.width,self.height)
		self.allSprites = pygame.sprite.RenderPlain((
	    	self.player,self.basket,self.leaf))
		self.counter = 0

	# returns background of game
	def setBackground(self):
		# source: http://www.mrwallpaper.com/Sunny-Autumn-Landscape-wallpaper/
		background = pygame.image.load("background.jpg").convert()
		background = pygame.transform.scale(background,(900,500))
		return background

	# responds to key presses made by player
	def onKeyPressed(self, event):
		self.counter = pygame.time.get_ticks()
		if (event.key == pygame.K_UP):
			collision = self.isPlayerLeafCollision()
			if (collision != False):
				self.leaf.blow(collision,self.counter)
		elif (event.key == pygame.K_LEFT):
			self.player.movingLeft = True
			(self.player.facingRight,self.player.facingLeft) = (False,True)
		elif (event.key == pygame.K_RIGHT):
			self.player.movingRight = True
			(self.player.facingRight,self.player.facingLeft) = (True,False)
		elif (event.key == pygame.K_r):
			self.initAnimation()

	# responds to key releases made by player
	def onKeyReleased(self, event):
		if (event.key == pygame.K_UP):
			self.leaf.blown = False
			self.counter = 0
		elif (event.key == pygame.K_LEFT):
			self.player.movingLeft = False
		elif (event.key == pygame.K_RIGHT):
			self.player.movingRight = False

	# method that keeps timer moving
	def onTimerFired(self):
		if (self.isGameOver):
			return
		self.leaf.update()
		self.player.update()
		# stops player blowing if leaf gets too far away
		if (self.isPlayerLeafCollision(self.rangeOfBlow) == False):
			self.leaf.blown = False
		if (self.isLeafBasketCollision()):
			self.score += 1
			if (self.score > self.highScore):
				self.highScore = self.score
			self.partialInit()
		# checks if leaf is above ground and if leaf, player in screen
		if (self.leaf.rect.bottom >= self.height or
			self.leaf.rect.left >= self.width or self.leaf.rect.right < 0 or
			self.player.rect.left >= self.width or
			self.player.rect.right < 0):
			self.isGameOver = True
			self.recordScore()

	# records score if score is higher than high score
	def recordScore(self):
		path = "highScoreClassic.txt"
		previousHighScore = int(Classic.readFile(path))
		if (self.highScore > previousHighScore):
			os.remove(path)
			Classic.writeFile(path,str(self.score))

	# returns False if leaf is not in offset
	# returns angle between leaf and head otherwise
	def isPlayerLeafCollision(self,offset=None):
		if (offset == None): offset = self.offset
		(player,leaf) = (self.player,self.leaf)
		bodyToHeadRatio = 0.875 # body is 7/8 size of head
		# location of head on screen
		headX = player.rect.centerx
		headY = self.screen.get_height() - bodyToHeadRatio*player.rect.height
		(leafX,leafY) = leaf.rect.center
		distance = ((headX-leafX)**2 + (headY-leafY)**2)**0.5
		if ( distance > offset or (leafX < headX and player.facingRight) or
			(leafX > headX and player.facingLeft)):
			return False
		else:
			angle = math.acos((leafX-headX)/distance)
			# blowing leaf will accelerate leaf downwards
			if (leafY > headY):
				return (1,angle)
			# blowing straight at leaf will not accelerate leaf
			elif (leafY == headY):
				return (0,angle)
			# blowing leaf will accelerate leaf upwards
			else: return (-1,angle)

	# returns True if leaf hits basket
	def isLeafBasketCollision(self):
		(basket,leaf) = (self.basket,self.leaf)
		(leafX,leafY) = leaf.rect.center
		basketY = basket.rect.top
		basketLeft = basket.rect.left
		basketRight = basket.rect.right
		if (leafX < basketRight and leafX > basketLeft):
			if (leafY > basketY):
				return True
		return False

	# redraws pygame screen
	def redrawAll(self):
	    self.allSprites.draw(self.screen)
	    self.displayScore()
	    if (self.isGameOver):
	    	self.displayGameOver()

	# draws score on screen
	def displayScore(self):
		if pygame.font:
			size = 20
			font = pygame.font.SysFont("baskerville",size)
			score = font.render("Score: %d" % (self.score), 1, (0,0,0))
			scorePos = score.get_rect(centerx=780,centery=150)
			highScore = font.render("High Score: %d" % (self.highScore),
				1, (0,0,0))
			highScorePos = score.get_rect(centerx=760,centery=120)
			self.screen.blit(score,scorePos)
			self.screen.blit(highScore,highScorePos)

	# displays game over screen
	def displayGameOver(self):
		pygame.draw.rect(self.screen,(102,51,0),(150,200,600,100))
		if pygame.font:
			size = 36
			font = pygame.font.SysFont("baskerville", size)
			text1 = font.render("You scored %d point(s)!" % self.score,
				1,(204,102,0))
			text1Pos = text1.get_rect(centerx=self.width/2,centery=
				self.height/2-25)
			text2 = font.render("Press 'r' to play another game!",1,(204,102,0))
			text2Pos = text2.get_rect(centerx=self.width/2,
				centery=self.height/2+25)
			self.screen.blit(text1,text1Pos)
			self.screen.blit(text2,text2Pos)

	# returns high score from file
	def getHighScore(self):
		path = "highScoreClassic.txt"
		highScore = 0
		# create the highScore.txt, if it is not there
		if (not os.path.exists("highScoreClassic.txt")):
			Classic.writeFile(path,"0")
		else:
			highScore = int(Classic.readFile(path))
		# change score if score is higher than previous high score
		if (self.score > highScore):
			os.remove(path)
			Classic.writeFile(path,str(self.score))
			highScore = self.score
		return highScore
