import socket

s = socket.socket()
s.connect(("localhost", 9003))

nom_cliente=input("Introduce tu nombre: ")
s.send(nom_cliente.encode())
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