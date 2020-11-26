import socket

s = socket.socket()
s.connect(("localhost", 9999))
validacion=False
# comprueba si el email es valido
def comprobarEmail(email):
    comprobacion=False
    if "@" in email:
        nuevo_email=email.split('@')
        resto=nuevo_email[1]
        if "." in resto:
            comprobacion=True
    
    return comprobacion


def menu(correoC):
    while(True):
        print("1.(Listar competiciones)")
        print("2.(Inscribir grupo)")
        print("3.(Mostrar preguntas)")
        print("4.(Enviar respuesta)")
        print("5.(Cerrar sesion): ")

        opcion=int(input("Seleccione una opcion: ").strip())
        # comprueba la opcion que ha elegido el usuario
        if(opcion==1):
            s.send("L".encode())
            nombre=input("Introduce el nombre del grupo: ")
            s.send(nombre.encode())
            print("Listando Competiciones...")
            competiciones=(s.recv(1024).decode()).split("|")
            for linea in competiciones:
                print(linea)
        elif(opcion==2):
            # envia la opcion
            s.send("I".encode())
            competiciones=s.recv(1024).decode()
            nombre=input("introduce el nombre del grupo: ").strip()
            nombre+=";"
            # concatena con el nombre del grupo el correo del usuario conectado
            nombre += (correoC+":")
            num_participantes=0
            # mientras que no se hayan introducido a todos los integrantes sigue el bucle
            while(num_participantes<2):
                correo=input("Introduce el correo de los demas participantes").strip()
                # comprueba que el email introducido sea valido
                if(comprobarEmail(correo)):
                    # si es el ultimo correo termina en ;
                    if(num_participantes==1):
                        nombre+=(correo+";")
                    # si no termina en :
                    else:
                        nombre+=(correo+":")
                    num_participantes +=1
                else:
                    print("Correo no valido")
            while(True):
                cont=0
                compe=competiciones.split("-")
                print (compe)
                con=0
                for linea in compe:
                    if( not con==(len(compe)-1)):
                        datos=linea.split(";")
                        print(datos)
                        mostrar=datos[0]+" Hora de inicio: "+datos[1]+" "+datos[2]
                        print(str(cont)+" = "+mostrar)
                        cont +=1
                    con+=1
                inscribir=int(input("Elige una opcion: ").strip())
                if(inscribir>=len(competiciones) or inscribir < 0):
                    print("Dicha competicion no existe")
                else:
                    nombre+=str(inscribir)+";"
                    break
            s.send(nombre.encode())
            print("enviando datos...")
            print(nombre)
            # envia la informacion y espera respuesta
            s.send(nombre.encode())
            # divide la respuesta
            respuesta=s.recv(1024).decode().split(";")
            tipo=respuesta[0]
            cadena=respuesta[1]
            # mira si se ha podido realizar la opcion o no, e informa de ello
            if (tipo == 'A'):
                print (cadena)
                print(s.recv(1024).decode())
            else:
                print (cadena)
        elif(opcion==3):
            s.send("M".encode())
            print("Cerrando Sesion...")
        elif(opcion==4):
            s.send("E".encode())
            print("Cerrando Sesion...")
        elif(opcion==5):
            s.send("C".encode())
            print("Cerrando Sesion...")
            break
        else:
            print("Opcion no valida")


correoC=""

while(not validacion):
    opcion=int(input("Seleccione una accion: 1.(Iniciar Sesion) 2.(Registrar una cuenta nueva) 3.(salir): ").strip())
    # comprueba el tipo de opcion que ha escogido el cliente
    if ( opcion==1):
        correo=input("Introduzca una direccion de correo: ").strip()
        # si el correo es valido lo envia al servidor esperando respuesta
        if (comprobarEmail(correo)):
            s.send(("I;"+correo).encode())
            respuesta=s.recv(1024).decode()
            dato=respuesta.split(";")
            tipo=dato[0]
            cadena=dato[1]
            # si la respuesta es afirmativa, sale del bucle, imprime el mensaje y guarda el correo
            if(tipo=="A"):
                validacion=True
                correoC = correo
                print(cadena)
                menu(correoC)
                break
            else:
                print(cadena)
        else:
            print("Correo no valido")
    elif( opcion==2):
        correo=input("Introduzca una direccion de correo: ").strip()
        # si el correo es valido lo envia al servidor y espera respuesta
        if (comprobarEmail(correo)):
            s.send(("R;"+correo).encode())
            respuesta=s.recv(1024).decode()
            dato=respuesta.split(";")
            tipo=dato[0]
            cadena=dato[1]
            # si la respuesta es afirmativa, vuelve a mostrar el menu por si quiere registrar a otro usuario o iniciar sesion
            if(tipo=='A'):
                print(cadena)
            else:
                print(cadena)
        else:
            print("Correo no valido")
    # si quiere salir, envia el mensaje al servidor y cierra conexion
    elif(opcion==3):
        s.send("S; ".encode())
        s.close()
        break
    # si la opcion no esta entre las esperadas muestra el mensaje
    else:
        print("La opcion elegida no es correcta")
# mientras que el cliente no quiera salir muestra el menu









# opcion=s.recv(1024).decode()
# fin_partida=True
# while fin_partida:
#     letra = input("Letra a buscar >> ")
#     s.send(letra.encode())
#     existe=s.recv(1024).decode()
#     if(existe=='s'):
#         print("La letra "+letra+" existe en la palabra.")
#     else:
#         print("La letra "+letra+" no existe en la palabra.")
#     datos=s.recv(1024).decode().split(";")
#     oculta=datos[0]
#     intentos=int(datos[1])
#     mensaje=datos[2]
#     palabra=datos[3]
#     print("Palabra: "+oculta)
#     print("Intentos: "+str(6-int(intentos)))
#     if(mensaje=='G'):
#         print("Has ganado la partida en "+str(6-int(intentos))+" intentos. La palabra era "+palabra)
#         fin_partida=False
#     elif (intentos==0):
#         print("Has perdido la partida. La palabra era "+palabra)
#         fin_partida=False
# s.close()