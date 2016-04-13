from meta_rd_karel import *
from errors_karel import *
from executeInterCode import *

InterCode = list()

InterCodeIndex=0

#<program> ::= "class program" "{" <functions> <main function> "}"
def program():
    '''
        Validates this grammar: <program> ::= "class program" "{" <functions> <main function> "}"
        And creates the interCode by reading from the intercodeFile
    '''
    global InterCode
    global InterCodeIndex
    if exigir("class"):
        if  exigir("program"):
            if exigir("{"):
                InterCode.append(JMP)
                InterCode.append("")
                InterCodeIndex += 2
                functions()
                main_function()
                if not exigir("}"):
                    showErrorMessage(3, getLine())
        else:
            showErrorMessage(4, getLine())
    else:
        showErrorMessage(4, getLine())
    intercodeFile = open("../out/compiled.icode",'w')
    intercodeFile.write(str(InterCode))
    executeIntercode(InterCode)

#<functions> ::= <functions prima>
def functions():
    '''
        Validates this grammar <functions> ::= <functions prima>
    '''
    function_prima()

#<functions prima> ::= <function> <functions prima> | lambda
def function_prima():
    '''
        Validates this grammar <functions prima> ::= <function> <functions prima> | lambda
    '''
    if leer("void"):
        function()
        function_prima()

#<main function> ::= "program()" "{" <body> "}"
def main_function():
    '''
        Validates this grammar <main function> ::= "program()" "{" <body> "}"
    '''
    global InterCode
    global InterCodeIndex
    if exigir("program"):
        if exigir("("):
            if exigir(")"):
                if exigir("{"):
                    InterCode[1] = InterCodeIndex
                    body()
                    if not exigir("}"):
                        showErrorMessage(3, getLine())
                else:
                    showErrorMessage(1, getLine())
            else:
                showErrorMessage(2, getLine())
        else:
            showErrorMessage(5, getLine())
    else:
        showErrorMessage(4, getLine())

#<function> := "void" <name function> "()" "{" <body> "}"
def function():
    '''
        Validates this grammar: <function> := "void" <name function> "()" "{" <body> "}"
    '''
    global InterCode
    global InterCodeIndex
    if exigir("void"):
        name_function()
        if exigir("("):
            if exigir(")"):
                if exigir("{"):
                    body()
                    if not exigir("}"):
                        showErrorMessage(3, getLine())
                    InterCode.append(RET)
#                   InterCode[ InterCodeIndex ] = RET
                    InterCodeIndex += 1
                else:
                    showErrorMessage(1, getLine())
            else:
                showErrorMessage(2, getLine())
        else:
            showErrorMessage(5, getLine())
    else:
        print ""
        #error de sintaxis, fin de ejecucion

# <name function> ::= <string without spaces>
def name_function():
    '''
        Validates this grammar: <name function> ::= <string without spaces>
    '''
    global InterCodeIndex
    nameFunction = string_without_spaces()
    AddNewFunction( nameFunction, InterCodeIndex )


#<body> ::= <expressions>
def body():
    '''
        This method calls the expression method
    '''
    expressions()

#<expressions> ::= <expression> <expressions prima>
def expressions():
    '''
        Validates this grammar: <expressions> ::= <expression> <expressions prima>
    '''
    expression()
    expressions_prima()



#<expression> ::= <call function> |
#  <if expression> |
#  <while expression> |
#  <iterate expression>
def expression():
    '''
        Validates this grammar: <expression> ::= <call function> | <if expression> | <while expression> | <iterate expression>
    '''
    if leer("if"):
        if_expression()
    elif leer("while"):
        while_expression()
    elif leer("iterate"):
        iterate_expression()
    else:
        call_function()


#<expressions prima> ::= <expression> <expressions prima> | lambda
def expressions_prima():
    '''
        Validates this grammar: <expressions prima> ::= <expression> <expressions prima> | lambda
    '''
    if not leer("}"):
        expression()
        expressions_prima()


#<call function> ::= <name of function> | <clone>
def call_function():
    '''
        Validates this grammar: <call function> ::= <name of function> | <clone>
    '''
    if leer("clone"):
        clone()
    else:
        name_of_function()



#<name of function> ::= <official function>() | <customer function>()
def name_of_function():
    '''
        Validates this grammar: <name of function> ::= <official function>() | <customer function>()
    '''
    if leer("move") or leer("turnoff") or leer("pickbeeper") or leer("turnleft") or leer("putbeeper") or leer("givebeeper"):
        official_function()
    else:
        customer_function()

# <official function> ::=
#    "move" |
#    "turnoff" |
#    "pickbeeper" |
#    "turnleft" |
#    "putbeeper" |
#    "giveBeeper" |

def official_function():
    '''
        Validates this grammar:
                <official function> ::=
                                        "move" |
                                        "turnoff" |
                                        "pickbeeper" |
                                        "turnleft" |
                                        "putbeeper" |
                                        "givebeeper" |
    '''
    global InterCode
    global InterCodeIndex
    needsArgument = False
    if leer("turnleft"):
        exigir("turnleft")  #turn left karel
        InterCode.append(TURN_LEFT)
        InterCodeIndex+=1
    elif leer("turnoff"):    #turn off karel
            exigir("turnoff")
            InterCode.append(TURN_OFF)
            InterCodeIndex+=1
    elif leer("move"):    #move karel
            exigir("move")
            InterCode.append(MOVE)
            InterCodeIndex+=1
    elif leer("pickbeeper"):
            exigir("pickbeeper")
            InterCode.append(PICK_BEEPER)
            InterCodeIndex+=1
    elif leer("putbeeper"):
            exigir("putbeeper")
            InterCode.append(PUT_BEEPER)
            InterCodeIndex+=1
    elif leer("givebeeper"):
            exigir("givebeeper")
            InterCode.append(GIVE_BEEPER)
            InterCodeIndex+=1
            needsArgument = True
    if exigir("("):
        if needsArgument:
            beepersToGive=(int(current()))
            InterCode.append(beepersToGive)
            InterCodeIndex+=1
            currentTokenMod(1)
        if not exigir(")"):
            showErrorMessage(2, getLine())
    else:
        showErrorMessage(5, getLine())

#<customer function> ::= <string without spaces>
def customer_function():
    '''
        Validates this grammar: <customer function> ::= <string without spaces>
    '''
    global InterCode
    global InterCodeIndex
    PosFunctionInCodeInter=int()
    nameFunction = string_without_spaces( )
    PosFunctionInCodeInter = findStartPointOfFunction( nameFunction )
    if PosFunctionInCodeInter != 0xFF:
        InterCode.append(CALL)
#       InterCode[ InterCodeIndex ] = CALL
        InterCodeIndex += 1
        InterCode.append(PosFunctionInCodeInter)
#       InterCode[ InterCodeIndex ] = PosFunctionInCodeInter
        InterCodeIndex += 1
    else:
        showErrorMessage(6, getLine())
    if exigir("("):
        if not exigir(")"):
            print "customer"
            showErrorMessage(2, getLine())
    else:
        print "Customer"
        showErrorMessage(5, getLine())

#<if expression> ::= "if" ( <conditional> ) "{" <body> "}" [ <elseif> ]
def if_expression():
    '''
        Validates this grammar: <if expression> ::= "if" ( <conditional> ) "{" <body> "}" [ <elseif> ]
    '''
    global InterCode
    global InterCodeIndex
    PosX_jmptrue= 0
    if exigir("if"):
        InterCode.append(IF)
        #InterCode[ InterCodeIndex ] = IF
        InterCodeIndex += 1
        if exigir("("):
            conditional()
            if exigir(")"):
                InterCode.append(JMP)
                #InterCode[ InterCodeIndex ] = JMP
                InterCodeIndex += 1
                InterCode.append('')
                PosX_jmptrue = InterCodeIndex
                InterCodeIndex += 1
                if exigir("{"):
                    body()
                    if exigir("}"):
                        if leer("else"):
                            elseif( PosX_jmptrue )
                        else:
                            InterCode[ PosX_jmptrue ] = InterCodeIndex
                    else:
                        showErrorMessage(3, getLine())
                else:
                    showErrorMessage(1, getLine())
            else:
                showErrorMessage(2, getLine())
        else:
            showErrorMessage(5, getLine())
    else:
        print ""
        #error de sintaxis, fin de ejecucion

#<elseif> ::= "else" "{" <body> "}"
def elseif(PosX_jmptrue ):
    '''
        Validates this grammar: #<elseif> ::= "else" "{" <body> "}"
    '''
    global InterCode
    global InterCodeIndex
    PosY_jmpfalse= 0
    if exigir("else"):
        InterCode.append(JMP)
#       InterCode[ InterCodeIndex ] = JMP
        InterCodeIndex += 1
        InterCode.append('')
        PosY_jmpfalse = InterCodeIndex
        InterCodeIndex += 1
        InterCode[ PosX_jmptrue ] = InterCodeIndex
        if exigir("{"):
            body()
            if not exigir("}"):
                showErrorMessage(3, getLine())
            InterCode[ PosY_jmpfalse ] = InterCodeIndex
        else:
            showErrorMessage(1, getLine())
    else:
        showErrorMessage(4, getLine())


#<while expression> ::= "while" "(" <conditional> ")" "{" <body> "}"
def while_expression():
    '''
        Validates this grammar: <while expression> ::= "while" "(" <conditional> ")" "{" <body> "}"
    '''
    global InterCode
    global InterCodeIndex
    PosX_jmptrue=int()
    PosY_beginWhile=int()
    if exigir("while"):
        PosY_beginWhile = InterCodeIndex
        InterCode.append(IF)
        InterCodeIndex += 1
        if exigir("("):
            conditional()
            if exigir(")"):
                InterCode.append(JMP)
                InterCodeIndex += 1
                InterCode.append('')
                PosX_jmptrue = InterCodeIndex
                InterCodeIndex += 1
                if exigir("{"):
                    body()
                    if not exigir("}"):
                        showErrorMessage(3, getLine())
                        #error de sintaxis, fin de ejecucion
                    InterCode.append(JMP)
                    InterCodeIndex += 1
                    InterCode.append(PosY_beginWhile)
                    InterCodeIndex += 1
                    InterCode[ PosX_jmptrue ] = InterCodeIndex
                else:
                    showErrorMessage(1, getLine())
                    #error de sintaxis, fin de ejecucion
            else:
                showErrorMessage(2, getLine())
                #error de sintaxis, fin de ejecucion
        else:
          showErrorMessage(5, getLine())
          #error de sintaxis, fin de ejecucion
    else:
        showErrorMessage(4, getLine())


#<iterate expression> ::= "iterate" "(" <number> ")" "{" <body> "}"
def iterate_expression():
    '''
        Validates this grammar: <iterate expression> ::= "iterate" "(" <number> ")" "{" <body> "}"
    '''
    global InterCode
    global InterCodeIndex
    Iteration_Number=int()
    PosX_jmptrue=int()
    PosY_beginIterate=int()
    PosIteration_Number=int()
    if exigir("iterate"):
        if exigir("("):
            Iteration_Number=(int(current()))
            currentTokenMod(1)
            if exigir(")"):
                if exigir("{"):
                    start=getCurrentIndexToken()
                    for i in range(Iteration_Number):
                        setCurrentTokenMod(start)
                        body()
                    if not exigir("}"):
                        showErrorMessage(3, getLine())
                        #error de sintaxis, fin de ejecucion
                else:
                    showErrorMessage(1, getLine())
                    #error de sintaxis, fin de ejecucion
            else:
                showErrorMessage(2, getLine())
                #error de sintaxis, fin de ejecucion
        else:
            showErrorMessage(5, getLine())
            #error de sintaxis, fin de ejecucion
    else:
        showErrorMessage(4, getLine())



#<conditional> ::= <simple condition> | <composed condition>
def conditional():
    '''
        Validates this grammar: <conditional> ::= <simple condition> | <composed condition>
    '''
    jumps=0
    while not (leer(")") or leer("||") or leer("&&")):
        currentTokenMod(1)
        jumps-=1
    if leer(")"):
        if jumps==-2:
            currentTokenMod(jumps)
            not_condition()
        else:
            currentTokenMod(jumps)
            simple_condition()
    else:
        composed_condition(jumps)

#<simple condition> ::=
#  "frontIsClear"
#  | "frontIsBlocked"
#  | "leftIsClear"
#  | "leftIsBlocked"
#  | "rightIsClear"
#  | "rightIsBlocked"
#  | "nextToABeeper"
#  | "notNextToABeeper"
#  | "anyBeepersInBeeperBag"
#  | "noBeepersInBeeperBag"
#  | "facingNorth"
#  | "facingSouth"
#  | "facingEast"
#  | "facingWest"
#  | "notFacingNorth"
#  | "notFacingSouth"
#  | "notFacingEast"
#  | "notFacingWest"
#  | "frontIsFull"
#  | "frontIsNotFull"
#  | "amIAlone"
#  | "amINotAlone"
#  | "isFather"
#  | "isNotFather"
#  | "isSon"
#  | "isNotSon"
#  | "isDescendant"
#  | "isNotDescendant"

def simple_condition():
    '''
        Validates this grammar:
            <simple condition> ::=
                                    "frontIsClear"
                                    | "frontIsBlocked"
                                    | "leftIsClear"
                                    | "leftIsBlocked"
                                    | "rightIsClear"
                                    | "rightIsBlocked"
                                    | "nextToABeeper"
                                    | "notNextToABeeper"
                                    | "anyBeepersInBeeperBag"
                                    | "noBeepersInBeeperBag"
                                    | "facingNorth"
                                    | "facingSouth"
                                    | "facingEast"
                                    | "facingWest"
                                    | "notFacingNorth"
                                    | "notFacingSouth"
                                    | "notFacingEast"
                                    | "notFacingWest"
                                    | "frontIsFull"
                                    | "frontIsNotFull"
                                    | "amIAlone"
                                    | "amINotAlone"
                                    | "isFather"
                                    | "isNotFather"
                                    | "isSon"
                                    | "isNotSon"
                                    | "isDescendant" 
                                    | "isNotDescendant" 
    '''
    global Intercode
    global InterCodeIndex
    if leer("frontIsClear"):
        exigir("frontIsClear")
        InterCode.append(FRONT_IS_CLEAR)
        InterCodeIndex += 1
    elif leer("frontIsBlocked"):
        exigir("frontIsBlocked")
        InterCode.append(FRONT_IS_BLOCKED)
        InterCodeIndex += 1
    elif leer("leftIsClear"):
        exigir("leftIsClear")
        InterCode.append(LEFT_IS_CLEAR)
        InterCodeIndex += 1
    elif leer("leftIsBlocked"):
        exigir("leftIsBlocked")
        InterCode.append(LEFT_IS_BLOCKED)
        InterCodeIndex += 1
    elif leer("rightIsClear"):
        exigir("rightIsClear")
        InterCode.append(RIGHT_IS_CLEAR)
        InterCodeIndex += 1
    elif leer("rightIsBlocked"):
        exigir("rightIsBlocked")
        InterCode.append(RIGHT_IS_BLOCKED)
        InterCodeIndex += 1
    elif leer("nextToABeeper"):
        exigir("nextToABeeper")
        InterCode.append(NEXT_TO_A_BEEPER)
        InterCodeIndex += 1
    elif leer("notNextToABeeper"):
        exigir("notNextToABeeper")
        InterCode.append(NOT_NEXT_TO_A_BEEPER)
        InterCodeIndex += 1
    elif leer("anyBeepersInBeeperBag"):
        exigir("anyBeepersInBeeperBag")
        InterCode.append(ANY_BEEPERS_IN_BEEPER_BAG)
        InterCodeIndex += 1
    elif leer("noBeepersInBeeperBag"):
        exigir("noBeepersInBeeperBag")
        InterCode.append(NO_BEEPERS_IN_BEEPER_BAG)
        InterCodeIndex += 1
    elif leer("facingNorth"):
        exigir("facingNorth")
        InterCode.append(FACING_NORTH)
        InterCodeIndex += 1
    elif leer("facingSouth"):
        exigir("facingSouth")
        InterCode.append(FACING_SOUTH)
        InterCodeIndex += 1
    elif leer("facingEast"):
        exigir("facingEast")
        InterCode.append(FACING_EAST)
        InterCodeIndex += 1
    elif leer("facingWest"):
        exigir("facingWest")
        InterCode.append(FACING_WEST)
        InterCodeIndex += 1
    elif leer("notFacingNorth"):
        exigir("notFacingNorth")
        InterCode.append(NOT_FACING_NORTH)
        InterCodeIndex += 1
    elif leer("notFacingSouth"):
        exigir("notFacingSouth")
        InterCode.append(NOT_FACING_SOUTH)
        InterCodeIndex += 1
    elif leer("notFacingEast"):
        exigir("notFacingEast")
        InterCode.append(NOT_FACING_EAST)
        InterCodeIndex += 1
    elif leer("notFacingWest"):
        exigir("notFacingWest")
        InterCode.append(NOT_FACING_WEST)
        InterCodeIndex += 1
    elif leer("frontIsFull"):
        exigir("frontIsFull")
        InterCode.append(FRONT_IS_FULL)
        InterCodeIndex += 1
    elif leer("frontIsNotFull"):
        exigir("frontIsNotFull")
        InterCode.append(FRONT_IS_NOT_FULL)
        InterCodeIndex += 1
    elif leer("amIAlone"):
        exigir("amIAlone")
        InterCode.append(AM_I_ALONE)
        InterCodeIndex += 1
    elif leer("amINotAlone"):
        exigir("amINotAlone")
        InterCode.append(AM_I_NOT_ALONE)
        InterCodeIndex += 1
    elif leer("isFather"):
        exigir("isFather")
        InterCode.append(IS_FATHER)
        InterCodeIndex += 1
    elif leer("isNotFather"):
        exigir("isNotFather")
        InterCode.append(IS_NOT_FATHER)
        InterCodeIndex += 1
    elif leer("isSon"):
        exigir("isSon")
        InterCode.append(IS_SON)
        InterCodeIndex += 1
    elif leer("isNotSon"):
        exigir("isNotSon")
        InterCode.append(IS_NOT_SON)
        InterCodeIndex += 1
    elif leer("isDescendant"):
        exigir("isDescendant")
        InterCode.append(IS_DESCENDANT)
        InterCodeIndex += 1
    elif leer("isNotDescendant"):
        exigir("isNotDescendant")
        InterCode.append(IS_NOT_DESCENDANT)
        InterCodeIndex += 1
    else:
        showErrorMessage(0, getLine())

def composed_condition(jumps):
    '''
        Validates if the conditions is an "or" or an "and" and call the proper function, if none, show an error
    '''
    if leer("||"):
        or_condition(jumps)
    elif leer("&&"):
        and_condition(jumps)
    else:
        showErrorMessage(0, getLine())


def or_condition(jumps):
    '''
        Validates the or condition, if contains a "not" condition the proper function is called
    '''
    global InterCodeIndex
    InterCode.append(OR)
    InterCodeIndex+=1
    if jumps==-2:
        currentTokenMod(jumps)
        not_condition()
    else:
        currentTokenMod(jumps)
        simple_condition()
    exigir("||")
    if leer("!"):
        not_condition()
    else:
        simple_condition()


def and_condition(jumps):
    '''
        Validates de "and" condition, if contains a "not" condtion, the proper function is called
    '''
    global InterCodeIndex
    InterCode.append(AND)
    InterCodeIndex+=1
    if jumps==-2:
        currentTokenMod(jumps)
        not_condition()
    else:
        currentTokenMod(jumps)
        simple_condition()
    exigir("&&")
    if leer("!"):
        not_condition()
    else:
        simple_condition()


def not_condition():
    '''
        Validates the "not" condtion
    '''
    global InterCodeIndex
    exigir("!")
    InterCode.append(NOT)
    InterCodeIndex+=1
    simple_condition()

#<clone> ::= "clone" "("<customer function>")"

def clone():
    '''
        Validates this grammar: <clone> ::= "clone" "("<customer function>")"
    '''
    global InterCodeIndex
    if exigir("clone"):
        if exigir("("):
            InterCode.append(CLONE)
            InterCodeIndex+=1
            customer_function()
            if not exigir(")"):
                showErrorMessage(2, getLine())
        else:
            showErrorMessage(5, getLine())
