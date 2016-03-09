import __builtin__
import meta_rd_karel
from rec_desc_karel import program
from lexicographical import start, getNext

tokens = start(getNext())
__builtin__.aTokensInput = tokens[0]
__builtin__.tokenLines = tokens[1]

__builtin__.currentToken = 0

'''
    This is the file that executes all the program, all the magic begins by executing the lexicographical component that return
    a set of detected tokens that wil be the input for the recursive-descent this component returned an intermediate code that 
    will be execute by the program and display by the gui. 

    The program needs and input file named "input.txt" and a "world.txt" The inputnew file contains all the instructions that 
    will be executed and the world file contains the description of the world where Aladin will interact.
'''
program()