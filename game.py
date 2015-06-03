# game.py
# Edward Ahn + esahn + Section H

import pygame
from classic import Classic
from arcade import Arcade
from multiplayer import Multiplayer
from sprites import Leaf
import random
from pygameAnimationClass import PygameAnimationClass
from pygame.locals import *

class Game(PygameAnimationClass):

	# loads image of clover from file
	# method slightly modified from pygame.org
	# arrow left: http://findicons.com/icon/69058/left
	# arrow right: http://findicons.com/icon/69012/right
	# keys: http://inventwithpython.com/pygame/chapter4.html
	@staticmethod
	def loadImage(path,colorkey=None,sizeX=100,sizeY=100):
	    try:
	    	image = pygame.image.load(path)
	    except pygame.error, message:
	        print 'Cannot load image'
	        raise SystemExit, message
	    image = image.convert()
	    if colorkey is not None:
	        if colorkey is -1:
	            colorkey = image.get_at((0,0))
	        image.set_colorkey(colorkey, RLEACCEL)
	    image = pygame.transform.scale(image,(sizeX,sizeY))
	    return image

	# returns text needed for help screen
	@staticmethod
	def getMessages():
		return ["""\

You're a young panda.
It's a breezy autumn day.
You're bored.
What do you do?
""","""\

In this game, your main goal is to put
as many leaves into the basket(s) as possible.
""","""\
Sounds easy right?
Here's the catch. You can't use your paws.
Keep the leaf afloat while you take it to the basket
by blowing the leaf up with your mighty lungs.
If the leaf touches the ground, you must start over
with a new leaf.
""","""\
Use your left and right arrow keys to walk to the left
and right. Use your up arrow key to blow. If you're
playing with another cub on multiplayer, your friend can
press 'W' to blow, 'A' to move left, and 'D' to move right.
""","""\
More details:

Classic: get as many consecutive leaves
into the basket as possible
""","""\
More details:

Arcade: get as many leaves into the basket
as possible in under a minute
""","""\
More details:

Multiplayer: either with the CPU or with
another cub, compete to see who can get as
many leaves into the basket as possible
in under a minute
""","""\
More details:

To exit a mode, close the window,
which will take you back to the main menu.
Press 'r' to restart a mode anytime.
""","""\

A final hint:
Look out for four-leaf clovers!
"""]

	# constructs instance of game
	def __init__(self):
		super(Game,self).__init__()
		self.middle = self.width/2
		self.title = "PANDAMONIUM"
		# font sizes
		(self.titleSize,self.modeSize,self.miscSize) = (90,50,30)
		# x or y coords of buttons
		(self.yTitle,self.yClassic,self.yArcade) = (100,275,325)
		(self.yMulti,self.yMisc) = (375,450) # misc: height for help, settings
		(self.xHelp,self.xSet) = (225,675) # set is settings
		# sees if mouse is hovering over button
		(self.onHelp,self.onSet) = (False,False)
		(self.onClass,self.onMulti,self.onArcade) = (False,False,False)
		self.initHelpVariables()
		self.initSetVariables()

	# initializes variables needed to display help screen
	def initHelpVariables(self):
		self.viewHelp = False
		(self.currentPage,self.maxPages) = (0,7)
		(self.arrowLeftX,self.arrowRightX) = (115,self.width-200)
		self.arrowY = 400
		(self.onLeftArrow,self.onRightArrow,self.onHelpExit) = (False,
			False,False)

	# initializes variables needed to display settings screen
	def initSetVariables(self):
		self.onSetExit = False
		(self.onMusicOn,self.onMusicOff) = (False,False)
		self.viewSet = False
		self.arrowImage = None
		self.exitImage = None
		self.arrowLeft = None
		self.arrowRight = None
		self.cpuOn = True
		self.windSpeed = 1
		self.music = True
		self.strength = 8
		self.numOfLeaves = 5
		self.range = 1
		self.cpuLevel = 2 # 3 is easy, 2 is medium, 1 is hard

	# loads images needed for settings screen
	def loadSetImages(self):
		self.exitImage = Game.loadImage("leaf2.png",-1)

	# loads images needed for help screen
	def loadHelpImages(self):
		self.arrowImage = Game.loadImage("leaf1.png",-1)
		self.arrowLeft = Game.loadImage("arrowLeft.png",-1)
		self.arrowRight = Game.loadImage("arrowRight.png",-1)
		self.clover = Game.loadImage("clover.png",-1)
		self.keys = Game.loadImage("keys.png",-1,265,91)
		self.basket = Game.loadImage("basket.jpg",-1)
		if (self.exitImage == None):
			self.loadSetImages()

	# plays background music
	# music source: Two Dots IOS game theme song
	# https://www.youtube.com/watch?v=PeDLgq23jfU
	def playMusic(self):
		pygame.mixer.music.stop()
		if (not self.music): return
		try:
			pygame.mixer.music.load("theme1.ogg")
			pygame.mixer.music.play(-1)
		except: return

	# animates leaves falling on the menu screen
	def initAnimation(self):
		self.leaves = self.getLeaves(15)
		self.sprites = pygame.sprite.RenderPlain(tuple(self.leaves))

	# returns background of game
	def setBackground(self):
		background = pygame.image.load("titleBg.jpg").convert()
		background = pygame.transform.scale(background,(900,500))
		return background

	# responds to mouse presses by player
	def onMousePressed(self, event):
		if (self.onHelp):
			self.onHelp = False
			self.viewHelp = True
		elif (self.viewHelp): self.onMousePressedHelp()
		elif (self.onSet):
			self.onSet = False
			self.viewSet = True
		elif (self.viewSet): self.onMousePressedSet()
		elif (self.onClass):
			self.onClass = False
			Classic(self.windSpeed,self.music,self.strength,self.range).run()
		elif (self.onMulti):
			self.onMulti = False
			Multiplayer(self.windSpeed,self.music,self.cpuOn,self.strength,
				self.numOfLeaves,self.range,self.cpuLevel).run()
		elif (self.onArcade):
			self.onArcade = False
			Arcade(self.windSpeed,self.music,self.strength,
				self.numOfLeaves,self.range).run()

	# responds to mouse presses by player on help screen
	def onMousePressedHelp(self):
		if (self.onLeftArrow and self.currentPage > 0):
			self.currentPage -= 1
		elif (self.onRightArrow and self.currentPage <= self.maxPages):
			self.currentPage += 1
		elif (self.onHelpExit):
			self.viewHelp = False
			self.currentPage = 0
			(self.onLeftArrow,self.onRightArrow,self.onHelpExit) = (False,
				False,False)

	# responds to mouse presses by player on settings screen
	def onMousePressedSet(self):
		(x,y) = pygame.mouse.get_pos()
		if (self.onSetExit):
			self.viewSet = False
		self.onMousePressedMusic(x,y)
		self.onMousePressedCpu(x,y)
		self.onMousePressedPlusMinus(x,y)
		self.onMousePressedCpuLevel(x,y)

	# if press on, background music will play; vice versa
	def onMousePressedMusic(self,x,y):
		# (x,y) = pygame.mouse.get_pos()
		musicOnX = 327
		musicOffX = 378
		musicY = 372
		r = 25
		if (y >= musicY-r and y <= musicY+r):
			if (x >= musicOnX-r and x <= musicOnX+r):
				self.music = True
				self.playMusic()
			elif (x >= musicOffX-r and x <= musicOffX+r):
				self.music = False
				self.playMusic()

	# if press on, cpu in multiplayer will activate; vice versa
	def onMousePressedCpu(self,x,y):
		# (x,y) = pygame.mouse.get_pos()
		cpuModeOnX = 689
		cpuModeOffX = 740
		cpuModeY = 191
		r = 25
		if (y >= cpuModeY-r and y <= cpuModeY+r):
			if (x >= cpuModeOnX-r and x <= cpuModeOnX+r):
				self.cpuOn = True
			elif (x >= cpuModeOffX-r and x <= cpuModeOffX+r):
				self.cpuOn = False

	# changes values after player presses plus/minus icons
	def onMousePressedPlusMinus(self,x,y):
		(w,h) = (30,22) # width, height of each plus/minus icon
		# top-left corners of each plus minus image
		plusMinusCoords = [(320,194),(320,249),(320,304),(765,338)]
		# (x,y) = pygame.mouse.get_pos()
		self.activatePlusSigns(x,y,w,h,plusMinusCoords)
		self.activateMinusSigns(x,y,w,h,plusMinusCoords)

	# allows plus signs to work on settings
	def activatePlusSigns(self,x,y,w,h,plusMinusCoords):
		# plus signs for wind speed, blow strength, blow range
		if (x>=plusMinusCoords[0][0] and x<=plusMinusCoords[0][0]+w):
			# wind speed
			if (y>=plusMinusCoords[0][1] and y<=plusMinusCoords[0][1]+h and
				self.windSpeed<10):
				self.windSpeed += 1
			# blow strength
			elif (y>plusMinusCoords[1][1] and y<=plusMinusCoords[1][1]+h and
				self.strength<20):
				self.strength += 1
			# blow range
			elif (y>plusMinusCoords[2][1] and y<=plusMinusCoords[2][1]+h and
				self.range<5):
				self.range += 1
		# plus sign for number of leaves
		elif (x>=plusMinusCoords[3][0] and x<=plusMinusCoords[3][0]+w and
			y>plusMinusCoords[3][1] and y<=plusMinusCoords[3][1]+h and
			self.numOfLeaves<20):
			self.numOfLeaves += 1

	# allows minus signs to work on settings
	def activateMinusSigns(self,x,y,w,h,plusMinusCoords):
		# minus signs for wind speed, blow strength, blow range
		if (x>=plusMinusCoords[0][0]+w and x<=plusMinusCoords[0][0]+2*w):
			# wind speed
			if (y>=plusMinusCoords[0][1] and y<=plusMinusCoords[0][1]+h and
				self.windSpeed>0):
				self.windSpeed -= 1
			# blow strength
			elif (y>plusMinusCoords[1][1] and y<=plusMinusCoords[1][1]+h
				and self.strength>1):
				self.strength -= 1
			# blow range
			elif (y>plusMinusCoords[2][1] and y<=plusMinusCoords[2][1]+h
				and self.range>1):
				self.range -= 1
		# minus sign for number of leaves
		elif (x>=plusMinusCoords[3][0]+w and x<=plusMinusCoords[3][0]+2*w and
			y>plusMinusCoords[3][1] and y<=plusMinusCoords[3][1]+h and
			self.numOfLeaves>1):
			self.numOfLeaves -= 1

	# allows player to adjust level of cpu difficulty
	def onMousePressedCpuLevel(self,x,y):
		(easyX,easyY,easyW,easyH) = (617,247,70,50)
		(medX,medY,medW,medH) = (692,247,115,50)
		(hardX,hardY,hardW,hardH) = (807,246,80,50)
		if (x>=easyX and x<=easyX+easyW and y>=easyY and y<=easyY+easyH):
			self.cpuLevel = 3
		elif (x>=medX and x<=medX+medW and y>=medY and y<=medY+medH):
			self.cpuLevel = 2
		elif (x>=hardX and x<=hardX+hardW and y>=hardY and y<=hardY+hardH):
			self.cpuLevel = 1

	# highlights text if mouse moves over them
	def onMouseMotion(self, event):
		(x,y) = (event.pos)
		# range of values mouse needs to be in to press button
		(helpXMin,helpXMax) = (200,250)
		(setXMin,setXMax) = (625,725)
		(miscYMin,miscYMax) = (425,475)
		(modeXMin,modeXMax) = (300,600)
		(classYMin,classYMax) = (250,300)
		(arcadeYMin,arcadeYMax) = (300,350)
		(multiYMin,multiYMax) = (350,400)
		if (self.viewHelp): self.onMouseMotionHelp()
		elif (self.viewSet): self.onMouseMotionSet()
		elif (y>=miscYMin and y<=miscYMax):
			if (x>=helpXMin and x<=helpXMax): self.onHelp = True
			elif (x>=setXMin and x<=setXMax): self.onSet = True
			else: (self.onHelp,self.onSet) = (False,False)
		elif (x>=modeXMin and x<=modeXMax):
			if (y>=classYMin and y<=classYMax):
				(self.onClass,self.onMulti,self.onArcade) = (True,False,False)
			elif (y>=multiYMin and y<=multiYMax):
				(self.onClass,self.onMulti,self.onArcade) = (False,True,False)
			elif (y>=arcadeYMin and y<=arcadeYMax):
				(self.onClass,self.onMulti,self.onArcade) = (False,False,True)
			else:
				(self.onClass,self.onMulti,self.onArcade) = (False,False,False)
		else:
			(self.onHelp,self.onSet) = (False,False)
			(self.onClass,self.onMulti,self.onArcade) = (False,False,False)

	# highlights arrows or exit button in help screen
	def onMouseMotionHelp(self):
		(x,y) = pygame.mouse.get_pos()
		size = 100 # size of arrow
		textSize = 50
		if (x >= self.arrowLeftX and x<= self.arrowLeftX+size and
			y >= self.arrowY and y<= self.arrowY+size and self.currentPage!=0):
			self.onLeftArrow = True
		elif (x >= self.arrowRightX and x <= self.arrowRightX+size and
			y >= self.arrowY and y<= self.arrowY+size and
			self.currentPage<=self.maxPages):
			self.onRightArrow = True
		elif (x >= self.width/2-textSize and x <= self.width/2+textSize and
			y >= self.arrowY+textSize/2 and y <= self.arrowY+3*textSize/2):
			self.onHelpExit = True
		else:
			(self.onLeftArrow,self.onRightArrow,self.onHelpExit) = (False,
				False,False)

	# highlights +'s and -'s on settings screen
	def onMouseMotionSet(self):
		(x,y) = pygame.mouse.get_pos()
		exitSize = 50
		if (x >= self.width/2-exitSize and x <= self.width/2+exitSize and
			y >= self.arrowY+exitSize/2 and y <= self.arrowY+3*exitSize/2):
			self.onSetExit = True
		else:
			self.onSetExit = False

	# animates leaves as timer is fired
	def onTimerFired(self):
		for leaf in self.leaves:
			leaf.update()
			if (leaf.rect.top >= self.height):
				(leaf.rect.top,leaf.rect.centerx) = (0,
					random.randint(0,self.width))

	# returns group of n number of leaves
	def getLeaves(self,n):
		leaves = []
		for x in xrange(n):
			leaf = Leaf(self.width,self.height,self.windSpeed,self.strength)
			leaf.windX = random.randint(0,1)
			# prevents leaf from going directly into basket without any blows
			leaf.rect.centerx = random.randint(0,self.width)
			leaf.rect.centery = random.randint(0,self.height)
			leaves.append(leaf)
		return leaves

	# redraws canvas after updates
	def redrawAll(self):
		self.sprites.draw(self.screen)
		screen = self.screen
		middle = self.width/2
		if (self.viewHelp):
			self.drawHelp()
			return
		elif (self.viewSet):
			self.drawSet()
			return
		if pygame.font:
			self.drawText("%s" % (self.title),
				self.titleSize,middle,self.yTitle,False)
			self.drawText("Classic",self.modeSize,middle,self.yClassic,
				self.onClass)
			self.drawText("Multiplayer",self.modeSize,middle,self.yMulti,
				self.onMulti)
			self.drawText("Arcade",self.modeSize,middle,self.yArcade,
				self.onArcade)
			self.drawText("Help",self.miscSize,self.xHelp,self.yMisc,
				self.onHelp)
			self.drawText("Settings",self.miscSize,self.xSet,self.yMisc,
				self.onSet)

	# draws buttons; if on==True, it means mouse is hovering over that button
	def drawText(self, text, size, x, y, on):
		if pygame.font:
			color = (204,102,0)
			if (on == True):
				color = (102,51,0)
			font = pygame.font.SysFont("baskerville",size)
			text = font.render(text,1,color)
			textPos = text.get_rect(centerx=x,centery=y)
		self.screen.blit(text,textPos)

	# draws help screen
	def drawHelp(self):
		if (self.arrowImage == None): self.loadHelpImages() # loads images once
		# draw mouse motion events
		if (self.onLeftArrow and self.currentPage!=0):
			self.screen.blit(self.arrowImage,(self.arrowLeftX,self.arrowY))
		elif (self.onRightArrow and self.currentPage<=self.maxPages):
			self.screen.blit(self.arrowImage,(self.arrowRightX,self.arrowY))
		elif (self.onHelpExit):
			self.screen.blit(self.exitImage,(self.width/2-50,self.arrowY))
		# draw actual icons
		if (self.currentPage!=0):
			self.screen.blit(self.arrowLeft,(self.arrowLeftX,self.arrowY))
		if (self.currentPage<=self.maxPages):
			self.screen.blit(self.arrowRight,(self.arrowRightX,self.arrowY))
		self.drawText("EXIT",30,self.width/2,self.arrowY+50,True)
		# display help text
		messages = Game.getMessages()
		self.displayHelpMessages(messages[self.currentPage])
		# display images that go with text on some pages
		if (self.currentPage == 1):
			self.screen.blit(self.basket,(self.width/2-50,285)) 
		elif (self.currentPage == 3):
			self.screen.blit(self.keys,(self.width/2-133,310))
		elif (self.currentPage == 8):
			self.screen.blit(self.clover,(self.width/2-50,275))

	# draws text on help screens
	def displayHelpMessages(self,message):
		size = 30
		yInitial = 100 # y coord of first line of text
		spacing = increment = 40
		if pygame.font:
			color = (204,102,0)
			font = pygame.font.SysFont("baskerville",size)
			for line in message.splitlines():
				text = font.render(line,1,color)
				textPos = text.get_rect(centerx=self.width/2,
					centery= yInitial + spacing + 5)
				self.screen.blit(text,textPos)
				spacing += increment

	# draws settings screen
	def drawSet(self):
		# draw mouse motion events
		if (self.onSetExit):
			if (self.exitImage == None): self.loadSetImages()
			self.screen.blit(self.exitImage,(self.width/2-50,self.arrowY))
		# draw exit sign
		self.drawText("EXIT",30,self.width/2,self.arrowY+50,True)
		# draw actual settings
		self.drawSetTitles()
		self.drawSetText()

	# draws "Setting", "General Settings", "Advanced Settings" onto screen
	def drawSetTitles(self):
		sizeMainTitle = 60
		sizeSubTitle = 40
		(mainY,subY) = (70,130)
		color = (204,102,0)
		if pygame.font:
			# create fonts
			mainTitleFont = pygame.font.SysFont("baskerville",sizeMainTitle)
			subTitleFont = pygame.font.SysFont("baskerville",sizeSubTitle)
			# create titles
			mainTitle = mainTitleFont.render("Settings",1,color)
			subTitle1 = subTitleFont.render("General",1,color)
			subTitle2 = subTitleFont.render("Advanced",1,color)
			# position titles
			mainTitlePos = mainTitle.get_rect(centerx=self.width/2,
				centery=mainY)
			subTitle1Pos = subTitle1.get_rect(centerx=self.width/4,
				centery=subY)
			subTitle2Pos = subTitle2.get_rect(centerx=3*self.width/4,
				centery=subY)
			# display titles
			self.screen.blit(mainTitle,mainTitlePos)
			self.screen.blit(subTitle1,subTitle1Pos)
			self.screen.blit(subTitle2,subTitle2Pos)

	# draws text on settings screen by calling self.displaySetText(text,textX)
	def drawSetText(self):
		genInc = 55
		genTextX = self.width/4
		genText = """\
Wind Speed: %d m/s               
Blow Strength: %d           
Blow Range: %d m         
Background Music:   on/off
""" % (self.windSpeed,self.strength,self.range)
		advInc = 40
		advTextX = 3*self.width/4
		advText = """\
CPU:   on/off
(multiplayer)
CPU Level:   easy/medium/hard
(multiplayer)
Number of Leaves: %d                     
(arcade/multiplayer)
""" % (self.numOfLeaves)
		self.displaySetText(genText,genTextX,genInc)
		self.displaySetText(advText,advTextX,advInc)
		self.drawSelectors()

	# draws circles that indicate off/on, + - signs that can change attributes
	def drawSelectors(self):
		self.drawOnOffSelectors()
		self.drawPlusMinus()
		self.drawCpuLevelSelectors()

	# draws plus/minus icons for player to manipulate
	# http://www.clker.com/clipart-plus-and-minus.html
	def drawPlusMinus(self):
		plusMinus = Game.loadImage("plusMinus.png",-1,60,22)
		plusMinusCoords = [(320,194),(320,249),(320,304),(765,338)]
		for coord in plusMinusCoords:
			self.screen.blit(plusMinus,coord)

	# draws circles on on/off selectors in settings
	def drawOnOffSelectors(self):
		red = (255,0,0)
		musicOn = (327,372)
		musicOff = (378,372)
		cpuModeOn = (689,191)
		cpuModeOff = (740,191)
		(r,w) = (25,3) # radius, width
		if (self.music):
			pygame.draw.circle(self.screen,red,musicOn,r,w)
		else:
			pygame.draw.circle(self.screen,red,musicOff,r,w)
		if (self.cpuOn):
			pygame.draw.circle(self.screen,red,cpuModeOn,r,w)
		else:
			pygame.draw.circle(self.screen,red,cpuModeOff,r,w)

	# draws ellipses that indicate which cpu difficulty is on
	def drawCpuLevelSelectors(self):
		red = (255,0,0)
		(easy,med,hard) = (3,2,1)
		easyXYWH = (617,247,70,50)
		medXYWH = (692,247,115,50)
		hardXYWH = (807,246,80,50)
		w = 3 # line width
		if (self.cpuLevel == easy):
			pygame.draw.ellipse(self.screen,red,easyXYWH,w)
		elif (self.cpuLevel == med):
			pygame.draw.ellipse(self.screen,red,medXYWH,w)
		elif (self.cpuLevel == hard):
			pygame.draw.ellipse(self.screen,red,hardXYWH,w)

	# draws text at given x value
	def displaySetText(self,text,textX,increment):
		spacing = increment
		size = 25
		yInitial = 150 # y coord of first option
		if pygame.font:
			color = (102,51,0)
			font = pygame.font.SysFont("baskerville",size)
			for line in text.splitlines():
				option = font.render(line,1,color)
				optionPos = option.get_rect(centerx=textX,
					centery=yInitial+spacing)
				self.screen.blit(option,optionPos)
				spacing += increment

game = Game()
game.run()