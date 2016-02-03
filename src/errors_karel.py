import sys

aErrorTable={1:'Falta llave izquierda, %s',
             2:'Falta parentesis derecho, %s',
             3:'Falta llave derecha, %s',
             4:'Error en palabra reservada, %s',
             5:'Falta parentesis izquierda, %s',
             6:'Funcion no definida, %s'}

def showErrorMessage(message, line=None):
    '''
       This method receives an index an returns a message if the index
       does not belongs to the Error Table
    '''
    if message in aErrorTable:
        print aErrorTable[message] % str(line)
    else:
        print "The error code was not found"
    sys.exit(1)

