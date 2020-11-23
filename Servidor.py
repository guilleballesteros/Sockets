from threading import Thread, Semaphore, Lock
import socket
import random
import os, os.path
from time import sleep 

class Cliente(Thread):
    def __init__(self, socket_cliente, datos_cliente, nombre_cliente, palabra):
        Thread.__init__(self)
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

def comprobar(correo):
    try:
        comprobacion=False
        f=open("ficheros/Usuarios.txt","r")
        for linea in f:
            print(linea)
            print(correo)
            if (linea == correo):
                comprobacion=True
        f.close()
        return comprobacion
    except:
        print("Fichero no encontrado")

turnos=Semaphore(2)
mutex=Lock()
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("", 9999))
server.listen(1)
Usuarios_conectados=[]

    
# bucle para atender clientes
while True:
    # Se espera a un cliente
    socket_cliente, datos_cliente = server.accept()
    # Se mira si quiere iniciar sesion o registrarse
    while True:
        eleccion=socket_cliente.recv(1024).decode()
        datos=eleccion.split(';')
        tipo=datos[0]
        correo=datos[1]
        print(tipo)
        if(tipo=='I'):
            comp=comprobar(correo) 
            if(comp):
                socket_cliente.send("A".encode())
                break
            else:
                socket_cliente.send("D".encode())
        else:
            comp=comprobar(correo)
            if(comp):
                socket_cliente.send("D".encode())
            else:
                f=open("ficheros/Usuarios.txt","a")
                f.write(correo)
                f.write("\n")
                socket_cliente.send("A".encode())
                f.close()
    print("Exito")



    # elif(tipos=='R'):


    # palabra=random.choice(lista_palabras)
    # while (palabra in lista_elegidas):
    #     palabra=random.choice(lista_palabras)
    # lista_elegidas.append(palabra)
    # hilo = Cliente(socket_cliente, datos_cliente, nom, palabra)
    # hilo.start()
