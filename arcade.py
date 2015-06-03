# arcade.py
# Edward Ahn + esahn + Section H

import pygame
from pygame.locals import *
from pygameAnimationClass import PygameAnimationClass
from sprites import *
import os

class Arcade(PygameAnimationClass):

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

	# creates instance of arcade mode of this game
	def __init__(self, windSpeed, music, strength, n, rangeFactor):
		super(Arcade,self).__init__()
		self.strength = strength
		self.title = "PANDAMONIUM"
		self.windSpeed = windSpeed
		self.music = music
		self.numOfLeaves = n
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

	# initializes important variables
	def initAnimation(self):
		self.leaves = self.getLeaves(self.numOfLeaves)
		self.player = Player(self.width,self.height)
		self.player.rect.centerx = self.width/2
		self.basketLeft = Basket(self.width,self.height)
		self.basketRight = Basket(self.width,self.height)
		self.basketLeft.rect.centerx = 100
		self.basketRight.rect.centerx = self.width - 100
		self.allSprites = self.getSprites()
		self.isGameOver = False
		self.offset = max(self.player.rect.size)
		self.rangeOfBlow = 1.2*self.offset*self.rangeFactor
		self.counter = 0 # limits blow to 1 second
		self.score = 0 # number of leaves put into the basket
		self.highScore = self.getHighScore()
		(self.minute,self.second) = ("0","00")
		self.previousTicks = pygame.time.get_ticks()
		self.clover = None

	# inits only some var; called when player scores and game isn't over yet
	def partialInit(self):
		self.leaves = self.getLeaves(self.numOfLeaves)
		self.player = Player(self.width,self.height)
		self.player.rect.centerx = self.width/2
		self.allSprites = self.getSprites()
		self.isGameOver = False
		(self.minute,self.second) = ("0","00")
		self.previousTicks = pygame.time.get_ticks()
		self.clover = None
		self.score = 0

	# returns group of n number of leaves
	def getLeaves(self,n):
		leaves = []
		for x in xrange(n):
			leaf = Leaf(self.width,self.height,self.windSpeed,self.strength)
			# prevents leaf from going directly into basket without any blows
			leaf.rect.centerx = self.getLeafX()
			leaf.rect.centery = random.randint(0,self.height)
			leaves.append(leaf)
		return leaves

	# returns random leaf center that isn't above any of the baskets
	def getLeafX(self):
		offset = 200
		x = random.randint(offset,self.width-offset)
		return x

	# returns group of sprites
	def getSprites(self):
		group = []
		group += [self.player,self.basketLeft,self.basketRight]
		group += self.leaves
		group = tuple(group)
		return pygame.sprite.RenderPlain(group)

	# returns background of game
	def setBackground(self):
		background = pygame.image.load("background.jpg").convert()
		background = pygame.transform.scale(background,(900,500))
		return background

	# responds to key presses made by player
	def onKeyPressed(self, event):
		self.counter = pygame.time.get_ticks()
		if (event.key == pygame.K_UP):
			for leaf in self.leaves:
				collision = self.isPlayerLeafCollision(leaf)
				if (collision != False):
					leaf.blow(collision,self.counter)
			if (self.clover != None):
				collision = self.isPlayerLeafCollision(self.clover)
				if (collision != False):
					self.clover.blow(collision,self.counter)
		elif (event.key == pygame.K_LEFT):
			self.player.movingLeft = True
			(self.player.facingRight,self.player.facingLeft) = (False,True)
		elif (event.key == pygame.K_RIGHT):
			self.player.movingRight = True
			(self.player.facingRight,self.player.facingLeft) = (True,False)
		elif (event.key == pygame.K_r):
			self.partialInit()

	# responds to key releases made by player
	def onKeyReleased(self, event):
		if (event.key == pygame.K_UP):
			for leaf in self.leaves:
				leaf.blown = False
			if (self.clover != None): self.clover.blown = False
			self.counter = 0
		elif (event.key == pygame.K_LEFT):
			self.player.movingLeft = False
		elif (event.key == pygame.K_RIGHT):
			self.player.movingRight = False

	# responds to timer firing (creates leaves)
	def onTimerFired(self):
		if (self.isGameOver): return
		self.inputClover()
		t = pygame.time.get_ticks() - self.previousTicks
		if (int(self.second) != t/1000 and int(self.minute) == 0):
			self.incrementTime()
		for leaf in self.leaves:
			if (self.isPlayerLeafCollision(leaf,self.rangeOfBlow) == False):
				leaf.blown = False
			leaf.update()
			if (self.isLeafBasketCollision(leaf)):
				self.score += 1
				if (self.score > self.highScore): self.highScore = self.score
				leaf.rect.centery = 0
				leaf.rect.centerx = self.getLeafX()
			if (leaf.rect.top >= self.height):
				leaf.rect.top = 0
				leaf.rect.centerx = self.getLeafX()
		if (self.clover != None): self.cloverAction()
		self.player.update()

	# returns true randomly; more likely to return true at end of minute
	def randomize(self,t):
		sec = int(self.second)
		# clovers may start appearing after 45 seconds on the clock
		start = 45
		if (sec > start):
			# clover produced if t has units, tens digit of 1
			# (just for random's sake)
			if (t%10 == 1 and t%100 == 1):
				return True
		return False

	# randomly inputs four leaf clover into game; clover worth 5 points
	def inputClover(self):
		t = pygame.time.get_ticks()
		# inputs clover if t is a square, to make inclusion random
		if (self.randomize(t) and self.clover == None):
			self.clover = Clover(self.width,self.height,self.windSpeed,self.strength)
			self.clover.rect.center = (self.getLeafX(),0)
			self.clover.add(self.allSprites)

	# updates clover like a leaf
	def cloverAction(self):
		clover = self.clover
		cloverScore = 5 # score increments by 5 if clover put into basket
		if (self.isPlayerLeafCollision(clover,self.rangeOfBlow) == False):
			clover.blown = False
		clover.update()
		if (self.isLeafBasketCollision(clover)):
			self.score += cloverScore
			if (self.score > self.highScore): self.highScore = self.score
			clover.remove(self.allSprites)
			self.clover = None
		elif (clover.rect.centery >= self.height):
			clover.remove(self.allSprites)
			clover = None

	# increments time after 1 second
	def incrementTime(self):
		self.second = str(int(self.second)+1)
		if (int(self.second) == 60):
			self.minute = str(int(self.minute)+1)
			self.second=str("00") if (self.minute==0) else str("0")
			self.isGameOver = True
			self.recordScore()
		if (int(self.second) < 10):
			self.second = "0"+self.second

	# records score if score is higher than high score
	def recordScore(self):
		path = "highScoreArcade.txt"
		previousHighScore = int(Arcade.readFile(path))
		if (self.highScore > previousHighScore):
			os.remove(path)
			Arcade.writeFile(path,str(self.score))

	# returns True if player is in range to blow leaf
	def isPlayerLeafCollision(self,leaf,offset=None):
		if (offset == None): offset = self.offset
		player = self.player
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

	# returns True if a leaf hits basket
	def isLeafBasketCollision(self,leaf):
		(basketLeft,basketRight) = (self.basketLeft,self.basketRight)
		basketY = basketLeft.rect.top # y-coord of both baskets
		(leafX,leafY) = leaf.rect.center
		# basket at right's x-coords of its left and right sides
		(basketRightLeft,basketRightRight) = (basketRight.rect.left,
			basketRight.rect.right)
		# basket at left's x-coords of its left and right sides
		(basketLeftLeft,basketLeftRight) = (basketLeft.rect.left,
			basketLeft.rect.right)
		if (leafX < basketRightRight and leafX > basketRightLeft and
			basketY < leafY):
			return True
		elif (leafX < basketLeftRight and leafX > basketLeftLeft and
			basketY < leafY):
			return True
		return False

	# redraws canvas with all leaves and sprites
	def redrawAll(self):
		self.allSprites.draw(self.screen)
		self.displayTime()
		self.displayScore()
		if (self.isGameOver):
			self.displayGameOver()

	# draws time on screen
	def displayTime(self):
		if pygame.font:
			size = 30
			font = pygame.font.SysFont("baskerville",size)
			time = font.render("Time: %s:%s" % (self.minute,
				self.second), 1, (50,50,150))
			timePos = time.get_rect(centerx=100,centery=150)
			self.screen.blit(time,timePos)

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

	# returns high score from file
	def getHighScore(self):
		path = "highScoreArcade.txt"
		highScore = 0
		# create the highScore.txt, if it is not there
		if (not os.path.exists("highScoreArcade.txt")):
			Arcade.writeFile(path,"0")
		else:
			highScore = int(Arcade.readFile(path))
		# change score if score is higher than previous high score
		if (self.score > highScore):
			os.remove(path)
			Arcade.writeFile(path,str(self.score))
			highScore = self.score
		return highScore

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
