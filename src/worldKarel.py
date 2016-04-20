from gui import *
from karel import Karel
import time
import copy
import sys

worldFile = open('../worlds/testProfe.txt', 'r')
rows = int()
columns = int()
world = list()
karelCount = 0
karelList = list()
mainKarel=False

global flagNoErrors 
flagNoErrors= True

def getSize():
	'''
	    This method reads from the world.txt file the dimensions of the world
	'''
	global rows, columns
	rows = int(worldFile.readline())
	print rows
	columns = int(worldFile.readline())
	print columns


def createWorld():
	'''
	    This method reads from the world.txt all the data of the world in order
	    to import it to the program
	'''
	global columns, rows, world, karelCount, mainKarel
	getSize()
	world = [[list() for x in range(columns)] for x in range(rows)]
	#worldFile.read(1)
	for i,line in enumerate(worldFile):
		for j,c in enumerate(line):
			if 'l' in c or 'r' in c or 'u' in c or 'd' in c:
				if not mainKarel:
					mainKarel=True
					#id, index, idF, colF, rowF, facingF
					karelInit = Karel(0, 0, -1, j, i, c)
					karelList.append(karelInit)
					karelCount+=1
					world[i][j].append(karelInit)
				else:
					print "More than one Karel declared, just one instance is accepted"
					sys.exit()
			elif c.isdigit():
				for x in range(int(c)):
					world[i][j].append("B")	
			elif not c == "\n":
				world[i][j].append(c)

def move(karel):
	'''
	    Moves Karel one step ahead on the world to the
	    direction where it is facing
	'''
	#checar que no se salga del mundo
	global world, flagNoErrors
	if checkFrontIsClear(karel) and checkFrontIsNotFull(karel):
		if karel.facing == "left":
			if karel.col==0:
				flagNoErrors=False
				print "Invalid operation"
			else:
				print "move left"
				world[karel.row][karel.col-1].append(karel)
				world[karel.row][karel.col].remove(karel) 
				karel.setPosition(karel.col-1, karel.row)
		elif karel.facing == "right":
			if karel.col==columns-1:
				flagNoErrors=False
				print "Invalid operation"
			else:
				print "move right"
				world[karel.row][karel.col+1].append(karel)
				world[karel.row][karel.col].remove(karel)
				karel.setPosition(karel.col+1, karel.row)
		elif karel.facing == "up":
			if karel.row==0:
				flagNoErrors=False
				print "Invalid operation"
			else:
				print "move up"
				world[karel.row-1][karel.col].append(karel)
				world[karel.row][karel.col].remove(karel)
				karel.setPosition(karel.col, karel.row-1)
		else:
			if karel.row==rows-1:
				flagNoErrors=False
				print "Invalid operation"
			else:
				print "move down"
				world[karel.row+1][karel.col].append(karel)
				world[karel.row][karel.col].remove(karel)
				karel.setPosition(karel.col, karel.row+1)
	else:
		flagNoErrors = False

def turnleft(karel):
	'''
	    Change Karel instance to face to its left
	'''
	if karel.facing == "left":
		karel.setFacing("down")
		print "I'm looking down"
	elif karel.facing == "right":
		karel.setFacing("up")
		print "I'm looking up"
	elif karel.facing == "up":
		karel.setFacing("left")
		print "I'm looking left"
	else:
		karel.setFacing("right")
		print "I'm looking right"

def pickbeeper(karel):
	'''
	    This method checks if there is a beeper on the position where the receive instance
	    of Karel is place it. If the beeper exist Karel will pick it up otherwise the method will send an error
	'''
	global flagNoErrors
	if "B" in world[karel.row][karel.col]:
		world[karel.row][karel.col].remove("B")
		karel.pickBeeper()
		print str(karel.name) + ": Picked a beeper"
	else:
		print "Error at picking beeper!"
		flagNoErrors = False

def putbeeper(karel):
	'''
	    This method checks if Karel has a beeper, if it is the case Karel receive instance puts the beeper in its 
	    current position elsewhere the method will send an error
	'''
	global flagNoErrors
	if karel.beepers > 0:
		karel.dropBeeper()
		world[karel.row][karel.col].append("B")
		print str(karel.name) + ": Put beeper down"
	else:
		print "I don't have a beeper to leave :("
		flagNoErrors = False

def givebeeper(karel, count):
	companion = _getCompanion(karel)
	if companion != None:
		for i in xrange(count):
			putbeeper(karel)
			pickbeeper(companion)


def checkFrontIsClear(karel):
	'''
	    This method returns False if Karel is facing a wall 
	    or a none world position True otherwise.
	'''
	if karel.facing == "left":
		if karel.col==0:
			return False
		else:
			content = world[karel.row][karel.col-1]
	elif karel.facing == "right":
		if karel.col==columns-1:
			return False
		else:
			content = world[karel.row][karel.col+1]
	elif karel.facing == "up":
		if karel.row==0:
			return False
		else:
			content = world[karel.row-1][karel.col]
	else:
		if karel.row==rows-1:
			return False
		else:
			content = world[karel.row+1][karel.col]
	if "x" in content:
		return False
	else:
		return True

def checkFrontIsBlocked(karel):
	'''
	    This method returns True if Karel is facing a wall 
	    or a none world position False otherwise. 
	'''
	return not checkFrontIsClear(karel)

def checkLeftIsClear(karel):
	'''
	    This method Checks the left position of Karel's facing and
	    returns False if Karel is facing a wall 
	    or a none world position True otherwise.
	'''
	content = ""
	if karel.facing == "left":
		if karel.row==rows-1:
			return False
		else:
			content = world[karel.row+1][karel.col]
	elif karel.facing == "right":
		if karel.row==0:
			return False
		else:
			content = world[karel.row-1][karel.col]
	elif karel.facing == "up":
		if karel.col==0:
			return False
		else:
			content = world[karel.row][karel.col-1]
	else:
		if karel.col==columns-1:
			return False
		else:
			content = world[karel.row][karel.col+1]
	if "x" in content:
		return False
	else:
		return True

def checkLeftIsBlocked(karel):
	'''
	    This method checks the left position of Karel's facing and
	    returns True if Karel is facing a wall 
	    or a none world position False otherwise.
	'''
	return not checkLeftIsClear(karel)

def checkRightIsClear(karel):
	'''
	    This method checks the right position of Karel's facing and
	    returns False if Karel is facing a wall 
	    or a none world position True otherwise.
	'''
	print "check right"
	if karel.facing == "left":
		if karel.row==0:
			return False
		else:
			content = world[karel.row-1][karel.col]
	elif karel.facing == "right":
		if karel.row==rows-1:
			return False
		else:
			content = world[karel.row+1][karel.col]
	elif karel.facing == "up":
		if karel.col==columns-1:
			return False
		else:
			content = world[karel.row][karel.col+1]
	else:
		if karel.col==0:
			return False
		else:
			content = world[karel.row][karel.col-1]
	if "x" in content:
		return False
	else:
		return True

def checkRightIsBlocked(karel):
	'''
	    This method checks the right position of Karel's facing and
	    returns True if Karel is facing a wall 
	    or a none world position False otherwise.
	'''
	print "check right blocked"
	return not checkRightIsClear(karel)

def checkNextToBeeper(karel):
	'''
	    This method returns True if there is a beeper on the immediate intersections False otherwise 
	'''
	return "B" in world[karel.row][karel.col]
	#if "B" in world[karel.row+1][karel.col] or "B" in world[karel.row-1][karel.col] or "B" in world[karel.row][karel.col-1] or "B" in world[karel.row][karel.col+1]:
	#	return True
	#else:
	#	return False

def checkNotNextToBeeper(karel):
	'''
	    This method returns False if there is a beeper on the immediate intersections True otherwise 
	'''
	return not checkNextToBeeper(karel)

def checkAnyBeepers(karel):
	'''
	    This method returns True if Karel instance has at least one beeper False otherwise 
	'''
	return karel.beepers > 0

def checkNotAnyBeepers(karel):
	'''
	    This method returns True if Karel instance does not has any beeper False otherwise 
	'''
	return not checkAnyBeepers(karel)

def checkFacingNorth(karel):
	'''
	    This method returns True if Karel instance is facing to North False otherwise 
	'''
	return karel.facing == "up"

def checkNotFacingNorth(karel):
	'''
	    This method returns True if Karel instance is not facing to North False otherwise 
	'''
	return not checkFacingNorth(karel)

def checkFacingSouth(karel):
	'''
	    This method returns True if Karel instance is facing to South False otherwise 
	'''
	return karel.facing == "down"

def checkNotFacingSouth(karel):
	'''
	    This method returns True if Karel instance is not facing to North False otherwise 
	'''
	return not checkFacingSouth(karel)

def checkFacingEast(karel):
	'''
	    This method returns True if Karel instance is facing to East False otherwise 
	'''
	return karel.facing == "right"

def checkNotFacingEast(karel):
	'''
	    This method returns True if Karel instance is not facing to North False otherwise 
	'''
	return not checkFacingEast(karel)

def checkFacingWest(karel):
	'''
	    This method returns True if Karel instance is facing to West False otherwise 
	'''
	return karel.facing == "left"

def checkNotFacingWest(karel):
	'''
	    This method returns True if Karel instance is not facing to West False otherwise 
	'''
	return not checkFacingWest(karel)

def checkFrontIsFull(karel):
	'''
	    This method returns True if no more Karels are allowed to be on the front space. 
	'''
	if karel.facing == "left":
		if karel.col==0:
			return False
		else:
			content = world[karel.row][karel.col-1]
	elif karel.facing == "right":
		if karel.col==columns-1:
			return False
		else:
			content = world[karel.row][karel.col+1]
	elif karel.facing == "up":
		if karel.row==0:
			return False
		else:
			content = world[karel.row-1][karel.col]
	elif karel.row==rows-1:
		return False
	else:
		content = world[karel.row+1][karel.col]

	count = 0
	for i in content:
		if isinstance(i, Karel):
			count = count + 1
	return count >= 2

def checkFrontIsNotFull(karel):
	'''
	    This method returns True if more Karels are allowed to be on the front space.
	'''
	return not checkFrontIsFull(karel)

def checkAmIAlone(karel):
	'''
	    This method returns True if Karel is the only one occupying his current position.
	'''
	return _getCompanion(karel) == None

def checkAmINotAlone(karel):
	'''
	    This method returns True if Karel is not the only one occupying his current position.
	'''
	return not checkAmIAlone(karel)

def checkIsFather(karel):
	'''
	    This method returns True if the other Karel in the same place is his father.
	'''
	companion = _getCompanion(karel)
	return companion is not None and companion.id == karel.idF

def checkIsNotFather(karel):
	'''
	    This method returns True if the other Karel in the same place is not his father.
	'''
	return not checkIsFather(karel)


def checkIsSon(karel):
	'''
	    This method returns True if the other Karel in the same place is his son.
	'''
	companion = _getCompanion(karel)
	return companion is not None and companion.idF == karel.id

def checkIsNotSon(karel):
	'''
	    This method returns True if the other Karel in the same place is not his son.
	'''
	return not checkIsSon(karel)

def checkIsDescendant(karel):
	'''
	    This method returns True if the other Karel in the same place is his descendant.
	'''

	current = _getCompanion(karel)
	print 'CHECKING FOR DESCENDANCE'
	while(current != None):
		
		if current.father == karel:
			print 'IS DESCENDANT'
			return True
		else:
			current = current.father
	print 'IS NOT DESCENDANT'			
	return False


def checkIsNotDescendant(karel):
	'''
	    This method returns True if the other Karel in the same place is not his descendant.
	'''	
	return not checkIsDescendant(karel)

def printWorld():
	'''
	    This method draws the world to the graphic user interface 
	'''
	global world, columns, rows
	copyWorld = copy.deepcopy(world)
	
	for row in copyWorld:
		for val in row:
			if any(isinstance(x, worldKarel.Karel) for x in val):
				for w in range(len(val)):
					if isinstance(val[w],worldKarel.Karel):
						val[w] = val[w].name

	for row in copyWorld:
		for val in row:
			print '{:2}'.format(val),
		print 
    
	repaint(world)
	time.sleep(0.05)

def finalWorld():
	'''
		This method prints the final instance of the world
	'''
	global world
	paintFinalWorld(world)

def dropBeepers(karel):
	'''
	    Drops all the beeper that the Karel instance has on its current position
	'''
	print "Drop beepers"
	for x in range(karel.beepers):
		world[karel.row][karel.col].append("B")
    

def killSons(karel):
	'''
	    This method kills all the sons of Karel instance
	'''
	print "drop sons"
	for son in karelList:
		if son.idF == karel.id:
			son.kill()

def leaveWorld(karel):
	'''
	    This methos removes Karel instance's body of the world
	'''
	print "Leaving World"
	karelList.remove(karel)
	world[karel.row][karel.col].remove(karel)

def _getCompanion(karel):

	'''
	'''

	for companion in karelList:
		if companion.id != karel.id and companion.row == karel.row and companion.col == karel.col:
			return companion
	return None