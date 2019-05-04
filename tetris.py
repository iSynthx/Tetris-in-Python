#Tetris v0.2
#Python 3

import pygame, sys, random, time
from pygame.locals import *
screenSize = (800, 600)
window = pygame.display.set_mode(screenSize)
floorPieces = []
pieces = [
# ---- 0
	[[1,1,1,1]],
#   - 1
# ---
	[[0,0,1],
	[1,1,1]
	],
#  -- 2
# --
	[[0,1,1],
	[1,1,0]
	],
# --- 3
#  -
	[[1,1,1],
	[0,1,0]
	],
# -- 4
# --
	[[1,1],
	[1,1]
	],
# - 5
# -
# - 
# -
	[[1],
	[1],
	[1],
	[1]
	],
# -- 6
#  -
#  -
	[[1,1],
	[0,1],
	[0,1]
	],
# --- 7
# -
	[[1,1,1],
	[1,0,0]
	],
# - 8
# -
# --
	[[1,0],
	[1,0],
	[1,1]
	],
# - 9
# --
#  -
	[[1,0],
	[1,1],
	[0,1]],
# - 10
# --
# -
	[[1,0],
	[1,1],
	[1,0]],
#  - 11
# ---
	[[0,1,0],
	[1,1,1]],
#  -
# -- 12
#  -
	[[0,1],
	[1,1],
	[0,1]]
]



class Board:
	def __init__(self):
		self.height = 400
		self.width = 300
		self.color = (255,255,255) #Tuplo RGB
		self.surface = pygame.Surface((self.width, self.height))
		self.surface.fill(self.color)
		self.rectangle = self.surface.get_rect()

class Piece:
	def __init__(self):
		self.color=(255,0,0)
		self.pieceIndex = random.randrange(len(pieces))
		self.pieceChoice = pieces[self.pieceIndex]
		self.xPos = 0 
		self.yPos = 0
		self.bottomLimit = 0
		self.topLimit = 0
	
	def debugPiece(self):
		print("Color: " + str(self.color))
		print("Piece: " + str(self.pieceChoice))

	def dropIt(self, window):
		#time.sleep(0.3) #pausa durante 0.5 segundo
		window.fill((0,0,0))
		self.displayPiece(window,(self.xPos,self.yPos+25))

	def moveXaxis(self,isLeft, window):
		if (isLeft == True):
			if ( self.xPos >= 50):
				self.xPos -= 50
		else:
			if ( self.xPos <= 750):
				self.xPos += 50
		window.fill((0,0,0))
		self.displayPiece(window, (self.xPos, self.yPos))
		pygame.display.update()

	def overlaps(self, floorPieces):
		for aux in floorPieces:
			if (self.bottomLimit == aux.topLimit and self.xPos == aux.xPos):
				return True
		return False


	def displayPiece(self, window, pos):
		self.yPos = pos[1]
		hOffset = 0 #horizontal offset
		vOffset = 0 #vertical offset

		for iList in self.pieceChoice:
			for j in iList:
				if (j == 1): #lets draw
				#	print("Imprimi um quadrado :)" + str(hOffset))
					pygame.draw.rect(window,self.color,(pos[0]+hOffset,pos[1]+vOffset,50,50),3) #(x,y,width,height)
				#	pygame.display.flip()
				hOffset += 50
			hOffset = 0
			vOffset += 50
		self.topLimit = pos[1]
		self.bottomLimit = pos[1]+vOffset

	def flipPiece(self, window):
		print("Rodando... :)")
		#clearScreen()
		if (self.pieceIndex == 0):
			self.pieceIndex = 5
			self.pieceChoice = pieces[self.pieceIndex]
		elif (self.pieceIndex == 1):
			self.pieceIndex = 6
			self.pieceChoice = pieces[self.pieceIndex]
		elif (self.pieceIndex == 2):
			self.pieceIndex = 9
			self.pieceChoice = pieces[self.pieceIndex]
		elif (self.pieceIndex == 3):
			self.pieceIndex = 10
			self.pieceChoice = pieces[self.pieceIndex]
		elif (self.pieceIndex == 4):
			self.pieceIndex = 4
			self.pieceChoice = pieces[self.pieceIndex]
		elif (self.pieceIndex == 5):
			self.pieceIndex = 0
			self.pieceChoice = pieces[self.pieceIndex]
		elif (self.pieceIndex == 6):
			self.pieceIndex = 7
			self.pieceChoice = pieces[self.pieceIndex]
		elif (self.pieceIndex == 7):
			self.pieceIndex = 8
			self.pieceChoice = pieces[self.pieceIndex]
		elif (self.pieceIndex == 8):
			self.pieceIndex = 1
			self.pieceChoice = pieces[self.pieceIndex]	
		elif (self.pieceIndex == 9):
			self.pieceIndex = 2
			self.pieceChoice = pieces[self.pieceIndex]
		elif (self.pieceIndex == 10):
			self.pieceIndex = 11
			self.pieceChoice = pieces[self.pieceIndex]
		elif (self.pieceIndex == 11):
			self.pieceIndex = 12
			self.pieceChoice = pieces[self.pieceIndex]
		elif (self.pieceIndex == 12):
			self.pieceIndex = 3
			self.pieceChoice = pieces[self.pieceIndex]
		window.fill((0,0,0))
		self.displayPiece(window, (self.xPos, self.yPos))
		pygame.display.update()




#Chama a funcao main quando abre o programa
def main():

	pygame.init()
	pygame.event.set_blocked(pygame.MOUSEMOTION)
	piece = None
	pygame.time.set_timer(pygame.USEREVENT+1, 800)
	dont_burn_my_cpu = pygame.time.Clock()
	while True:
		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
				sys.exit(0)
			elif (event.type == KEYDOWN and event.key == K_RETURN):
				#startGame()
				piece = tempGeneratePiece()
			elif (event.type == KEYDOWN and event.key == K_t):
				piece.flipPiece(window)
			elif (event.type == KEYDOWN and event.key == K_LEFT):
				piece.moveXaxis(True, window)
			elif (event.type == KEYDOWN and event.key == K_RIGHT):
				piece.moveXaxis(False, window)
			if (not (piece is None)):
				if (piece.bottomLimit >= 550 or piece.overlaps(floorPieces)):
					floorPieces.append(piece)
					piece = tempGeneratePiece()
					window.fill((0,0,0))
				else:
					piece.dropIt(window)
				for i in floorPieces: #pega nas pecas velhas e mete as no ecra
					i.displayPiece(window, (i.xPos, i.yPos))
				pygame.draw.lines(window, (0, 255, 0), False, [(0,550),(800,550)],4)
				pygame.display.update()
		dont_burn_my_cpu.tick(60)	

def tempGeneratePiece():
	#mainBoard = Board()
	#window.fill((0,0,0))
	piece1 = Piece()
	#piece1.debugPiece()
	piece1.displayPiece(window, (0,0))
	pygame.display.update()
	return piece1

def startGame():
	#build the board
	mainBoard = Board()
	
	#draws board
	#window.blit(mainBoard.surface, (200,100))
	#pygame.display.flip()
	
	window.fill((0,0,0))
	piece1 = Piece()
	piece1.debugPiece()
	piece1.displayPiece(window, (0,0))
	pygame.display.update()

def clearScreen():
	window.fill((0,0,0))

main()
