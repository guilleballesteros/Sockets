from threading import Thread, Semaphore, Lock
import socket
import random
import os, os.path
from time import sleep 

class Cliente(Thread):
    def _init_(self, socket_cliente, datos_cliente, nombre_cliente, palabra):
        Thread._init_(self)
        self.socket = socket_cliente
        self.datos = datos_cliente
        self.nombre=nombre_cliente
        self.intentos=6
        self.escogida=palabra
        self.encontrada=False
      
    def run(self):
        global turnos, mutex
        print(self.nombre+" espera turno para jugar.")
        turnos.acquire()
        print(self.nombre+" ha comenzado a jugar.")
        adivina=['*']*len(self.escogida)
        while(self.intentos>0 and self.encontrada==False):
            letra=self.socket.recv(1024).decode()
            if(letra in self.escogida):
                self.socket.send("s".encode())
                for i in range(len(self.escogida)):
                    if (self.escogida[i]==letra):
                        adivina[i]=letra
            else:
                self.intentos-=1
                self.socket.send("n".encode())
            pal="".join(adivina)
            cadena=pal+";"+str(self.intentos)+";"
            if(self.escogida==pal):
                self.encontrada=True
                cadena+="G;"
                cadena+=self.escogida
            else:
                cadena+="P;"
                cadena+=self.escogida
            sleep(2)
            self.socket.send(cadena.encode())
        if(self.encontrada):
            print(self.nombre+" ha ganado la partida. Puntos: "+str(self.intentos))
            mutex.acquire()
            fichero=open("puntuaciones.txt","a")
            fichero.write(self.nombre+";"+str(self.intentos))
            fichero.write("\n")
            fichero.close()
            mutex.release()
        else:
            print(self.nombre+" ha perdido la partida. Puntos: "+str(self.intentos))
        turnos.release()
        self.socket.close()

def mostrar_rank():
    try:
        fichero=open("puntuaciones.txt","r")
        dicc_jug={}
        for linea in fichero:
            datos=linea.split(';')
            jugador=datos[0]
            puntos=int(datos[1])
            dicc_jug[jugador]=puntos
        fichero.close()
        #Tengo el diccionario, ahora ordeno y muestro
        for item in sorted(dicc_jug, key=dicc_jug.get,reverse=True):
                print('{0:12} ==> {1:2d}'.format(item,dicc_jug[item]))
    except:
        print("Fichero no encontrado")

turnos=Semaphore(2)
mutex=Lock()
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("", 9003))
server.listen(1)
lista_palabras=['internet','programacion','matematicas','fisica','analisis','redes','sistemas','interfaces','servicios','netbeans']
lista_elegidas=[]

#mostramos menu servidor
print("Menú: ")
print("1. Jugar.")
print("2. Mostrar ranking.")
opcion=int(input("Elige una opción: "))
if(opcion==1):
    #eliminamos el fichero de ranking
    if(os.path.isfile("puntuaciones.txt")):
        os.remove("puntuaciones.txt")    
    # bucle para atender clientes
    while True:
        # Se espera a un cliente
        socket_cliente, datos_cliente = server.accept()
        # Se escribe su informacion
        nom=socket_cliente.recv(1024).decode()
        print ("Conectado "+str(datos_cliente))
        palabra=random.choice(lista_palabras)
        while (palabra in lista_elegidas):
            palabra=random.choice(lista_palabras)
        lista_elegidas.append(palabra)
        hilo = Cliente(socket_cliente, datos_cliente, nom, palabra)
        hilo.start()
elif(opcion==2):
    mostrar_rank()
else:
    print("Se ha elegido otra opción. Saliendo del sistema.")