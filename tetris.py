#Tetris v0.4
#João Lucas Pires

#Fixed overlaping bug
#Need to find a way to rotate bottom and top Points along with the piece

import pygame, sys, random, time
from pygame.locals import *
from tetraminos import *
from Piece import *
from Config import *

window = pygame.display.set_mode(config['screensize'])
floorPieces = []

class Tetris():
	def __init__(self):
		self.game = None
		self.info = None

	#start(this)
	#Starts the game and contains the main sequence of operations
	def start(self):
		#Starts a pygame instance and blocks mouse movement as it's not required
		pygame.init()
		pygame.event.set_blocked(pygame.MOUSEMOTION)
		#Creates timer to control the frames
		pygame.time.set_timer(pygame.USEREVENT+1, config["timer_constant"])
		clock = pygame.time.Clock()
		#Starts the game
		piece = generatePiece()
		while True:
			eventHandler(piece)
			#Checks if piece is overlapping or on the bottom,
			#if so adds the piece to the resting list and generates a new one ; else drops one position the current one
			if (piece.overlaps(floorPieces) or piece.reachedFloor()):
					floorPieces.append(piece)
					piece = generatePiece()
			#else:
				#	piece.dropIt()
			#Refreshes the screen graphics with all the pieces and bottom line
			window.fill(colors["BLACK"])
			
			for aux in floorPieces:
				if (aux.yPos <= 10):
					sys.exit(0) #if a resting piece is on the top of the screen, exit
				aux.displayPiece(window, (aux.xPos, aux.yPos))
			piece.displayPiece(window, (piece.xPos, piece.yPos))
			
			pygame.draw.lines(window, colors["GREEN"],False,LINE_COORDINATES,4)
			pygame.display.update()
			#Ticks the timer (fps)
			clock.tick(30)	
			
#eventHandler(Piece)
#Handles the keypresses on the event queue in each iteration
def eventHandler(piece):
	#Controls the event queue
	for event in pygame.event.get():
		if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
			sys.exit(0)
		elif (event.type == KEYDOWN):
			if (event.key == K_SPACE):
				piece.flipPiece(window)
			elif (event.key == K_LEFT):
				piece.moveXaxis(True, window)
			elif (event.key == K_RIGHT):
				piece.moveXaxis(False, window)
			#debug modes
			elif (event.key == K_UP):
				piece.moveYaxis(True, window)
			elif (event.key == K_DOWN):
				piece.moveYaxis(False, window)
			elif (event.key == K_s):
				time.sleep(10) #Stops game for debug	

#generatePiece(void)
#Auxiliary function to construct the piece and display it on the top of the screen
def generatePiece():
	piece = Piece()
	#piece.debugPiece()
	piece.displayPiece(window, (0,0))
	pygame.display.update()
	return piece

#clearScreen(void)
#Auxiliary function to fill the screen with black
def clearScreen():
	window.fill(colors["BLACK"])
	pygame.display.update()

#debugFloorPieces(void)
#Auxiliary function to debug the list of pieces
def debugFloorPieces():
	print("Pieces on the bottom: " + str(floorPieces))

mainGame = Tetris()
mainGame.start()
