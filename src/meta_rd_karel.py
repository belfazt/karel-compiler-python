CALL = "CALL"
RET = "RET"
JMP = "JMP"
IF = "IF"
FRONT_IS_CLEAR = "FRONT_IS_CLEAR"
FRONT_IS_BLOCKED = "FRONT_IS_BLOCKED"
LEFT_IS_CLEAR = "LEFT_IS_CLEAR"
LEFT_IS_BLOCKED = "LEFT_IS_BLOCKED"
RIGHT_IS_CLEAR = "RIGHT_IS_CLEAR"
RIGHT_IS_BLOCKED = "RIGHT_IS_BLOCKED"
NEXT_TO_A_BEEPER = "NEXT_TO_A_BEEPER"
NOT_NEXT_TO_A_BEEPER = "NOT_NEXT_TO_A_BEEPER"
ANY_BEEPERS_IN_BEEPER_BAG = "ANY_BEEPERS_IN_BEEPER_BAG"
NOT_ANY_BEEPERS_IN_BEEPER_BAG = "NOT_ANY_BEEPERS_IN_BEEPER_BAG"
FACING_NORTH = "FACING_NORTH"
FACING_SOUTH = "FACING_SOUTH"
FACING_EAST = "FACING_EAST"
FACING_WEST = "FACING_WEST"
NOT_FACING_NORTH = "NOT_FACING_NORTH"
NOT_FACING_SOUTH = "NOT_FACING_SOUTH"
NOT_FACING_EAST = "NOT_FACING_EAST"
NOT_FACING_WEST = "NOT_FACING_WEST"
FRONT_IS_FULL = "FRONT_IS_FULL"
FRONT_IS_NOT_FULL = "FRONT_IS_NOT_FULL"
AM_I_ALONE = "AM_I_ALONE"
AM_I_NOT_ALONE = "AM_I_NOT_ALONE"
IS_FATHER = "IS_FATHER"
IS_SON = "IS_SON"
IS_DESCENDANT = "IS_DESCENDANT"
TURN_LEFT = "TURN_LEFT"
TURN_OFF = "TURN_OFF"
MOVE = "MOVE"
PICK_BEEPER = "PICK_BEEPER"
PUT_BEEPER = "PUT_BEEPER"
GIVE_BEEPER = "GIVE_BEEPER"
OR = "OR"
AND = "AND"
NOT = "NOT"
ITE = "ITE"
CLONE = "CLONE"

SymbolTable = dict()

def printAtokensInput():
    '''
        This method prints to console the ArokensInput array 
    '''
    print aTokensInput

def string_without_spaces():
    '''
        This method returns the currenToken without spaces
    '''
    global currentToken
    nameFunction=aTokensInput[currentToken]
    currentToken+=1
    return nameFunction

def currentTokenMod(value):
    '''
        This method adds the receive value to the currentToken
    '''
    global currentToken
    currentToken+=value

def setCurrentTokenMod(value):
    '''
        This method sets the receive value to the currentToken
    '''
    global currentToken
    currentToken=value

def current():
    '''
        This method returns the value of currentToken
    '''
    global currentToken
    return aTokensInput[currentToken]

def getCurrentIndexToken():
    '''
        This method retuns the curren token (index)
    '''
    global currentToken    
    return currentToken

def exigir(tokenRequerido):
    '''
        This method returns True if the receive token is the same as the current token
        False otherwise. And moves the value of current token to the next token.
    '''
    result=False
    global currentToken
    if tokenRequerido==aTokensInput[currentToken]:
        result=True
    else:
        result=False
    currentToken+=1
    return result

def getLine():
    '''
        Returns the line where the token is written
    '''
    global currentToken
    return tokenLines[currentToken] - 1

def leer(tokenRequerido, inc=0):
    '''
        This method returns True if the receive token is the same as the current token
        False otherwise.
    '''
    result=False
    global currentToken
    if tokenRequerido==aTokensInput[currentToken]:
        result=True
    else:
        result=False
    currentToken+=inc
    return result

def findStartPointOfFunction(nameFunction):
    '''
       Checks the symbol table in order to find the start point that is pass as an argument. 
    '''
    if nameFunction in SymbolTable:
        return SymbolTable[nameFunction]
    else:
        return 0xFF

def AddNewFunction(tokenRequerido, inicio):
    '''
       Adds the value "inicio" to the Symbol table in the name of the function (tokenRequerido) position. 
       
    '''
    SymbolTable[tokenRequerido]=inicio








