#Arantxa Viladomat Morales
#Alma Lorena Gonzalez Lopez
#Maya Alba Perez
import sys
'''
    This module contains the lexicographical functionality. Reads from the inputnew.txt file
    to gather all the valid tokens fails if an invalid tokens is read.
    Also writes the output (list of tokens) to the output.txt file
'''
inp = open('inputnew.txt','r')
out = open('output.txt', 'w')
tokens_dic = {'(': 'PA', ')': 'PC', '{': 'LLA', '}': 'LLC','!':'NOT','0':'CAD','1':'NUM', '&&':'AND', '||':'OR'}
symbol_table = list()
line= 1
tokens=list()
syntaxError=False


def getNext():
    '''
        This method gets the next character available in the inputnew.txt file 
    '''
    c = inp.read(1)
    if not c:
      return False
    return c

def isValidChar(ch):
    '''
        This method checks if the receive character is one of the valid character "(" or ")" or 
        "{" or "}"  or "!"
        Return True if a valid charachter is read False otherwise  
    '''
    if '(' in ch or ')' in ch or '{' in ch or '}' in ch or '!' in ch:
        return True
    else:
        return False

def insertToken(buff):
    '''
        Appends to the symbol table the receive buffer
    '''
    if buff.isalpha():
        symbol_table.append([tokens_dic.get('0'),buff,line])
    elif buff.isdigit():
        symbol_table.append([tokens_dic.get('1'),buff,line])
    else:
        if tokens_dic.get(buff):
            symbol_table.append([tokens_dic.get(buff),buff,line])
        else:
            symbol_table.append(['ERR',buff,line])

def addOne():
    '''
        Adds 1 to the line that is being read
    '''
    global line
    line +=1

def double(ch, buff, special):
    '''
       Adds to the symbol table the buffer in case that
       2 of the special characters were read, does nothing otherwise         
    '''
    buff += ch
    ch=getNext()
    if special in ch:
        buff += ch
        ch =getNext()
        tokens.append(buff)
        out.write(buff + '\n')
        insertToken(buff)
        buff = ""
        start(ch)
    else: 
        buff = ""
        start(ch)

def ifError(x):
    '''
        This method checks if there passed list contains an ERR statement
    '''
    global syntaxError
    if x[0]=="ERR":
        syntaxError=True
        print "Syntax error: symbol:", x[1], " detected on line", x[2]

def checkErrors():
    '''
        Check if the symbol_table contains any error and throws an error message
    '''
    map(ifError,symbol_table)

def start(ch):
    '''
        This method is the main loop of the progrmas reads character by character
        and classify them in ordet to get the valid tokkens an add the to the symbol table
    '''
    if ch:
        buff = ""
        if isValidChar(ch):
            buff += ch
            ch=getNext()
            tokens.append(buff)
            out.write(buff + '\n')
            insertToken(buff)
            buff = ""
            start(ch)
        elif ch.isalpha():
#            print "is alpha:",ch 
            buff += ch
            ch = getNext()
            while ch.isalpha():
                  buff += ch
                  ch = getNext()
            tokens.append(buff)
            out.write(buff + '\n')
            insertToken(buff)
            buff = ""
            start(ch)
        elif ch.isdigit():
            buff += ch
            ch=getNext()
            while ch.isdigit(): 
                buff += ch  
                ch=getNext()
            tokens.append(buff)
            out.write(buff + '\n')
            insertToken(buff)
            buff = ""
            start(ch)
        elif '&' in ch:
            double(ch,buff,'&')
        elif '|' in ch:
            double(ch,buff,'|')
        elif ' ' in ch:
            ch=getNext()
            start(ch)
        elif '\n' in ch:
            addOne()
            ch=getNext()
            start(ch)
        else:
            if ch:
                buff += ch
                insertToken(buff)
                start(getNext())
            elif ch=='':
                print "EOF!!"
    else:
        checkErrors()
        if(syntaxError):
            sys.exit()
    return tokens