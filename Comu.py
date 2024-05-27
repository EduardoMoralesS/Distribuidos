import random
import threading
from mysql.connector import connect, Error

class Nodo:
    def __init__(self, id_nodo, host, user, password):
        self.id_nodo = id_nodo
        self.host = host
        self.user = user
        self.password = password
        self.es_maestro = False
        self.termino = 0
        self.estado = 'seguidor'
        self.connection = None

    def conectar(self):
        try:
            self.connection = connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database='SOPORTE'
            )
            if self.connection.is_connected():
                print(f"Conexión establecida con el nodo {self.id_nodo}")
        except Error as e:
            print(f"Error al conectar con el nodo {self.id_nodo}: {e}")

    def cerrar_conexion(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print(f"Conexión cerrada con el nodo {self.id_nodo}")

nodos = [
    Nodo(1, 'localhost', 'root', '1234'),
    Nodo(2, 'localhost', 'root', '1234'),
    Nodo(3, 'localhost', 'root', '1234')
]

def iniciar_eleccion_bully(nodo_iniciador):
    nodo_iniciador.termino += 1
    nodo_iniciador.estado = 'candidato'
    candidatos = [nodo for nodo in nodos if nodo.id_nodo > nodo_iniciador.id_nodo]

    if not candidatos:
        nodo_iniciador.es_maestro = True
        nodo_iniciador.estado = 'maestro'
        print(f"Nodo {nodo_iniciador.id_nodo} es el nuevo nodo maestro")
    else:
        for candidato in candidatos:
            if candidato.estado != 'maestro':
                candidato.estado = 'candidato'
                iniciar_eleccion_bully(candidato)

iniciar_eleccion_bully(nodos[0])

for nodo in nodos:
    print(f"Nodo {nodo.id_nodo} - Maestro: {nodo.es_maestro}")

def distribuir_dispositivos():
    for nodo in nodos:
        nodo.conectar()
    
    maestro = next(nodo for nodo in nodos if nodo.es_maestro)
    cursor = maestro.connection.cursor()
    cursor.execute("SELECT * FROM DISPOSITIVO")
    dispositivos = cursor.fetchall()

    for i, dispositivo in enumerate(dispositivos):
        sucursal = nodos[i % len(nodos)]
        sucursal_cursor = sucursal.connection.cursor()
        sucursal_cursor.execute("INSERT INTO DISPOSITIVO (tipo, marca, modelo, usuario_id, nodo) VALUES (%s, %s, %s, %i, %i)", dispositivo)
        sucursal.connection.commit()
        print(f"Dispositivo {dispositivo[0]} distribuido al nodo {sucursal.id_nodo}")

    for nodo in nodos:
        nodo.cerrar_conexion()

distribuir_dispositivos()

lock = threading.Lock()

def levantar_ticket(id_usuario, id_dispositivo):
    lock.acquire()
    try:
        nodo_activo = random.choice(nodos)
        nodo_activo.conectar()
        cursor = nodo_activo.connection.cursor()

        cursor.execute("SELECT id_ingeniero FROM INGENIEROS ORDER BY RAND() LIMIT 1")
        id_ingeniero = cursor.fetchone()[0]

        cursor.execute("SELECT MAX(id_ticket) FROM TICKETS")
        max_id_ticket = cursor.fetchone()[0] or 0
        id_ticket = max_id_ticket + 1
        folio = f"{id_usuario}-{id_ingeniero}-{nodo_activo.id_nodo}-{id_ticket}"

        cursor.execute("INSERT INTO TICKETS (id_usuario, id_dispositivo, id_ingeniero, folio) VALUES (%s, %s, %s, %s)",
                       (id_usuario, id_dispositivo, id_ingeniero, folio))
        nodo_activo.connection.commit()
        print(f"Ticket {folio} levantado en nodo {nodo_activo.id_nodo}")
    except Error as e:
        print(f"Error al levantar ticket: {e}")
    finally:
        nodo_activo.cerrar_conexion()
        lock.release()

def cerrar_ticket(id_ticket):
    lock.acquire()
    try:
        nodo_activo = random.choice(nodos)
        nodo_activo.conectar()
        cursor = nodo_activo.connection.cursor()
        cursor.execute("DELETE FROM TICKETS WHERE id_ticket = %s", (id_ticket,))
        nodo_activo.connection.commit()
        print(f"Ticket {id_ticket} cerrado en nodo {nodo_activo.id_nodo}")
    except Error as e:
        print(f"Error al cerrar ticket: {e}")
    finally:
        nodo_activo.cerrar_conexion()
        lock.release()

def redistribuir_soportes():
    for nodo in nodos:
        if not nodo.connection.is_connected():
            for dispositivo in dispositivos:
                nodo_activo = random.choice([n for n in nodos if n.connection.is_connected()])
                nodo_activo.conectar()
                cursor = nodo_activo.connection.cursor()
                cursor.execute("INSERT INTO DISPOSITIVO (tipo, marca, modelo, usuario_id, nodo) VALUES (%s, %s, %s, %s, %s)", dispositivo)
                nodo_activo.connection.commit()
                print(f"Dispositivo {dispositivo[0]} redistribuido al nodo {nodo_activo.id_nodo}")
                nodo_activo.cerrar_conexion()

def menu_usuario():
    while True:
        print("\nMenu Usuario:")
        print("1. Levantar Ticket")
        print("2. Salir")
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            id_usuario = input("Ingrese su ID de usuario: ")
            id_dispositivo = input("Ingrese el ID del dispositivo: ")
            levantar_ticket(id_usuario, id_dispositivo)
        elif opcion == "2":
            break
        else:
            print("Opción no válida, por favor intente de nuevo.")

def menu_ingeniero():
    while True:
        print("\nMenu Ingeniero:")
        print("1. Agregar Ticket")
        print("2. Agregar Dispositivo")
        print("3. Salir")
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            id_usuario = input("Ingrese el ID de usuario: ")
            id_dispositivo = input("Ingrese el ID del dispositivo: ")
            levantar_ticket(id_usuario, id_dispositivo)
        elif opcion == "2":
            tipo = input("Ingrese el tipo de dispositivo: ")
            marca = input("Ingrese la marca del dispositivo: ")
            modelo = input("Ingrese el modelo del dispositivo: ")
            usuario_id = input("Ingrese el ID del usuario: ")
            nodo_asignado = random.choice(nodos).id_nodo
            nodo_activo = random.choice(nodos)
            nodo_activo.conectar()
            cursor = nodo_activo.connection.cursor()
            cursor.execute("INSERT INTO DISPOSITIVOS (tipo, marca, modelo, usuario_id, nodo) VALUES (%s, %s, %s, %s, %s)",
                           (tipo, marca, modelo, usuario_id, nodo_asignado))
            nodo_activo.connection.commit()
            nodo_activo.cerrar_conexion()
            print(f"Dispositivo {modelo} agregado y asignado al nodo {nodo_asignado}")
        elif opcion == "3":
            break
        else:
            print("Opción no válida, por favor intente de nuevo.")

def menu_sucursal():
    while True:
        print("\nMenu Sucursal:")
        print("1. Consultar Usuarios")
        print("2. Actualizar Lista de Usuarios")
        print("3. Levantar Ticket")
        print("4. Cerrar Ticket")
        print("5. Salir")
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            nodo_activo = random.choice(nodos)
            nodo_activo.conectar()
            cursor = nodo_activo.connection.cursor()
            cursor.execute("SELECT * FROM USUARIOS")
            usuarios = cursor.fetchall()
            for usuario in usuarios:
                print(usuario)
            nodo_activo.cerrar_conexion()
        elif opcion == "2":
            nodo_activo = random.choice(nodos)
            nodo_activo.conectar()
            id_usuario = input("Ingrese el ID del usuario: ")
            nombre = input("Ingrese el nombre del usuario: ")
            correo = input("Ingrese el correo del usuario: ")
            cursor = nodo_activo.connection.cursor()
            cursor.execute("UPDATE USUARIOS SET nombre=%s, correo=%s WHERE id_usuario=%s", (nombre, correo, id_usuario))
            nodo_activo.connection.commit()
            nodo_activo.cerrar_conexion()
            print("Usuario actualizado correctamente")
        elif opcion == "3":
            id_usuario = input("Ingrese el ID de usuario: ")
            id_dispositivo = input("Ingrese el ID del dispositivo: ")
            levantar_ticket(id_usuario, id_dispositivo)
        elif opcion == "4":
            id_ticket = input("Ingrese el ID del ticket: ")
            cerrar_ticket(id_ticket)
        elif opcion == "5":
            break
        else:
            print("Opción no válida, por favor intente de nuevo.")

def menu_principal():
    while True:
        print("\nMenu Principal:")
        print("1. Usuario")
        print("2. Ingeniero")
        print("3. Sucursal")
        print("4. Salir")
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            menu_usuario()
        elif opcion == "2":
            menu_ingeniero()
        elif opcion == "3":
            menu_sucursal()
        elif opcion == "4":
            break
        else:
            print("Opción no válida, por favor intente de nuevo.")

if __name__ == "__main__":
    menu_principal()
