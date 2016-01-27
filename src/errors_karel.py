import sys

aErrorTable=dict()
aErrorTable={1:'Falta llave izquierda',
             2:'Falta parentesis derecho',
             3:'Falta llave derecha',
             4:'Error en palabra reservada',
             5:'Falta parentesis izquierda',
             6:'Funcion no definida'}

def showErrorMessage(indexMessage):
    '''
       This method receives an index an returns a message if the index
       does not belongs to the Error Table
    '''
    if (indexMessage<=len(aErrorTable) and indexMessage>0):
        print aErrorTable[indexMessage]
    else:
        print "The code error was not found"
    sys.exit(0)

