import multiprocessing
import socket
import datetime
import os

# Directorio para almacenar los mensajes
directorio_mensajes = os.path.join(os.path.expanduser("~"), "Escritorio", "Mensajes")
if not os.path.exists(directorio_mensajes):
    os.makedirs(directorio_mensajes)

# Función para enviar mensajes
def enviar_mensaje(nodo_destino, mensaje):
    # Crear un socket para la conexión
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Conectar al nodo destino
    try:
        sock.connect((nodo_destino, 5000))
    except ConnectionRefusedError:
        print(f"Error: No se pudo conectar al nodo {nodo_destino}.")
        return
    
    # Obtener el timestamp actual
    tiempo_envio = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Enviar el mensaje
    mensaje_completo = f"{tiempo_envio}|{socket.gethostname()}|{mensaje}"
    sock.sendall(mensaje_completo.encode())

    # Recibir la respuesta de recibido
    respuesta = sock.recv(1024).decode()
    print(f"Respuesta de {nodo_destino}: {respuesta}")

    # Cerrar el socket
    sock.close()

# Función para recibir mensajes
def recibir_mensajes():
    # Crear un socket para la recepción
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('0.0.0.0', 5000))
    sock.listen()

    while True:
        conn, addr = sock.accept()
        mensaje_recibido = conn.recv(1024).decode()
        tiempo_recepcion = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn.sendall(b"Recibido")

        # Extraer el remitente, destinatario y el mensaje del paquete recibido
        remitente, destinatario, mensaje = mensaje_recibido.split("|")
        
        # Almacenar el mensaje en un archivo de texto
        ruta_archivo = os.path.join(directorio_mensajes, f"{destinatario}.txt")
        with open(ruta_archivo, "a") as archivo:
            archivo.write(f"{tiempo_recepcion} | {remitente} -> {mensaje}\n")

        print(f"Mensaje recibido de {remitente} para {destinatario}: {mensaje}")

# Proceso para recibir mensajes en segundo plano
proceso_recepcion = multiprocessing.Process(target=recibir_mensajes)
proceso_recepcion.start()

# Menú principal
while True:
    print("\n--- Menú ---")
    print("1. Enviar mensaje")
    print("2. Mostrar mensajes recibidos")
    print("3. Salir")

    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        nodo_destino = input("Introduzca el nombre del nodo destino: ")
        mensaje = input("Introduzca el mensaje: ")
        enviar_mensaje(nodo_destino, mensaje)
    elif opcion == "2":
        print("\n--- Mensajes Recibidos ---")
        for mensaje_archivo in os.listdir(directorio_mensajes):
            ruta_archivo = os.path.join(directorio_mensajes, mensaje_archivo)
            print(f"--- {mensaje_archivo} ---")
            with open(ruta_archivo, "r") as archivo:
                print(archivo.read())
    elif opcion == "3":
        # Detener el proceso de recepción de mensajes
        proceso_recepcion.terminate()
        print("Saliendo del programa...")
        break
    else:
        print("Opción no válida. Inténtelo de nuevo.")

