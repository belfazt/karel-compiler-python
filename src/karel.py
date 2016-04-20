import worldKarel

class Karel(object):
	'''
	    This class defines Karel's object:
	    Karel has the following attributes
	        -id
	        -A list of beepers
	        -An index that indicates what  
	        -position (composed by column and row)
	        -A facing attribute that defines where is the Karel point of view
	        -An alive attribute that indicates if Karel is or not 
	        -Karel Stack which saves position old the interCodeArray after a call to a function 
	'''
	def __init__(self, id, index, idF = None, colF = None, rowF = None, facingF = None, father = None):
		self.callStack = list()
		self.iterateStack = list()
		self.beepers = 0
		self.alive = True
		self.id = id
		self.name="Karel" + str(self.id)
		self.index = index
		self.father = father
		if father != None:
			self.idF = father.id
			self.col = father.col
			self.row = father.row
			self.facing=self.setInitFacing(father.facing)	
		else:
			self.idF = idF
			self.col = colF
			self.row = rowF
			self.facing=self.setInitFacing(facingF)

	def pickBeeper(self):
	    self.beepers += 1

	def dropBeeper(self):
	    self.beepers -= 1

	def kill(self):
	    print self.name + ' died with ' + str(self.beepers) + ' beepers at ' + str(self.row) + ', ' + str(self.col)
	    self.alive = False
	    worldKarel.leaveWorld(self)
	    worldKarel.dropBeepers(self)
	    worldKarel.killSons(self)

	def addIndex(self):
	    self.index+=1

	def setPosition(self, col, row):
	    self.row = row
	    self.col = col

	def setFacing(self, facing):
	    self.facing = facing

	def setInitFacing(self, c):
		if c == 'l' or c == "left":
			return "left"
		elif c == 'r' or c == "right":
			return "right"
		elif c == 'u' or c == "up":
			return "up"
		else:
			return "down"

	def __str__(self):
	    print self.id
