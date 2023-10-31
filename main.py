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
def creaRestricciones(variables,factibles,podados):
    restricciones = []
    varFilas = [var for var in variables if var.getTipo() == 'f']
    varCols = [var for var in variables if var.getTipo() == 'c']
    #for varFila in varFilas:
     #   for varCol in varCols:
      #      if varCol.getPosicion()[0] <= varFila.getPosicion()[0]+varFila.getTam()-1 and varFila.getPosicion()[] varCol.getPosicion()[1]: 
        
#########################################################################
# Crear variables
#########################################################################

    
def dominios(variables,almacen):
    podados = []
    factibles = []
    print(len(variables))
    for i, var in enumerate(variables):
        domAlmacen=copy(almacen[busca(almacen,var.getTam())])
        #print(f'domAlmacen: {domAlmacen.getLista()}')
        #print(f'palagra: {var.getLista()}')
        #Guardamos la posicion y el caracter de la palabra de la primera de variables
        listaCarVar=[(pos,c) for pos,c in enumerate(var.getLista()) if c.isalpha()==True]
        domFact = Dominio(var.getTam())
        domPod = Dominio(var.getTam())
        
        for pal in domAlmacen.getLista():
            #Guardamos la posicion y el caracter de la palabra del almacen en listaCarPal
            listaCarPal = [(pos,c) for pos,c in enumerate(pal)]
            contaCar = 0
            #print(f'Lista de caracteres de la palabra del dominio: {listaCarPal}')
            #print(f'Lista de caracteres de la palabra de la variable: {listaCarVar} \n')
            #Comparamos si se corresponden los mismo carácteres en las mismas posiciones
            for j in range(len(listaCarVar)):
                if listaCarVar[j] in listaCarPal:
                    contaCar+=1
              
            if contaCar == len(listaCarVar):
              
                if listaCarPal == listaCarVar:
                    domFact.addPal(pal)
            else:
                domPod.addPal(pal)
        factibles.insert(i,domFact)
        podados.insert(i,domPod)
    k = 0
    for i in factibles:
        #print(f'{k} Dominio factible :{i.getLista()}')
        k+=1
    k = 0
    for j in podados:
        #print(f'{k} Dominio podado :{j.getLista()}')
        k+=1
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
            print('Itera')
            tam = 0
            for j in range(iterInf):
                fila=i
                col=j
                if esCol==True: #Intercambiamos los valores para crear las variables Columna
                    fila=j
                    col=i
                print(f'Iteración {i}: ({fila}, {col})')
                if (tablero.getCelda(fila,col) == LLENA or j == iterInf-1) and tam > 0:
                    if esFil==True:
                        posFija=fila
                        posFinal=col-1
                        variable = Variable(tablero,posFinal,posFija,"f",tam)
                    if esCol==True:
                        posFija=col
                        posFinal=fila-1
                        variable = Variable(tablero,posFinal,posFija,"c",tam)
                    
                    variables.append(variable)
                    #print(f'Variable {fila},{col}: {variable}')
                    tam = 0
                #Si en una fila o columna llegamos al final y resulta que solo hay un hueco
                #se crea una nueva variable
                elif j == iterInf-1 and tam==0 and tablero.getCelda(fila,col) != LLENA:
                    if esFil==True:
                        posFija=i
                        posFinal=j-1
                        variable = Variable(tablero,posFinal,posFija,'f',1)
                    if esCol==True:
                        posFija=j
                        posFinal=i-1
                        variable = Variable(tablero,posFinal,posFija,'c',1)
                    variables.append(variable)
                else:
                    tam+=1
            
        #Si al crear las variables filas llegamos al final 
        #activamos los flags para crear las columnas e intercambiamos las constantes
        if conta == 0:
            esCol=True
            esFil=False
            iterSup=COLS
            iterInf=FILS
    print(len(variables))
    return variables

#########################################################################
# ForwardChecking
#########################################################################
#def restaura(posVar, var):
    

def forward(var,posVar,palabra,tamListVar,factibles,podados):
    for j in range(posVar+1,tamListVar):
        vacio = True
        #for b in factibles[j]:
            #if (a,b) in restricciones

def FC(i,variables,factibles,podados):
    
    for a in factibles[i].getLista():
        variables[i].setPalabra(a)
        if i == len(variables):
            return True
        else:
            if forward(variables[i],i,a,len(variables),factibles,podados):
                if FC(i+1,variables,factibles,podados):
                    return True
            #restaura(i,variables[i])
        
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
 
