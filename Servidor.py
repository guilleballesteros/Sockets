from threading import Thread, Semaphore, Lock
import socket
import random
import os, os.path
from time import sleep 
import time 
from datetime import datetime

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
                competiciones=getComp()
                mensaje=""
                for linea in competiciones:
                    compe=linea.split(";")
                    mensaje+=(compe[0]+";"+compe[1]+";"+compe[2]+"-")
                print(mensaje)
                self.socket.send(mensaje.encode())
                grupo = self.socket.recv(1024).decode()
                print(grupo)
                # coprueba que no haya integrantes registrados en otro grupo
                # comprueba que los integrantes esten registrados
                comp = comprobacionGrupo(grupo)
                if(comp=="C"):
                    mutex.acquire()
                    f = open("ficheros/Grupos.txt",'a')
                    f.write(grupo+"\n")
                    self.socket.send("A;Grupo registrado, procedemos a inscribir en la competicion".encode())
                    f.close()
                    mutex.release()
                elif(comp=="P"):
                    self.socket.send("A;Ya existe un grupo con ese nombre procedemos a inscribir a la competicion".encode())
                    competicion=competiciones[int(grupo.split(";")[2])]
                    print (competicion)

                else:
                    self.socket.send("D; Hay usuarios que no estan registrados")
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

# def comprobacionRep(dato):
#     comp = True
#     datos=dato.split(";")
#     grupo=datos[1]
#     integrantes=grupo.split(":")
#     f=open("ficheros/Grupos.txt",'r')
#     print (comp)
#     # recorre el fichero y comprueba que no haya integrantes en otro grupo registrado
#     for linea in f:
#         datostxt=linea.split(";")
#         grupotxt=datostxt[1].split(":")
#         for integrante in integrantes:
#             if(integrante in grupotxt):
#                 comp=False
#     return comp

def comprobacionGrupo(dato):
    comp = "C"
    datos=dato.split(";")
    nombre=datos[0]
    print(nombre)
    grupo=datos[1]
    print(grupo)
    integrantes=grupo.split(":")
    f=open("ficheros/Grupos.txt",'r')
    print (comp)
    # # compprueba que el fichero este vacio o no
    # if(f.read() == ''):
    #     comp= "C"
    # else:
        # recorre el fichero y compprueba que esten registrados y que el nombre no coincida
    for linea in f:
        datoG=linea.split(";")
        nombreG=datoG[0]
        print(nombre)
        print(nombreG)
        if(nombre!=nombreG):
            for integrante in integrantes:
                if ( not comprobacionCorreo(integrante) ):
                    return "D"
        else:
            comp="P"
    f.close()
    return comp

def inscribir_competicion(grupo, competiciones, posicion):
    f=open("ficheros/Competiciones.txt",'w')
    competicion=competiciones[posicion]
    competicion = competicion.split(";")
    fechaI=competicion[1]
    fechaF=competicion[2]


def comprobar_fecha(fechacomp):
    now = datetime.now() 
    ahora = now.strftime("%d/%m/%y")
    fecha = time.strptime(ahora,"%d/%m/%y")
    fecha2 = time.strptime(fechacomp,"%d/%m/%y")
    print("hoy es "+ahora)
    if(fecha == fecha2):
        print("entra")
    if(fecha < fecha2):
        print("ya se ha pasado la fecha")
    if(fecha > fecha2):
        print("no ha llegado aun la fecha")


def comprobar_hora(horacomp):
    
    now = datetime.now() 
    ahora = now.strftime("%H:%M:%S")
    hora = time.strptime(ahora,"%H:%M:%S")
    horaLimite = time.strptime(horacomp,"%H:%M:%S")
    print("ahora es "+ahora)
    if(hora > horaLimite):
        print("entra")
    if(hora < horaLimite):
        print("hora finalizada")

        
# comprueba si hay algun usuario con el mismo nombre en el fichero
def comprobacionCorreo(correo):
    comp=False
    f=open("ficheros/Usuarios.txt",'r')
    for linea in f:
        dato=linea.split(";")
        if (dato[0] == correo):
            comp=True
    f.close()
    return comp

turnos=Semaphore(2)
mutex=Lock()
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("", 9999))
server.listen(1)
Usuarios_conectados=[]

def inicio(socket_cliente,datos_cliente,correo):
    hilo=Cliente(socket_cliente,datos_cliente, correo)
    hilo.start()

def getComp():
    f=open("ficheros/Competiciones.txt")
    competiciones=[]
    for linea in f:
        competiciones.append(linea)
    f.close()
    print (competiciones)
    return competiciones

def listarComp1(competiciones,grupo):
    compFinal=[]
    for linea in competiciones:
        dato=linea.split(";")
        if(len(dato<4)):
            compFinal.append(linea)
        else:
            grupos=dato[3].split(":")
            if (grupo not in grupos):
                compFinal.append(linea)
    return compFinal

def listarComp2(competiciones,grupo):
    compFinal=[]
    for linea in competiciones:
        dato=linea.split(";")
        if(len(dato<4)):
            compFinal.append(linea)
        else:
            grupos=dato[3].split(":")
            if (grupo in grupos):
                compFinal.append(linea+" * ")
            
    return compFinal




# bucle para atender clientes
while True:
    # Se espera a un cliente
    socket_cliente, datos_cliente = server.accept()
    # Se mira si quiere iniciar sesion o registrarse
    while (True):
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
                    inicio(socket_cliente,datos_cliente,correo)
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
    

    






    # elif(tipos=='R'):


    # palabra=random.choice(lista_palabras)
    # while (palabra in lista_elegidas):
    #     palabra=random.choice(lista_palabras)
    # lista_elegidas.append(palabra)
    # hilo = Cliente(socket_cliente, datos_cliente, nom, palabra)
    # hilo.start()
