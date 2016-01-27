from execute import *
'''
    This module is an alternative main to receive an intercode in order to provide a vitual machine functionality. 
    Reads the intecode from the "intercodeFile.txt" 
    Appends all the available tokens (in order) to the interCode list.
'''

interCodeArray=list()
interCodeFile = open('intercodeFile.txt', 'r')
line=interCodeFile.read()
line = line[1 : len(line) - 1]
interCodeArray=line.split(', ')

interCode=list()
for token in interCodeArray:
	if token.isdigit():
		interCode.append(int(token))
	else:
		interCode.append(token[1:-1])
print interCode

#print interCodeArray
executeIntercode(interCode)