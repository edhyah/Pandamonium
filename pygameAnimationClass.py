# pygameAnimationClass.py
# Edward Ahn + esahn + Section H

import pygame

class PygameAnimationClass(object):
	def onMousePressed(self, event): pass
	def onKeyPressed(self, event): pass
	def onKeyReleased(self, event): pass
	def onMouseMotion(self, event): pass
	def onTimerFired(self): pass
	def redrawAll(self): pass
	def initAnimation(self): pass
	def setBackground(self): pass
	def playMusic(self): pass
	def playTheme(self): pass

	def __init__(self, width=900, height=500):
	    self.width = width
	    self.height = height
	    self.size = (self.width,self.height)
	    self.done = False
	    self.clock = pygame.time.Clock()
	    self.isRunning = True
	    self.title = ""

	def onMousePressedWrapper(self, event):
		if (not self.isRunning): return
		self.onMousePressed(event)
		self.redrawAll()
		pygame.display.flip()

	def onKeyPressedWrapper(self, event):
		if (not self.isRunning): return
		self.onKeyPressed(event)
		self.redrawAll()
		pygame.display.flip()

	def onKeyReleasedWrapper(self, event):
		if (not self.isRunning): return
		self.onKeyReleased(event)
		self.redrawAll()
		pygame.display.flip()

	def onMouseMotionWrapper(self, event):
		if (not self.isRunning): return
		self.onMouseMotion(event)
		self.redrawAll()
		pygame.display.flip()

	def onTimerFiredWrapper(self):
		if (not self.isRunning): return
		self.onTimerFired()
		self.redrawAll()
		pygame.display.flip()

	def run(self):
		pygame.mixer.pre_init(44100, -16, 2, 2048)
		pygame.init()
		pygame.font.init()
		self.screen = pygame.display.set_mode(self.size)
		self.initAnimation()
		background = self.setBackground()
		pygame.display.set_caption(self.title)
		self.playMusic()
		while (not self.done):
			if (background == None):
				self.screen.fill((0,0,0))
			else:
				self.screen.blit(background, [0, 0])
			events = pygame.event.get()
			for event in events:
				if (event.type == pygame.QUIT):
					self.isRunning = False
					self.done = True
					self.playTheme()
				elif (event.type == pygame.KEYDOWN):
					self.onKeyPressedWrapper(event)
				elif (event.type == pygame.KEYUP):
					self.onKeyReleasedWrapper(event)
				elif (event.type == pygame.MOUSEBUTTONDOWN):
					self.onMousePressedWrapper(event)
				elif (event.type == pygame.MOUSEMOTION):
					self.onMouseMotionWrapper(event)
			self.onTimerFiredWrapper()
			self.clock.tick(60)

# PygameAnimationClass().run()