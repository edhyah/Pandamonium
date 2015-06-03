# sprites.py
# Edward Ahn + esahn + Section H

import pygame
import math
import random
from pygame.locals import *

class Leaf(pygame.sprite.Sprite):

	# loads image from file
	# method slightly modified from pygame.org
	# leaf 1: http://weekinthewoods.org/Bulletin%20Board/index.html
	# leaf 2: https://plus.google.com/102245072134375625336/reviews
	# leaf 3: http://www.wpclipart.com/small_icons/misc_4/leaf.png.html
	# leaf 4: http://www.abeka.com/ABekaOnline/MediaDescription.aspx?id=0000237302
	# leaf 5: http://dragon-story.wikia.com/wiki/Dragon_Summoning
	@staticmethod
	def loadImage(colorkey=None):
	    try:
	    	x = random.randint(1,5)
	    	image = pygame.image.load("leaf%d.png" % x)
	    except pygame.error, message:
	        print 'Cannot load image'
	        raise SystemExit, message
	    image = image.convert()
	    if colorkey is not None:
	        if colorkey is -1:
	            colorkey = image.get_at((0,0))
	        image.set_colorkey(colorkey, RLEACCEL)
	    image = pygame.transform.scale(image,(30,30))
	    return (image, image.get_rect())

	# creates instance of image
	def __init__(self, width, height, windSpeed, strength):
		super(Leaf,self).__init__()
		(self.image,self.rect) = Leaf.loadImage(-1)
		self.width = width
		self.height = height
		self.windX = windSpeed
		self.windY = 3
		self.gravity = 3 # speed due to gravity
		self.blown = False
		self.timeSinceBlow = 0
		self.angle = 0
		self.strength = strength # player's blowing strength, classic is 8
		self.orientation = 1 # 1, -1 if player blowing down or up respectively
		self.counter = 0 # counts time; used to limit blow to 1 seconds
		self.acceler = 0

	# updates leaf position
	def update(self):
		t = pygame.time.get_ticks()/100 # t in 1/10 second
		self.acceler += .1 * self.orientation
		randFactor = 1.5*random.random() + 0.5
		delta = (self.windX+self.windX*math.cos(t),self.windY*randFactor)
		if (pygame.time.get_ticks()-self.counter < 1000):
			if (self.blown):
				deltaX = (self.windX + self.strength*math.cos(self.angle)) + \
					self.windX*math.cos(t)
				deltaY = self.windY + self.gravity + self.orientation * \
					self.strength*math.sin(self.angle) + self.acceler
				delta = (deltaX,deltaY)
				(self.image,self.rect) = self.rotateImage()
		if (self.rect.bottom >= self.height):
			delta = (self.windX+self.windX*math.cos(t),self.windY*randFactor)
		self.rect.move_ip(delta)

	# rotates leaf
	def rotateImage(self):
		angle = 90
		image = pygame.transform.rotate(self.image,angle)
		rect = image.get_rect(center=self.rect.center)
		return (image,rect)

	# updates leaf attributes after player successfully blows leaf
	def blow(self,collision,counter):
		self.acceler = 0
		(self.orientation,self.angle) = collision
		self.blown = True
		self.counter = counter


class Player(pygame.sprite.Sprite):

	# loads image from file
	# method slightly modified from pygame.org
	@staticmethod
	def loadImage(colorkey=None):
	    try:
	    	imageLeft = pygame.image.load("pandaLeft.png")
	        imageRight = pygame.image.load("pandaRight.png")
	    except pygame.error, message:
	        print 'Cannot load image'
	        raise SystemExit, message
	    imageLeft = imageLeft.convert()
	    imageRight = imageRight.convert()
	    for image in [imageLeft,imageRight]:
		    if colorkey is not None:
		        if colorkey is -1:
		            colorkey = image.get_at((0,0))
		        image.set_colorkey(colorkey, RLEACCEL)
	    return imageLeft,imageRight

	# creates instance of image
	def __init__(self, width, height):
		super(Player,self).__init__()
		self.imageLeft,self.imageRight = Player.loadImage(-1) # sprite sheet
		(self.cRow,self.cCol) = (0,0) # current row, col in sprite sheet
		# width, height of each sprite in sprite sheet
		self.width = 45.75
		self.height = 102
		# number of rows, cols in sprite sheet
		(self.maxRows,self.maxCols) = (4,4)
		(self.sizeX,self.sizeY) = (70,140) # size of player on screen
		self.image = self.imageRight.subsurface((0,0,self.width,self.height))
		self.image = pygame.transform.scale(self.image,(self.sizeX,self.sizeY))
		self.rect = self.image.get_rect()
		self.rect.bottom = height-10
		self.windowWidth = width
		self.windowHeight = height
		self.speed = 5
		(self.movingLeft,self.movingRight) = (False,False)
		(self.facingLeft,self.facingRight) = (False,False)
		self.prevImage = None

	# updates player position
	def update(self):
		if (self.movingLeft):
			self.walk()
			self.rect.centerx -= self.speed
			if (self.rect.centerx < 0): self.rect.centerx = 0
		elif (self.movingRight):
			self.walk()
			self.rect.centerx += self.speed
			if (self.rect.centerx > self.windowWidth):
				self.rect.centerx = self.windowWidth

	# simulates player walking
	def walk(self):
		self.cCol += 1
		if (self.cCol >= self.maxCols):
			self.cRow += 1
			self.cCol = 0
		if (self.cRow >= self.maxRows):
			self.cRow = 0
			self.cCol = 0
		if (self.facingLeft):
			self.image = self.imageLeft.subsurface((self.cCol*self.width,
				self.cRow*self.height,self.width,self.height))
			self.image = pygame.transform.scale(self.image,
				(self.sizeX,self.sizeY))
		elif (self.facingRight):
			self.image = self.imageRight.subsurface((self.cCol*self.width,
				self.cRow*self.height,self.width,self.height))
			self.image = pygame.transform.scale(self.image,
				(self.sizeX,self.sizeY))
		# self.rect = self.image.get_rect()
		self.rect.bottom = self.windowHeight-10


class Basket(pygame.sprite.Sprite):

	# loads image from file
	# method slightly modified from pygame.org
	# http://thumbs4.ebaystatic.com/d/l225/m/mr1Br-qSO6TtGNzGmw1yDBw.jpg
	@staticmethod
	def loadImage(colorkey=None):
	    try:
	        image = pygame.image.load("basket.jpg")
	    except pygame.error, message:
	        print 'Cannot load image'
	        raise SystemExit, message
	    image = image.convert()
	    if colorkey is not None:
	        if colorkey is -1:
	            colorkey = image.get_at((0,0))
	        image.set_colorkey(colorkey, RLEACCEL)
	    image = pygame.transform.scale(image,(70,70))
	    return (image, image.get_rect())

	# creates instance of image
	def __init__(self, width, height):
		super(Basket,self).__init__()
		(self.image,self.rect) = Basket.loadImage(-1)
		self.width = width
		self.height = height
		self.rect.right = width - 10
		self.rect.bottom = height - 10


class Clover(Leaf):

	# loads image of clover from file
	# method slightly modified from pygame.org
	# http://www.clipartpanda.com/categories/clover-clip-art-black-and-white-free
	@staticmethod
	def loadImage(colorkey=None):
	    try:
	    	image = pygame.image.load("clover.png")
	    except pygame.error, message:
	        print 'Cannot load image'
	        raise SystemExit, message
	    image = image.convert()
	    if colorkey is not None:
	        if colorkey is -1:
	            colorkey = image.get_at((0,0))
	        image.set_colorkey(colorkey, RLEACCEL)
	    image = pygame.transform.scale(image,(30,30))
	    return (image, image.get_rect())

	# creates instance of clover sprite
	def __init__(self, width, height, windSpeed, strength):
		super(Clover,self).__init__(width,height,windSpeed,strength)
		(self.image,self.rect) = Clover.loadImage(-1)

