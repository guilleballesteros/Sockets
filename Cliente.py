import socket

s = socket.socket()
s.connect(("localhost", 9999))
validacion=False

def comprobarEmail(email):
    comprobacion=False
    if "@" in email:
        nuevo_email=email.split('@')
        resto=nuevo_email[1]
        if "." in resto:
            comprobacion=True
    
    return comprobacion



while(not validacion):
    opcion=int(input("Seleccione una accion: 1.(Iniciar Sesion) 2.(Registrar una cuenta nueva): "))
    if ( opcion==1):
        correo=input("Introduzca una direccion de correo: ")
        if (comprobarEmail(correo)):
            s.send(("I;"+correo).encode())
            respuesta=s.recv(1024).decode()
            print(respuesta)
            if(respuesta=="A"):
                validacion=True
            else:
                print("No se ha podido iniciar sesion, puede que el correo sea incorrdcto.")
        else:
            print("Correo no valido")
    elif( opcion==2):
        correo=input("Introduzca una direccion de correo: ")
        if (comprobarEmail(correo)):
            s.send(("R;"+correo).encode())
            respuesta=s.recv(1024).decode()
            if(respuesta=='A'):
                print("Correo registrado exisosamente, Inicie sesion o registre un nuevo correo.")
            else:
                print("No se ha podido Registrar, puede que el correo ya exista.")
        else:
            print("Correo no valido")
    else:
        print("La opcion elegida no es correcta")
opcion=s.recv(1024).decode()
fin_partida=True
while fin_partida:
    letra = input("Letra a buscar >> ")
    s.send(letra.encode())
    existe=s.recv(1024).decode()
    if(existe=='s'):
        print("La letra "+letra+" existe en la palabra.")
    else:
        print("La letra "+letra+" no existe en la palabra.")
    datos=s.recv(1024).decode().split(";")
    oculta=datos[0]
    intentos=int(datos[1])
    mensaje=datos[2]
    palabra=datos[3]
    print("Palabra: "+oculta)
    print("Intentos: "+str(6-int(intentos)))
    if(mensaje=='G'):
        print("Has ganado la partida en "+str(6-int(intentos))+" intentos. La palabra era "+palabra)
        fin_partida=False
    elif (intentos==0):
        print("Has perdido la partida. La palabra era "+palabra)
        fin_partida=False
s.close()