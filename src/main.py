import __builtin__
import meta_rd_karel
from rec_desc_karel import *
from lexicographical import *

__builtin__.aTokensInput=start(getNext())

__builtin__.currentToken=0

'''
    This is the file that executes all the program, all the magic begins by executing the lexicographical component that return
    a set of detected tokens that wil be the input for the recursive-descent this component returned an intermediate code that 
    will be execute by the program and display by the gui. 

    The program needs and input file named "inputnew.txt" and a "world.txt" The inputnew file contains all the instructions that 
    will be executed and the world file contains the description of the world where Aladin will interact.
'''
program()