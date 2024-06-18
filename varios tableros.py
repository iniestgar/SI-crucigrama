from tablero import Tablero

max_col=7
max_fil=6

(p1,p2)=(1,2)

t1= Tablero(None)
t1.setCelda(max_fil,0,p2)
t1.setCelda(max_fil-1,0,p2)
t1.setCelda(max_fil-2,0,p2)

t1.setCelda(max_fil,2,p1)
t1.setCelda(max_fil,3,p1)

print(t1)

print ("Tableros")

t2= Tablero(None)
t2.setCelda(max_fil,0,p2)
t2.setCelda(max_fil-1,0,p2)
t2.setCelda(max_fil-2,0,p2)

t2.setCelda(max_fil,1,p1)
t2.setCelda(max_fil-1,1,p1)

t2.setCelda(max_fil,5,p1)

print(t2)


t3= Tablero(None)
t3.setCelda(max_fil,0,p2)
t3.setCelda(max_fil-1,0,p2)
t3.setCelda(max_fil-2,0,p1)
t3.setCelda(max_fil-3,0,p2)
t3.setCelda(max_fil-4,0,p2)
t3.setCelda(max_fil-5,0,p2)
t3.setCelda(max_fil-6,0,p1)

t3.setCelda(max_fil,1,p2)
t3.setCelda(max_fil-1,1,p2)

t3.setCelda(max_fil,3,p1)
t3.setCelda(max_fil,4,p1)

t3.setCelda(max_fil,5,p1)
t3.setCelda(max_fil-1,5,p1)
t3.setCelda(max_fil-2,5,p1)



print(t3)

print("Ejercicio: Obtener el valor de la función de evaluación para t1, t2 y t3")
