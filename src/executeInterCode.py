from worldKarel import *
import worldKarel
import time
from meta_rd_karel import *
index = 0
karelFatherAlive = True



def executeIntercode(interCodeArray):
    '''   
        This method reads the world contained into the world.txt file. Also it
        receives and array call interCodeArray.
        The method iterates while The Karel Father is alive and no errors where detected in the last iteration. 
        Each iteration gives one execution step to all the current instances of Karel
    '''
    global karelFatherAlive
    createWorld()
    printWorld()
#    global index
#    callStack = list()
#    iterateStack = list()
    while karelFatherAlive and worldKarel.flagNoErrors:
        for karel in worldKarel.karelList:
            if karelFatherAlive and worldKarel.flagNoErrors:
                executeInterCodeLine(karel,interCodeArray)
    print worldKarel.finalWorld()
        

def executeInterCodeLine(karel,interCodeArray):
    '''
        This method receives one instance of Karel to get its data and the interCodeArray
        The main purpose of this method is to execute one step which is one of the basic function
        such as RET, CALL, IF, etc.
    '''
    global karelFatherAlive
    if interCodeArray[karel.index] == CALL:
        print "This is CALL"
        karel.callStack.append(karel.index+2)
        karel.index = interCodeArray[karel.index+1]
        print karel.index
    elif interCodeArray[karel.index] == RET:
        print "This is RET"
        karel.index = karel.callStack.pop()
        print karel.index
    elif interCodeArray[karel.index] == JMP:
        print "This is JMP"
        karel.index = interCodeArray[karel.index+1]
    elif interCodeArray[karel.index] == IF:
        print "This is IF"
        karel.index += 1
        ifEval = conditionals(karel, interCodeArray)
        if ifEval:
            karel.index+=3
        else:
            karel.index+=1
    elif interCodeArray[karel.index] == ITE:
        print "This is ITE"
        karel.index+=1
        if not interCodeArray[karel.index] == 0:
            interCodeArray[karel.index] = interCodeArray[karel.index]-1
            karel.index+=3
        else:
            karel.index+=1
    elif interCodeArray[karel.index] == TURN_LEFT:
        print "This is TURN_LEFT"
        turnleft(karel)
        karel.index+=1
    elif interCodeArray[karel.index] == MOVE:
        print "This is MOVE"
        move(karel)
        karel.index+=1
        if worldKarel.flagNoErrors:
            printWorld()
    elif interCodeArray[karel.index] == PICK_BEEPER:
        print "This is PICK_BEEPER"
        pickbeeper(karel)
        karel.index+=1
        if worldKarel.flagNoErrors:
            printWorld()
    elif interCodeArray[karel.index] == PUT_BEEPER:
        print "This is PUT_BEEPER"
        putbeeper(karel)
        karel.index+=1
        if worldKarel.flagNoErrors:
            printWorld()
    elif interCodeArray[karel.index] == GIVE_BEEPER:
        print "This is GIVE_BEEPER"
        givebeeper(karel)
        karel.index+=1
        if worldKarel.flagNoErrors:
            printWorld()
    elif interCodeArray[karel.index] == CLONE:
        print "this is clone"
        karel.index+=2
        cloneKarel = Karel(len(worldKarel.karelList),interCodeArray[karel.index],karel.id,karel.col,karel.row,karel.facing)
        worldKarel.karelList.append(cloneKarel)
        worldKarel.world[cloneKarel.row][cloneKarel.col].append(cloneKarel)
        worldKarel.printWorld()
        karel.index+=1
    elif interCodeArray[karel.index] == TURN_OFF:
        print "Turn off"
        karel.kill()
        if karel.idF == -1:
            karelFatherAlive = False

    if not worldKarel.flagNoErrors:
        print "Karel died :("

def conditionals(karel, interCodeArray):
    '''
        Evaluates against the world if the given condition is True of False for the karel instance
    '''
    global index
    if interCodeArray[karel.index] == OR:
        print "This is OR"
        karel.index+=1
        exp1 = conditionals(interCodeArray)
        karel.index+=1
        exp2 = conditionals(interCodeArray)
        if exp1 or exp2:
            print "OR evaluation is TRUE"
            return True
        else:
            return False
    elif interCodeArray[karel.index] == AND:
        print "This is AND"
        karel.index+=1
        exp1 = conditionals(interCodeArray)
        karel.index+=1
        exp2 = conditionals(interCodeArray)
        if exp1 and exp2:
            print "AND evaluation is TRUE"
            return True
        else:
            return False
    elif interCodeArray[karel.index] == NOT:
        print "This is NOT"
        karel.index+=1
        return not conditionalsKarel(karel, interCodeArray)
    else:
        print "conditionals else"
        print interCodeArray[karel.index]
        return conditionalsKarel(karel, interCodeArray)


def conditionalsKarel(karel, interCodeArray):
    '''
            This method checks if the receive instance of Karel accomplish an specific condition in the world.
    '''
    global index
    if interCodeArray[karel.index] == FRONT_IS_CLEAR:
        return checkFrontIsClear(karel)
    elif interCodeArray[karel.index] == FRONT_IS_BLOCKED:
        return checkFrontIsBlocked(karel)
    elif interCodeArray[karel.index] == LEFT_IS_CLEAR:
        return checkLeftIsClear(karel)
    elif interCodeArray[karel.index] == LEFT_IS_BLOCKED:
        return checkLeftIsBlocked(karel) 
    elif interCodeArray[karel.index] == RIGHT_IS_CLEAR:
        return checkRightIsClear(karel)
    elif interCodeArray[karel.index] == RIGHT_IS_BLOCKED:
        return checkRightIsBlocked(karel)
    elif interCodeArray[karel.index] == NEXT_TO_A_BEEPER:
        return checkNextToBeeper(karel)
    elif interCodeArray[karel.index] == NOT_NEXT_TO_A_BEEPER:
        return checkNotNextToBeeper(karel)
    elif interCodeArray[karel.index] == ANY_BEEPERS_IN_BEEPER_BAG:
        return checkAnyBeepers(karel)
    elif interCodeArray[karel.index] == NOT_ANY_BEEPERS_IN_BEEPER_BAG:
        return checkNotAnyBeepers(karel)
    elif interCodeArray[karel.index] == FACING_NORTH:
        return checkFacingNorth(karel)
    elif interCodeArray[karel.index] == FACING_SOUTH:
        return checkFacingSouth(karel)
    elif interCodeArray[karel.index] == FACING_EAST:
        return checkFacingEast(karel)
    elif interCodeArray[karel.index] == FACING_WEST:
        return checkFacingWest(karel)
    elif interCodeArray[karel.index] == NOT_FACING_NORTH:
        return checkNotFacingNorth(karel)
    elif interCodeArray[karel.index] == NOT_FACING_SOUTH:
        return checkNotFacingSouth(karel)
    elif interCodeArray[karel.index] == NOT_FACING_EAST:
        return checkNotFacingEast(karel)
    elif interCodeArray[karel.index] == NOT_FACING_WEST:
        return checkNotFacingWest(karel)
    elif interCodeArray[karel.index] == FRONT_IS_FULL:
        return checkFrontIsFull(karel)
    elif interCodeArray[karel.index] == FRONT_IS_NOT_FULL:
        return checkFrontIsNotFull(karel)
    elif interCodeArray[karel.index] == AM_I_ALONE:
        return checkAmIAlone(karel)
    elif interCodeArray[karel.index] == AM_I_NOT_ALONE:
        return checkAmINotAlone(karel)
    elif interCodeArray[karel.index] == IS_FATHER:
        return checkIsFather(karel)
    elif interCodeArray[karel.index] == IS_SON:
        return checkIsSon(karel)
    elif interCodeArray[karel.index] == IS_DESCENDANT:
        return checkIsDescendant(karel)