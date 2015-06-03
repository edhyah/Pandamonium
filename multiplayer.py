# multiplayer.py
# Edward Ahn + esahn + Section H

import pygame
from pygame.locals import *
from arcade import Arcade
from sprites import *
import os

class Multiplayer(Arcade):

	# constructs instance of multiplayer mode
	def __init__(self, windSpeed, music, cpuOn, strength, n, rangeFactor,
		cpuLevel):
		super(Multiplayer,self).__init__(windSpeed,music,strength,
			n,rangeFactor)
		self.windSpeed = windSpeed
		self.strength = strength
		self.cpuOn = cpuOn # AI mode is off
		self.title = "PANDAMONIUM"
		self.numOfLeaves = n
		self.rangeFactor = rangeFactor
		self.cpuLevel = cpuLevel

	# initializes important variables
	def initAnimation(self):
		if (self.cpuOn): self.closestLeaf = None
		self.leaves = self.getLeaves(self.numOfLeaves)
		for leaf in self.leaves: leaf.windX = 0
		self.player1 = Player(self.width,self.height)
		self.player1.rect.centerx = 10
		self.player2 = Player(self.width,self.height)
		self.player2.rect.centerx = self.width - 10
		self.basket = Basket(self.width,self.height)
		self.basket.rect.centerx = self.width/2
		self.allSprites = self.getSprites()
		self.isGameOver = False
		# range where player can blow a leaf
		self.offset = max(self.player1.rect.size)
		# range where player can keep blowing to
		self.rangeOfBlow = 1.2*self.offset*self.rangeFactor
		# counter limits player's blow to 1 second
		self.counterP1 = 0
		self.counterP2 = 0
		# number of leaves put into the basket
		(self.p1Score,self.p2Score) = (0,0)
		(self.minute,self.second) = ("0","00")
		self.previousTicks = pygame.time.get_ticks()
		self.clover = None

	# initializes only some variables important to restarting game
	def partialInit(self):
		self.closestLeaf = None
		self.leaves = self.getLeaves(self.numOfLeaves)
		self.player1 = Player(self.width,self.height)
		self.player1.rect.centerx = 10
		self.player2 = Player(self.width,self.height)
		self.player2.rect.centerx = self.width - 10
		(self.p1Score,self.p2Score) = (0,0)
		self.allSprites = self.getSprites()
		self.isGameOver = False
		(self.minute,self.second) = ("0","00")
		self.previousTicks = pygame.time.get_ticks()
		self.clover = None

	# returns random leaf center that isn't above any of the baskets
	def getLeafX(self):
		offset = 100
		bound = 20 # bound from right and left sides of screen
		x = random.randint(bound,self.width/2-offset)
		y = random.randint(self.width/2+offset,self.width-bound)
		return random.choice([x,y])

	# returns group of sprites
	def getSprites(self):
		group = []
		group += [self.player1,self.player2,self.basket]
		group += self.leaves
		group = tuple(group)
		return pygame.sprite.RenderPlain(group)

	# responds to key presses made by players
	def onKeyPressed(self, event):
		if (not self.cpuOn and event.key in
			[pygame.K_w,pygame.K_a,pygame.K_d]):
			self.onKeyPressedForP1(event)
		elif (event.key in [pygame.K_UP,pygame.K_LEFT,pygame.K_RIGHT]):
			self.onKeyPressedForP2(event)
		elif (event.key == pygame.K_r):
			self.partialInit()

	# responds to key presses made by player 1
	def onKeyPressedForP1(self, event):
		self.counterP1 = pygame.time.get_ticks()
		if (event.key == pygame.K_w):
			for leaf in self.leaves:
				collision = self.isPlayerLeafCollision(self.player1,leaf)
				if (collision != False):
					leaf.blow(collision,self.counterP1)
			if (self.clover != None):
				collision = self.isPlayerLeafCollision(self.player1,
					self.clover)
				if (collision != False):
					self.clover.blow(collision,self.counterP1)
		elif (event.key == pygame.K_a):
			self.player1.movingLeft = True
			(self.player1.facingRight,self.player1.facingLeft) = (False,True)
		elif (event.key == pygame.K_d):
			self.player1.movingRight = True
			(self.player1.facingRight,self.player1.facingLeft) = (True,False)

	# responds to key presses made by player 2
	def onKeyPressedForP2(self, event):
		self.counterP2 = pygame.time.get_ticks()
		if (event.key == pygame.K_UP):
			for leaf in self.leaves:
				collision = self.isPlayerLeafCollision(self.player2,leaf)
				if (collision != False):
					leaf.blow(collision,self.counterP2)
			if (self.clover != None):
				collision = self.isPlayerLeafCollision(self.player2,
					self.clover)
				if (collision != False):
					self.clover.blow(collision,self.counterP2)
		elif (event.key == pygame.K_LEFT):
			self.player2.movingLeft = True
			(self.player2.facingRight,self.player2.facingLeft) = (False,True)
		elif (event.key == pygame.K_RIGHT):
			self.player2.movingRight = True
			(self.player2.facingRight,self.player2.facingLeft) = (True,False)

	# responds to key releases made by players
	def onKeyReleased(self, event):
		if (not self.cpuOn and event.key in
			[pygame.K_w,pygame.K_a,pygame.K_d]):
			self.onKeyReleasedForP1(event)
		elif (event.key in [pygame.K_UP,pygame.K_LEFT,pygame.K_RIGHT]):
			self.onKeyReleasedForP2(event)

	# responds to key releases by player 1
	def onKeyReleasedForP1(self, event):
		if (event.key == pygame.K_w):
			for leaf in self.leaves:
				leaf.blown = False
			if (self.clover != None): self.clover.blown = False
			self.counterP1 = 0
		elif (event.key == pygame.K_a):
			self.player1.movingLeft = False
		elif (event.key == pygame.K_d):
			self.player1.movingRight = False

	# responds to key releases by player 2
	def onKeyReleasedForP2(self, event):
		if (event.key == pygame.K_UP):
			for leaf in self.leaves:
				leaf.blown = False
			if (self.clover != None): self.clover.blown = False
			self.counterP2 = 0
		elif (event.key == pygame.K_LEFT):
			self.player2.movingLeft = False
		elif (event.key == pygame.K_RIGHT):
			self.player2.movingRight = False

	# increments time after 1 second
	def incrementTime(self):
		self.second = str(int(self.second)+1)
		if (int(self.second) == 60):
			self.minute = str(int(self.minute)+1)
			self.second=str("00") if (self.minute==0) else str("0")
			self.isGameOver = True
		if (int(self.second) < 10):
			self.second = "0"+self.second

	# responds to timer firing (creates leaves)
	def onTimerFired(self):
		if (self.isGameOver): return
		self.inputClover()
		t = pygame.time.get_ticks() - self.previousTicks
		if (int(self.second) != t/1000 and int(self.minute) == 0):
			self.incrementTime()
		if (self.cpuOn): self.cpuAction()
		for leaf in self.leaves:
			if (self.isPlayerLeafCollision(self.player1,
				leaf,self.rangeOfBlow) == False and self.isPlayerLeafCollision(
				self.player2,leaf,self.rangeOfBlow) == False):
				leaf.blown = False
			leaf.update()
			if (self.isLeafBasketCollision(leaf)):
				if (leaf.angle > 1.57): self.p2Score += 1
				else: self.p1Score += 1
				(leaf.rect.centery,leaf.rect.centerx) = (0,self.getLeafX())
			if (leaf.rect.top >= self.height):
				(leaf.rect.top,leaf.rect.centerx) = (0,self.getLeafX())
		if (self.clover != None): self.cloverAction()
		if (self.player1.rect.centerx >= self.width/2):
			self.player1.rect.centerx = self.width/2
		if (self.player2.rect.centerx <= self.width/2):
			self.player2.rect.centerx = self.width/2
		self.player1.update()
		self.player2.update()

	# updates clover like a leaf
	def cloverAction(self):
		clover = self.clover
		cloverScore = 5 # score increments by 5 if clover put into basket
		if (self.isPlayerLeafCollision(self.player1,clover,
			self.rangeOfBlow) == False and self.isPlayerLeafCollision(
			self.player2,clover,self.rangeOfBlow) == False):
			clover.blown = False
		clover.update()
		if (self.isLeafBasketCollision(clover)):
			if (clover.angle > 1.57): self.p2Score += cloverScore
			else: self.p1Score += cloverScore
			clover.remove(self.allSprites)
			self.clover = None
		elif (clover.rect.centery >= self.height):
			clover.remove(self.allSprites)
			self.clover = None

	# returns True if player is in range to blow leaf
	# modified from super class's function
	def isPlayerLeafCollision(self,player,leaf,offset=None):
		if (offset == None): offset = self.offset
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
		basket = self.basket
		basketY = basket.rect.top # y-coord of both baskets
		(leafX,leafY) = leaf.rect.center
		(basketLeft,basketRight) = (basket.rect.left,basket.rect.right)
		if (leafX < basketRight and leafX > basketLeft and basketY < leafY):
			return True
		return False

	# computes distance from leaf to cpu
	def distLeafCpu(self, leaf):
		xDist = self.player1.rect.centerx - leaf.rect.centerx
		yDist = self.player1.rect.centery - leaf.rect.centery
		return (xDist**2 + yDist**2)**0.5

	# controls cpu (artificial intelligence)
	def cpuAction(self):
		# target the leaf, but target clover if there is one
		if (self.clover != None and self.clover.rect.centerx < self.width/2 and
			self.clover.rect.centery < self.height/2):
			self.closestLeaf = self.clover
		elif (self.closestLeaf == None or
			self.closestLeaf.rect.centerx >= self.width/2 or
			self.closestLeaf.rect.centerx == 0):
			self.findClosestLeafToCpu()
		leaf = self.closestLeaf
		if (leaf == None):
			self.player1.movingLeft = False
			self.player1.movingRight = False
			return
		# if leaf not in range, move to it
		if (self.isPlayerLeafCollision(self.player1,leaf) == False):
			self.moveToLeafCpu(leaf)
		# if leaf in range, blow it
		else:
			delta = 30*self.cpuLevel
			# if leaf is not within delta px of basket, blow
			if (leaf.rect.centerx < self.basket.rect.centerx-delta):
				self.blowLeafCpu(leaf)
			# blows other leaves that may be in the way
			for leaf in self.leaves:
				if (leaf != self.closestLeaf and self.isPlayerLeafCollision(
					self.player1,leaf)): self.blowLeafCpu(leaf)

	# returns leaf closest to cpu
	def findClosestLeafToCpu(self):
		dist = self.height/2 # min height needed for cpu to get to it in time
		for leaf in self.leaves:
			if (self.closestLeaf == None):
				self.closestLeaf = leaf
			elif (leaf.rect.centerx < self.width/2 and
				self.distLeafCpu(leaf) < self.distLeafCpu(self.closestLeaf)
				and leaf.rect.centery <= dist):
				self.closestLeaf = leaf
		if (self.closestLeaf.rect.centerx >= self.width/2):
			self.closestLeaf = None

	# moves cpu to closest leaf
	def moveToLeafCpu(self, leaf):
		coord = leaf.rect.centerx
		pos = self.player1.rect.centerx
		# if leaf is to the left of cpu, walk left
		if (pos > coord-self.offset/4 and pos!=0 and coord!=0):
			self.player1.movingLeft = True
			self.player1.movingRight = False
			(self.player1.facingRight,self.player1.facingLeft) = (False,True)
		# if leaf is in range but too high, don't move the cpu
		elif (pos<coord and coord-self.offset/2<pos and pos!=0 and coord!=0):
			self.player1.movingRight = False
			self.player1.movingLeft = False
			(self.player1.facingRight,self.player1.facingLeft) = (True,False)
		else:
			self.player1.movingRight = True
			self.player1.movingLeft = False
			(self.player1.facingRight,self.player1.facingLeft) = (True,False)
		self.player1.update()

	# cpu blows closest leaf if it is in range
	def blowLeafCpu(self, leaf):
		collision = self.isPlayerLeafCollision(self.player1,leaf)
		leaf.blow(collision,pygame.time.get_ticks())

	# draws score on screen
	def displayScore(self):
		if (self.cpuOn):
			name1 = "CPU"
			name2 = "Your"
		else:
			name1 = "Player 2"
			name2 = "Player 1"
		if pygame.font:
			size = 20
			font = pygame.font.SysFont("baskerville",size)
			score1 = font.render("%s Score: %d" % (name1,self.p1Score),
				1, (0,0,0))
			score1Pos = score1.get_rect(centerx=780,centery=150)
			score2 = font.render("%s Score: %d" % (name2,self.p2Score),
				1, (0,0,0))
			score2Pos = score2.get_rect(centerx=780,centery=120)
			self.screen.blit(score1,score1Pos)
			self.screen.blit(score2,score2Pos)

	# displays game over screen
	def displayGameOver(self):
		pygame.draw.rect(self.screen,(102,51,0),(150,200,600,100))
		msg = ""
		diff = self.p1Score - self.p2Score
		if (diff < 0):
			if (self.cpuOn): msg = "You win by %d point(s)!" % abs(diff)
			else: msg = "Player 1 wins by %d point(s)!" % abs(diff)
		elif (diff > 0):
			if (self.cpuOn): msg = "The CPU wins by %d point(s)!" % diff
			else: msg = "Player 2 wins by %d point(s)!" % diff
		else: msg = "It's a tie!"
		if pygame.font:
			size = 36
			font = pygame.font.SysFont("baskerville", size)
			text1 = font.render(msg,1,(204,102,0))
			text1Pos = text1.get_rect(centerx=self.width/2,centery=
				self.height/2-25)
			text2 = font.render("Press 'r' to play another game!",1,(204,102,0))
			text2Pos = text2.get_rect(centerx=self.width/2,
				centery=self.height/2+25)
			self.screen.blit(text1,text1Pos)
			self.screen.blit(text2,text2Pos)
