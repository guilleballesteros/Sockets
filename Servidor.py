from threading import Thread, Semaphore, Lock
import socket
import random
import os, os.path
from time import sleep 
import time 
from datetime import datetime
import random


try :
    fichero=open("preguntas.txt","r")
    respuestas=[]
    pregunta=[]
    for linea in fichero:
        datos=linea.split(";")
        pregunta+=datos[0],
        respuestas+=datos[1],datos[2],datos[3]
    fichero.close()   
except:
    print("fichero no encontrado") 

res=[]
punt=0

class Cliente(Thread):
    def __init__(self, socket_cliente, datos_cliente, correo):
        Thread.__init__(self)
        self.socket = socket_cliente
        self.datos = datos_cliente
        self.correo=correo
      
    def run(self):
        global mutex
        while(True):
            global turnos, mutex
            opcion=self.socket.recv(1024).decode()
            # comprueba el tipo de opcion que ha elegido el cliente
            if(opcion=='I'):
                competiciones=getComp()
                mensaje=""
                for linea in competiciones:
                    compe=linea.split(";")
                    mensaje+=(compe[0]+";"+compe[1]+";"+compe[2]+"-")
                self.socket.send(mensaje.encode())
                grupo = self.socket.recv(1024).decode()
                # comprueba que los integrantes esten registrados
                comp = comprobacionGrupo(grupo)
                if(comp=="C"):
                    self.socket.send("A;Grupo registrado, procedemos a inscribir en la competicion".encode())
                    datos=grupo.split(";")
                    contenido=datos[2]
                    datos.remove(contenido)
                    final=""
                    for linea in datos:
                        final+=(linea+";")
                    mutex.acquire()
                    f = open("ficheros/Grupos.txt",'a')
                    f.write(linea+"\n")
                    f.close()
                    nombreG=grupo.split(";")[0]
                    posicion=int(grupo.split(";")[2])
                    if(inscribir_competicion(nombreG,posicion)):
                        self.socket.send("Grupo inscrito".encode())
                    else:
                        self.socket.send("No se ha podido inscribir al grupo".encode())
                    mutex.release()
                elif(comp=="P"):
                    mutex.acquire()
                    self.socket.send("A;Ya existe un grupo con ese nombre procedemos a inscribir a la competicion".encode())
                    nombreG=grupo.split(";")[0]
                    posicion=int(grupo.split(";")[2])
                    if(inscribir_competicion(nombreG,posicion)):
                        self.socket.send("Grupo inscrito".encode())
                    else:
                        self.socket.send("No se ha podido inscribir al grupo".encode())
                    mutex.release()

                else:
                    self.socket.send("D; Hay usuarios que no estan registrados")
            elif(opcion=='L'):
                nombre=self.socket.recv(1024).decode()
                linea =listarComp(getComp(),nombre)
                self.socket.send(linea.encode())
            elif(opcion=='M'): # Mandar preguntas 
                entrada = comprobar_fecha2("25/11/20","27/11/20")
                self.socket.send(entrada.encode())
                if(entrada=="entra"):
                    mandar=""
                    for x in range(10):
                        if(x<10):
                            mandar= mandar+"Pregunta "+str(x+1)+" "+pregunta[x]+"\n"
                    self.socket.send(mandar.encode())    
           elif(opcion=='E'): #Responder una pregunta
                 global res
                 self.socket.send("Que pregunta quieres responder? ".encode())
                 y = int(self.socket.recv(1024).decode())-1
                 if( pregunta[y]=="Respondida"):
                    self.socket.send("FF;F".encode())
                 else:
                    res.append(respuestas[y*3])
                    res.append(respuestas[y*3+1])
                    res.append(respuestas[y*3+2])
                    random.shuffle(res)
                    pre ="Pregunta "+str(y+1)+" "+pregunta[y]
                    self.socket.send(pre.encode())
                    opciones=""
                    for z in range(3):
                        opciones=opciones+(str(z+1)+". "+res[z]+"\n")
                    self.socket.send(opciones.encode())
                    eleccion = int(self.socket.recv(1024).decode())  #eval(input("Eligie la respuesta correcta: 1, 2 o 3"))
                    # if(int(eleccion)<=3):
                    puntuacion(y,res[int(eleccion-1)])
                    res.clear()
                    pregunta[y]="Respondida"
            elif(opcion=='C'):
                print("Cliente ha cerrado sesion")
                self.socket.close()
                Usuarios_conectados.remove(self.correo)
                break


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

def puntuacion(pre,ele):
    global punt
    global res
    if(pre==0):
        if(respuestas[int(pre)]==ele):
            punt+=1
            return punt
        else:
            punt-=0.25
            return punt
    else:
        if(respuestas[int(pre*3)]==ele):
            punt+=1
            return punt
        else:
            punt-=0.25
            return punt


def comprobacionGrupo(dato):
    comp = "C"
    datos=dato.split(";")
    nombre=datos[0]
    grupo=datos[1]
    integrantes=grupo.split(":")
    f=open("ficheros/Grupos.txt",'r')
    # # compprueba que el fichero este vacio o no
    # if(f.read() == ''):
    #     comp= "C"
    # else:
        # recorre el fichero y compprueba que esten registrados y que el nombre no coincida
    for linea in f:
        datoG=linea.split(";")
        nombreG=datoG[0]
        if(nombre!=nombreG):
            for integrante in integrantes:
                if ( not comprobacionCorreo(integrante) ):
                    return "D"
        else:
            comp="P"
    f.close()
    return comp

def inscribir_competicion(grupo, posicion):
    comp=False
    competiciones = getComp()
    competicion=competiciones[posicion]
    competicionF = competicion.split(";")
    fechaI=competicionF[1]
    fechaF=competicionF[3]
    if(comprobar_fecha(fechaI, fechaF)):
        # comp=True
        linea=competiciones[posicion]
        grupos=(linea.split(";")[5].split(":"))
        if(grupo not in grupos):
            comp=True
            f=open("ficheros/Competiciones.txt",'w')
            competicion = competicion.split(";")
            competicion[5]+=(grupo+":")
            # competicion.remove("\n")
            final=""
            cont=0
            for a in competicion:
                if (cont==(len(competicion)-1)):
                    final+=(a)
                else:
                    final+=(a+";")
                cont+=1
            competiciones[posicion]=final
            for linea in competiciones:
                f.write(linea)
            f.close()
        else:
            comp=False
    return comp



def comprobar_fecha(fechaini,fechafin):
    
    now = datetime.now() 
    ahora = now.strftime("%d/%m/%y")

    fechaActual = time.strptime(ahora,"%d/%m/%y")
    fechaInicio = time.strptime(fechaini,"%d/%m/%y")
    fechaFinal = time.strptime(fechafin,"%d/%m/%y")

    if(fechaInicio >= fechaActual):
        if(fechaActual <= fechaFinal):
            return True
        else:
            return False
    else:
        return False
        

def comprobar_hora(horaini, horafin):
    
    now = datetime.now() 
    ahora = now.strftime("%H:%M:%S")
    horaActual = time.strptime(ahora,"%H:%M:%S")
    horaInicio = time.strptime(horaini,"%H:%M:%S")
    horaFinal = time.strptime(horafin,"%H:%M:%S")

    if(horaInicio <= horaActual):
        if(horaActual <= horaFinal):
            return True
        else:
            return False
    else:
        return False
    
   def comprobar_fecha2(fechaini,fechafin):
    
    now = datetime.now() 
    ahora = now.strftime("%d/%m/%y")

    fechaActual = time.strptime(ahora,"%d/%m/%y")
    fechaInicio = time.strptime(fechaini,"%d/%m/%y")
    fechaFinal = time.strptime(fechafin,"%d/%m/%y")

    if(fechaInicio <= fechaActual):
        if(fechaActual <= fechaFinal):
            return "entra"
        else:
            return "no"
    else:
        return "no"


        
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
    return competiciones



def listarComp(competiciones,grupo):
    compFinal=""
    for linea in competiciones:
        dato=linea.split(";")
        fechaIni=dato[1]
        fechaFin=dato[3]
        final="Nombre= "+dato[0]+" Fecha de inicio= "+fechaIni+" Fecha de fin= "+fechaFin
        grupos=dato[5].split(":")    
        if (grupo in grupos):
            final+=" *"
        comp=comprobar_fecha(fechaIni,fechaFin)
        if(comp):
            final+=" <-"
        if(not comp):
            final+=" x"
        compFinal+=final+"|"
            
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
