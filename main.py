import pygame
import tkinter
from tkinter import *
from tkinter.simpledialog import *
from tkinter import messagebox as MessageBox
from tablero import *
from dominio import *
from variable import *
from pygame.locals import *
from copy import copy

GREY=(190, 190, 190)
NEGRO=(100,100, 100)
BLANCO=(255, 255, 255)

MARGEN=5 #ancho del borde entre celdas
MARGEN_INFERIOR=60 #altura del margen inferior entre la cuadrícula y la ventana
TAM=60  #tamaño de la celda
FILS=5 # número de filas del crucigrama
COLS=6 # número de columnas del crucigrama

LLENA='*' 
VACIA='-'

#########################################################################
# Detecta si se pulsa el botón de FC
######################################################################### 
def pulsaBotonFC(pos, anchoVentana, altoVentana):
    if pos[0]>=anchoVentana//4-25 and pos[0]<=anchoVentana//4+25 and pos[1]>=altoVentana-45 and pos[1]<=altoVentana-19:
        return True
    else:
        return False
    
######################################################################### 
# Detecta si se pulsa el botón de AC3
######################################################################### 
def pulsaBotonAC3(pos, anchoVentana, altoVentana):
    if pos[0]>=3*(anchoVentana//4)-25 and pos[0]<=3*(anchoVentana//4)+25 and pos[1]>=altoVentana-45 and pos[1]<=altoVentana-19:
        return True
    else:
        return False
    
######################################################################### 
# Detecta si se pulsa el botón de reset
######################################################################### 
def pulsaBotonReset(pos, anchoVentana, altoVentana):
    if pos[0]>=(anchoVentana//2)-25 and pos[0]<=(anchoVentana//2)+25 and pos[1]>=altoVentana-45 and pos[1]<=altoVentana-19:
        return True
    else:
        return False
    
######################################################################### 
# Detecta si el ratón se pulsa en la cuadrícula
######################################################################### 
def inTablero(pos):
    if pos[0]>=MARGEN and pos[0]<=(TAM+MARGEN)*COLS+MARGEN and pos[1]>=MARGEN and pos[1]<=(TAM+MARGEN)*FILS+MARGEN:        
        return True
    else:
        return False
    
######################################################################### 
# Busca posición de palabras de longitud tam en el almacen
######################################################################### 
def busca(almacen, tam):
    enc=False
    pos=-1
    i=0
    while i<len(almacen) and enc==False:
        if almacen[i].tam==tam: 
            pos=i
            enc=True
        i=i+1
    return pos
    
######################################################################### 
# Crea un almacen de palabras
######################################################################### 
def creaAlmacen():
    f= open('d0.txt', 'r', encoding="utf-8")
    lista=f.read()
    f.close()
    listaPal=lista.split()
    almacen=[]
   
    for pal in listaPal:        
        pos=busca(almacen, len(pal)) 
        if pos==-1: #no existen palabras de esa longitud
            dom=Dominio(len(pal))
            dom.addPal(pal.upper())            
            almacen.append(dom)
        elif pal.upper() not in almacen[pos].lista: #añade la palabra si no está duplicada        
            almacen[pos].addPal(pal.upper())           
    
    return almacen

######################################################################### 
# Imprime el contenido del almacen
######################################################################### 
def imprimeAlmacen(almacen):
    for dom in almacen:
        print (dom.tam)
        lista=dom.getLista()
        for pal in lista:
            print (pal, end=" ")
        print()
        
#########################################################################
# Crear restricciones
#########################################################################

"""
def restriccionCasillaVacia(factibles,podados,posCruzadaFil,posCruzadaCol,posCol,posFila):
    domFactInf = factibles[posCol]
    domFactSup = factibles[posFila]
    posCruzadaSup = posCruzadaFil
    posCruzadaInf = posCruzadaCol
    print(f'posCruzadaSup: {posCruzadaSup}')
    print(f'posCruzadaInf: {posCruzadaInf} \n')
    
    for i in range(2):
        for posPalSup,palFactSup in enumerate(domFactSup.getLista()):
            palPodar = palFactSup
            encontrado = False
            print(f'---posPalSup: {posPalSup}    palFactSup: {palFactSup}')
            
            for posPalInf,palFactInf in enumerate(domFactInf.getLista()):
                print(f'posPalInf: {posPalInf}   palFactInf: {palFactInf}')                
                if palFactSup[posCruzadaSup] == palFactInf[posCruzadaInf] and i == 0:
                    encontrado = True
            #Si no ha encontrado una palabra con la misma letra en posCruzada
            #se quita en la variable posFila/posCol la palabra de factibles
            #y se añade al apartado podados
            if encontrado  == False:
                if i == 0:
                    factibles[posFila].getLista().remove(palPodar)
                    podados[posFila].addPal(palPodar)
                elif i == 1:
                    factibles[posCol].getLista().remove(palPodar)
                    podados[posCol].addPal(palPodar)
        if i == 0:
            #Ahora se comprobarán que palabras de la variable columna se quitan
            domFactSup = factibles[posCol]
            domFactInf = factibles[posFila]
            posCruzadaSup = posCruzadaCol
            posCruzadaInf = posCruzadaFil
            print('\n --------Intercambio de dominios y posCruzadas-------')
            print(f'posCruzadaSup: {posCruzadaSup}')
            print(f'posCruzadaInf: {posCruzadaInf}')
"""



def creaRestricciones(variables,factibles,podados):
    varFilas = [var for var in variables if var.getTipo() == 'f']
    varCols = [var for var in variables if var.getTipo() == 'c']
    for posFila,fila in enumerate(varFilas):
        print(f"Variable fila {fila.getLista()}")

        for posCol,col in enumerate(varCols): #Sumar siempre a posCol len(varFilas) para trabajar con el parametro 'variables'
            print(f"\t Columna={col.getLista()}")
            if col.getPosicion('inicio')[0]<= fila.getPosicion('inicio')[0] <= col.getPosicion('final')[0] and fila.getPosicion('inicio')[1] <= col.getPosicion('inicio')[1] <= fila.getPosicion('final')[1]:
                posCruzadaCol = col.getPosicion('inicio')[1]
                posCruzadaFila = fila.getPosicion('inicio')[0]
                
                #Tienen que ser IGUALES, sino, HAY ERROR
                if col.getLista()[posCruzadaFila-col.getPosicion('inicio')[0]] == fila.getLista()[posCruzadaCol-fila.getPosicion('inicio')[1]]:
                    print(f"Coinciden Pos={posCruzadaFila-col.getPosicion('inicio')[0]} Valor={col.getLista()[posCruzadaFila-col.getPosicion('inicio')[0]]} = Pos={posCruzadaCol-fila.getPosicion('inicio')[1]} Valor={fila.getLista()[posCruzadaCol-fila.getPosicion('inicio')[1]]}")
                
                #if col.getLista()[posCruzadaFila-col.getPosicion('inicio')[0]] == VACIA and fila.getLista()[posCruzadaCol-fila.getPosicion('inicio')[1]] == VACIA:
                    



"""
def estaRestringido(a,b,domFactibles,domPodados):
    
    restricciones = creaRestricciones(factibles)
"""
    
"""
def AC3():

    varFilas = [var for var in variables if var.getTipo() == 'f']
    #varCols = [var for var in variables if var.getTipo() == 'c']
    for posFila,varFila in enumerate(varFilas):
        #Variables columna que coinciden con la fila
        for posCol,var in enumerate(variables):
            #Mientras sea columna y la fila de la variable fila tenga a la variable columna entre sus valores
            if var.getTipo() == 'c' and var.getPosicion('inicio')[0]<= varFila.getPosicion('inicio')[0] <= var.getPosicion('final')[0] and varFila.getPosicion('inicio')[1] <= var.getPosicion('inicio')[1] <= varFila.getPosicion('final')[1]:
                
                print('posicion de la pos cruzada en VarCol: {}'.format(varFila.getPosicion('inicio')[0]))
                print('posicion de la pos cruzada en VarFila: {}'.format(var.getPosicion('inicio')[1]))
                #En la posicion de la columna donde coinciden
                posCruzadaCol = varFila.getPosicion('inicio')[0]-var.getPosicion('inicio')[0] #La posicion del caracter en "var" es la columna de "varFila"
                posCruzadaFil = var.getPosicion('inicio')[1]-varFila.getPosicion('inicio')[1] #La posicion del caracter en "varFila" es la columna de "var"
                if varFila.getLista()[posCruzadaFil] == VACIA:
                    print('##########################')
                    print(f'Variable fila:{posFila}            Variable columna: {posCol}')
                    print('Posicion: {}                        Posicion: {}'.format(varFila.getPosicion('inicio'),var.getPosicion('inicio')))
                    restriccionCasillaVacia(factibles,podados,posCruzadaFil,posCruzadaCol,posCol,posFila)
                    
                #elif varFila.getLista()[posCruzada].isalpha() == True:
                    
                #else:
                    
    k = 0
    for dom in factibles:
        print(f'{k} {dom.getLista()}')
        k+=1
    k = 0
    for dom in podados:
        print(f'{k} {dom.getLista()}')
        k+=1
        
"""               
                
            
        
#########################################################################
# Crear variables
#########################################################################

    
def dominios(variables,almacen):
    #En ambas listas las posiciones corresponden a la posición variable en la lista "variables"
    """
        Cada dominio de palabras en la posicion i de podados y factibles tienen el mismo tamaño de palabra 
    """
    podados = [] #Valores que no pueden entrar en la variable porque el contenido limita las opciones
    factibles = [] #Valores que se ajustan a los caracteres que hay en el tablero

    print(str(len(variables)) + "\n Almacen:")

    imprimeAlmacen(almacen)
    for i, var in enumerate(variables):
        domAlmacen=copy(almacen[busca(almacen,var.getTam())])
        #print(f'domAlmacen: {domAlmacen.getLista()}')
        #print(f'palagra: {var.getLista()}')
        #Guardamos la posicion y el caracter de la palabra de la primera de variables
        listaCarVar=[(pos,c) for pos,c in enumerate(var.getLista()) if c.isalpha()==True]
        
        domFact = Dominio(var.getTam())
        domPod = Dominio(var.getTam())
        
        for pal in domAlmacen.getLista():
            #Guardamos la POSICION y el CARACTER de la palabra del almacen en listaCarPal
            listaCarPal = [(pos,c) for pos,c in enumerate(pal)]
            contaCar = 0
            #print(f'Lista de caracteres de la palabra del dominio: {listaCarPal}')
            #print(f'Lista de caracteres de la palabra de la variable: {listaCarVar} \n')
            #Comparamos si se corresponden los mismo CARACTERES en las mismas POSICIONES
            for j in range(len(listaCarVar)):
                if listaCarVar[j] in listaCarPal:
                    contaCar+=1
                    #print(f'los caracteres {listaCarVar} estan en {listaCarPal}')
              
            if contaCar == len(listaCarVar):
                domFact.addPal(pal)
            else:
                domPod.addPal(pal)
        factibles.insert(i,domFact)
        podados.insert(i,domPod)
    """
    k = 0
    for i in factibles:
        print(f'{k} Dominio factible :{i.getLista()}')
        k+=1
    k = 0
    for j in podados:
       print(f'{k} Dominio podado :{j.getLista()}')
       k+=1
    """
    return factibles, podados
            
def creaVariables(tablero):
    variables = [] #Primero son las variables fila
    esCol=False
    esFil=True
    #Cuando pasemos a crear las colummnas cambiamos el valor de las constantes
    iterSup = FILS
    iterInf = COLS
    
    for conta in range(2):
        
        for i in range(iterSup):
            #print('Itera')
            tam = 0

            for j in range(iterInf):
                fila=i
                col=j

                if esCol==True: 
                #Intercambiamos los valores para crear las variables Columna
                    fila=j
                    col=i

                #print(f'Iteración {i}: ({fila}, {col})')
                if tablero.getCelda(fila,col) != LLENA:
                    tam+=1

                    if esFil==True:
                        #print(f'tamaño: {tam}')
                        posFija=fila
                        if j == iterInf-1 or tablero.getCelda(fila,col+1) == LLENA:
                            """SI llega al limite del tablero O si se encuentra una casilla negra en la siguiente columna"""
                            posFinal=col
                            variable = Variable(tablero,posFinal,posFija,"f",tam)
                            variables.append(variable)
                            tam = 0
                        
                    if esCol==True:
                        #print(f'tamaño: {tam}')
                        posFija=col
                        if j == iterInf-1 or tablero.getCelda(fila+1,col) == LLENA:
                            if tam > 1:
                                posFinal=fila
                                variable = Variable(tablero,posFinal,posFija,"c",tam)
                                variables.append(variable)
                            tam = 0

        #Si al crear las variables filas llegamos al final 
        #activamos los flags para crear las columnas e intercambiamos las constantes
        if conta == 0:
            esCol=True
            esFil=False
            iterSup=COLS
            iterInf=FILS
    
    """Imprime: Tamaño de la lista variables y cada par posicion y valor de la lista"""
    print(len(variables))
    for i,var in enumerate(variables):
        print(i,var.getPosicion('inicio'),var.getPosicion('final'),var)
    return variables

#########################################################################
# ForwardChecking
#########################################################################
#def restaura(posVar, var):
    

def forward(var,i,a,tamListVar,factibles,podados):
    for j in range(posVar+1,tamListVar):
        vacio = True
        for b in factibles[j]:
            if estaRestringido(a,b,factibles[j],podados[j]):
                vacio = False
            else:
                podados[j].addPal(b)
                factible[j].getLista().remove(b)
        if vacio == True:
            return False
    return True

def FC(i,variables,factibles,podados):
    
    for a in factibles[i].getLista():
        variables[i].setPalabra(a)
        if i == len(variables):
            return True
        else:
            if forward(variables[i],i,a,len(variables),factibles,podados):
                if FC(i+1,variables,factibles,podados):
                    return True
            #restaura(i,variables[i],factibles,podados)
    return False
        
#########################################################################  
# Principal
#########################################################################
def main():
    root= tkinter.Tk() #para eliminar la ventana de Tkinter
    root.withdraw() #se cierra
    pygame.init()
    
    reloj=pygame.time.Clock()
    
    anchoVentana=COLS*(TAM+MARGEN)+MARGEN
    altoVentana= MARGEN_INFERIOR+FILS*(TAM+MARGEN)+MARGEN
    
    dimension=[anchoVentana,altoVentana]
    screen=pygame.display.set_mode(dimension) 
    pygame.display.set_caption("Practica 1: Crucigrama")
    
    botonFC=pygame.image.load("botonFC.png").convert()
    botonFC=pygame.transform.scale(botonFC,[50, 30])
    
    botonAC3=pygame.image.load("botonAC3.png").convert()
    botonAC3=pygame.transform.scale(botonAC3,[50, 30])
    
    botonReset=pygame.image.load("botonReset.png").convert()
    botonReset=pygame.transform.scale(botonReset,[50,30])
    
    almacen=creaAlmacen()
    factibles=[]
    podados=[]
    game_over=False
    tablero=Tablero(FILS, COLS)
    while not game_over:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:               
                game_over=True
            if event.type==pygame.MOUSEBUTTONUP:                
                #obtener posición y calcular coordenadas matriciales                               
                pos=pygame.mouse.get_pos()                
                if pulsaBotonFC(pos, anchoVentana, altoVentana):
                    print("FC")
                    variables = creaVariables(tablero)
                    factibles, podados = dominios(variables,almacen)
                    restricciones = creaRestricciones(variables,factibles,podados)
                    FC(0,variables,factibles,podados)
                    res=False #aquí llamar al forward checking
                    if res==False:
                        MessageBox.showwarning("Alerta", "No hay solución")                                  
                elif pulsaBotonAC3(pos, anchoVentana, altoVentana):                    
                    print("AC3")
                    variables = creaVariables(tablero)
                elif pulsaBotonReset(pos, anchoVentana, altoVentana):                   
                    tablero.reset()
                elif inTablero(pos):
                    colDestino=pos[0]//(TAM+MARGEN)
                    filDestino=pos[1]//(TAM+MARGEN)                    
                    if event.button==1: #botón izquierdo
                        if tablero.getCelda(filDestino, colDestino)==VACIA:
                            tablero.setCelda(filDestino, colDestino, LLENA)
                        else:
                            tablero.setCelda(filDestino, colDestino, VACIA)
                    elif event.button==3: #botón derecho
                        c=askstring('Entrada', 'Introduce carácter')
                        tablero.setCelda(filDestino, colDestino, c.upper())   
            
        ##código de dibujo        
        #limpiar pantalla
        screen.fill(NEGRO)
        pygame.draw.rect(screen, GREY, [0, 0, COLS*(TAM+MARGEN)+MARGEN, altoVentana],0)
        for fil in range(tablero.getAlto()):
            for col in range(tablero.getAncho()):
                if tablero.getCelda(fil, col)==VACIA: 
                    pygame.draw.rect(screen, BLANCO, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                elif tablero.getCelda(fil, col)==LLENA: 
                    pygame.draw.rect(screen, NEGRO, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                else: #dibujar letra                    
                    pygame.draw.rect(screen, BLANCO, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                    fuente= pygame.font.Font(None, 70)
                    texto= fuente.render(tablero.getCelda(fil, col), True, NEGRO)            
                    screen.blit(texto, [(TAM+MARGEN)*col+MARGEN+15, (TAM+MARGEN)*fil+MARGEN+5])             
        #pintar botones        
        screen.blit(botonFC, [anchoVentana//4-25, altoVentana-45])
        screen.blit(botonAC3, [3*(anchoVentana//4)-25, altoVentana-45])
        screen.blit(botonReset, [anchoVentana//2-25, altoVentana-45])
        #actualizar pantalla
        pygame.display.flip()
        reloj.tick(40)
        if game_over==True: #retardo cuando se cierra la ventana
            pygame.time.delay(500)
    
    pygame.quit()
 
if __name__=="__main__":
    main()
 
