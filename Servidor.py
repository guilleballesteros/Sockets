from threading import Thread, Semaphore, Lock
import socket
import random
import os, os.path
from time import sleep 

class Cliente(Thread):
    def __init__(self, socket_cliente, datos_cliente, correo):
        Thread.__init__(self)
        self.socket = socket_cliente
        self.datos = datos_cliente
        self.correo=correo
      
    def run(self):
        while(True):
            print(self.correo)
            global turnos, mutex
            opcion=self.socket.recv(1024).decode()
            # comprueba el tipo de opcion que ha elegido el cliente
            if(opcion=='I'):
                grupo = self.socket.recv(1024).decode()
                # coprueba que no haya integrantes registrados en otro grupo
                if(comprobacionRep(grupo)):
                    # comprueba que los integrantes esten registrados
                    if(comprobacionGrupo(grupo)):
                        mutex.acquire()
                        f = open("ficheros/Grupos.txt",'a')
                        f.write(grupo+"\n")
                        self.socket.send("A;Grupo registrado".encode())
                        f.close()
                        mutex.release()
                    else:
                        self.socket.send("D;Ya existe un grupo con ese nombre o no estan todos los usuarios registrados".encode())
                else:
                    self.socket.send("D; ya hay un grupo con 1 o más de estos integrantes registrados".encode())
            elif(opcion=='L'):
                print("")
            elif(opcion=='M'):
                print("")
            elif(opcion=='E'):
                print("")
            elif(opcion=='C'):
                print("Cliente ha cerrado sesion")
                self.socket.close()
                Usuarios_conectados.remove(self.correo)
                break
        
           



        # print(self.nombre+" espera turno para jugar.")
        # turnos.acquire()
        # print(self.nombre+" ha comenzado a jugar.")
        # adivina=['*']*len(self.escogida)
        # while(self.intentos>0 and self.encontrada==False):
        #     letra=self.socket.recv(1024).decode()
        #     if(letra in self.escogida):
        #         self.socket.send("s".encode())
        #         for i in range(len(self.escogida)):
        #             if (self.escogida[i]==letra):
        #                 adivina[i]=letra
        #     else:
        #         self.intentos-=1
        #         self.socket.send("n".encode())
        #     pal="".join(adivina)
        #     cadena=pal+";"+str(self.intentos)+";"
        #     if(self.escogida==pal):
        #         self.encontrada=True
        #         cadena+="G;"
        #         cadena+=self.escogida
        #     else:
        #         cadena+="P;"
        #         cadena+=self.escogida
        #     sleep(2)
        #     self.socket.send(cadena.encode())
        # if(self.encontrada):
        #     print(self.nombre+" ha ganado la partida. Puntos: "+str(self.intentos))
        #     mutex.acquire()
        #     fichero=open("puntuaciones.txt","a")
        #     fichero.write(self.nombre+";"+str(self.intentos))
        #     fichero.write("\n")
        #     fichero.close()
        #     mutex.release()
        # else:
        #     print(self.nombre+" ha perdido la partida. Puntos: "+str(self.intentos))
        # turnos.release()
        # self.socket.close()

def comprobacionRep(dato):
    comp = True
    datos=dato.split(";")
    grupo=datos[1]
    integrantes=grupo.split(":")
    f=open("ficheros/Grupos.txt",'r')
    print (comp)
    # recorre el fichero y comprueba que no haya integrantes en otro grupo registrado
    for linea in f:
        datostxt=linea.split(";")
        grupotxt=datostxt[1].split(":")
        for integrante in integrantes:
            if(integrante in grupotxt):
                comp=False
    return comp

def comprobacionGrupo(dato):
    comp = False
    datos=dato.split(";")
    nombre=datos[0]
    grupo=datos[1]
    integrantes=grupo.split(":")
    f=open("ficheros/Grupos.txt",'r')
    print (comp)
    # comprueba que el fichero este vacio o no
    if(f.read() == ''):
        comp= True
    else:
        # recorre el fichero y comprueba que esten registrados y que el nombre no coincida
        for linea in f:
            datoG=linea.split(";")
            nombreG=datoG[0]
            print(nombre)
            print(nombreG)
            if(nombre!=nombreG):
                for integrante in integrantes:
                    comp = comprobacionCorreo(integrante)
                    if ( not comp ):
                        return False
    f.close()
    return comp


        
# comprueba si hay algun usuario con el mismo nombre en el fichero
def comprobacionCorreo(correo):
    comp=False
    f=open("ficheros/Usuarios.txt",'r')
    for linea in f:
        dato=linea.split(";")
        if (dato[0] == correo):
            print( dato[0])
            print (correo)
            comp=True
    f.close()
    return comp

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
        #Se mira se se inicia sesion o se registra
        if(tipo=='I'):
            #Se mira si coinciden los correos
            comp=comprobacionCorreo(correo)
            #si coinciden acepta el inicio y sale del bucle
            if(comp):
                if(correo in Usuarios_conectados):
                    socket_cliente.send("D;Ya hay un usuario registrado con ese correo".encode())
                else:
                    socket_cliente.send("A; has iniciado sesion ".encode())
                    Usuarios_conectados.append(correo)
                    break
            #Si no se sigue en el bucle hasta que se inicie sesion
            else:
                socket_cliente.send("D;No hay ningun correo registrado que coincida con el introducido".encode())
        elif(tipo=='R'):
            comp=comprobacionCorreo(correo)
            #si coinciden da error
            if(comp):
                socket_cliente.send("D;Ya existe un correo registrado".encode())
            #si no coinciden registra el nuevo correo
            else:
                f=open("ficheros/Usuarios.txt","a")
                f.write(correo)
                f.write(";\n")
                socket_cliente.send("A;Correo registrado".encode())
                f.close()
                break
        else:
            socket_cliente.close()
            break
    hilo=Cliente(socket_cliente,datos_cliente, correo)
    hilo.start()

    



    # elif(tipos=='R'):


    # palabra=random.choice(lista_palabras)
    # while (palabra in lista_elegidas):
    #     palabra=random.choice(lista_palabras)
    # lista_elegidas.append(palabra)
    # hilo = Cliente(socket_cliente, datos_cliente, nom, palabra)
    # hilo.start()
