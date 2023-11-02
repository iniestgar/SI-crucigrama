
class Variable:
    def __init__(self,tablero,posFinal,posConst,tipo,tamPal):
        self.palabra = []
        self.tam = tamPal
        self.tipo = tipo
        self.inicio = posFinal-tamPal+1
        self.FILA = 0
        self.COL = 0
        
        if tipo == 'f':
            self.FILA = posConst
            for i in range(self.inicio,posFinal+1):
                self.palabra.append(tablero.getCelda(self.FILA,i))
        elif tipo == 'c':
            self.COL = posConst
            for i in range(self.inicio,posFinal+1):
                self.palabra.append(tablero.getCelda(i,self.COL))
        else:
            print("Error: Tipo incorrecto")
            
    def getTam(self):
        return self.tam
    
    def getPosicion(self, posicion):
        if posicion == 'inicio':      
            if self.tipo == 'c':
                return self.inicio, self.COL
            else:
                return self.FILA, self.inicio
        elif posicion == 'final':
            if self.tipo == 'c':
                return (self.inicio+self.tam-1),self.COL
            else:
                return self.FILA, (self.inicio+self.tam-1)
        else:
            print(f'Error: {posicion} no es correcto')
            return -1
    def getLista(self):
        return self.palabra
    
    def setPalabra(self,pal):
        self.palabra = list(pal)
        
    def getTipo(self):
        return self.tipo
    
    def __str__(self):
        return ''.join(self.palabra)
            