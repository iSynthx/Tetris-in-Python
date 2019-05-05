#Class Piece
#Represents a tetramino (piece) instance

import pygame
import random as rnd
from tetraminos import *
import auxiliary
from Config import *

class Piece:
	######################
	# Declares a piece object that contains information about
	# color, type, rotation, position and top and bottom bounds.
	######################
	def __init__(self):
		self.color = auxiliary.randomizeColor() #default, randomize colors
		self.pieceIndex = rnd.randrange(len(pieces)) #choose a random piece
		self.pieceChoice = pieces[self.pieceIndex]
		self.xPos = 0 
		self.yPos = 0
		self.bottomLimit = 0
		self.topLimit = 0
		#beta2
		self.squarePositions = self.calculateBlockPositions()
	
	#calculateBlockPositions(this)
	#Auxiliary function to calculate initial block locations for the piece
	# (block -> a square of the piece) ; x = 0 , y = 0 top left 
	def calculateBlockPositions(self):
		positions = []
		x = 0
		y = 0
		for aux1 in self.pieceChoice:
			for aux2 in aux1:
				if (aux2 == 1):
					positions.append( (x,y) )
					x += 50
			x = 0
			y += 50
		return positions
	
	#debugPiece(this)
	#Shows information about this object
	def debugPiece(self):
		print("Color: " + str(self.color))
		print("Piece: " + str(self.pieceChoice))
		print("Position (x): " + str(self.xPos))
		print("Position (y): " + str(self.yPos))
		print("Top Position: " + str(self.topLimit))
		print("Bottom Position: " + str(self.bottomLimit))
		print("State of block positions: " + str(self.squarePositions) + "\n")

	#dropIt(this, WindowObject)
	#Pushes piece one space down
	def dropIt(self, window):
		window.fill((0,0,0))

		#Push each block down one square
		#Those mad Haskell skills =)
		self.squarePositions = [(i, j+50) for i, j in self.squarePositions]
		self.displayPiece(window,(self.xPos,self.yPos+50))

	#moveXaxis(this, boolean, WindowObject)
	#Moves piece along the X axis, as requested by a keystroke
	def moveXaxis(self,isLeft, window):
		#Adjusts position, including blocks and saves it in the object
		if (isLeft == True):
			if ( self.xPos >= privateConfig["max_screen_left"]):
				#Those mad Haskell skills =)
				self.squarePositions = [(i-50, j) for i, j in self.squarePositions]
				self.xPos -= 50
		else:
			if ( self.xPos < privateConfig["max_screen_right"]):
				#Those mad Haskell skills =)
				self.squarePositions = [(i+50, j) for i, j in self.squarePositions]
				self.xPos += 50
		#Resets the screen and draws the piece on the new position
		window.fill((0,0,0))
		self.displayPiece(window, (self.xPos, self.yPos))
		pygame.display.update()

	#overlaps(this, list of Piece)
	#Checks if the current piece overlaps with one of the resting pieces
	#Traverses the list and calls the comparator
	def overlaps(self, floorPieces):
		for auxP in floorPieces:
			if (self.overlaps2Pieces(auxP)):
				return True
		return False
	
	#overlaps2Pieces(this, Piece)
	#A comparator of 2 pieces blocks (this, b)
	def overlaps2Pieces(self, b):
		for aux1 in self.squarePositions:
			for aux2 in b.squarePositions:
				if (aux1[0] == aux2[0] and ((aux1[1]+50) >= aux2[1])):
					return True
		return False

	#displayPiece(this, WindowObject, tuple of integers)
	#Calculates each part of the piece and displays it on the screen
	def displayPiece(self, window, pos):
		#In case of manual changes to the position, saves the new position
		self.xPos = pos[0]
		self.yPos = pos[1]
		
		#Auxiliar variables to calculate horizontal and vertical offset
		hOffset = 0
		vOffset = 0

		for aux1 in self.pieceChoice:
			for aux2 in aux1:
				if (aux2 == 1):
					#(WindowObject,RGB tuple,x,y,width,height,bold)
					pygame.draw.rect(window,self.color,(pos[0]+hOffset,pos[1]+vOffset,privateConfig["square_size"],privateConfig["square_size"]),3)
				hOffset += 50
			hOffset = 0
			vOffset += 50
		#Sets the topLimit as the first vertical position
		#Sets the bottomLimit as the last vertical position
		self.topLimit = pos[1]
		self.bottomLimit = pos[1]+vOffset

	#flipPiece(this, WindowObject)
	#Retrieves the piece format of the rotation and refreshes its design on the screen
	def flipPiece(self, window):
		#rotations has the format: rotated = rotation[to_rotate]
		self.pieceIndex = rotations[self.pieceIndex]
		self.pieceChoice = pieces[self.pieceIndex]
		self.squarePositions = self.calculateBlockPositions()
		window.fill((0,0,0))
		self.displayPiece(window, (self.xPos, self.yPos))
		pygame.display.update()

