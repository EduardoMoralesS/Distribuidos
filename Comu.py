import mysql.connector
from mysql.connector import Error
import random
import threading

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
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database='SOPORTE'
            )
            if self.connection.is_connected():
                print(f"Conexión establecida con el nodo {self.id_nodo}")
                return True
        except Error as e:
            print(f"Error al conectar con el nodo {self.id_nodo}: {e}")
        return False

    def cerrar_conexion(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print(f"Conexión cerrada con el nodo {self.id_nodo}")

# Configuración de direcciones IP para cada nodo (VMs)
nodos = [
    Nodo(1, '192.168.30.132', 'root', '1234'),  # Nodo 1 en VM 1
    Nodo(2, '192.168.142.133', 'root', '1234'),  # Nodo 2 en VM 2
    Nodo(3, '192.168.142.134', 'root', '1234')   # Nodo 3 en VM 3
]

# Diccionario para mantener un registro de la carga de trabajo por sucursal
carga_trabajo_por_sucursal = {nodo.id_nodo: 0 for nodo in nodos}

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

lock = threading.Lock()

def levantar_ticket(id_usuario, id_dispositivo):
    lock.acquire()
    nodo_activo = None
    try:
        # Verificar si ya hay un ticket para este dispositivo
        for nodo in nodos:
            if nodo.conectar():
                cursor = nodo.connection.cursor()
                cursor.execute("SELECT COUNT(*) FROM TICKETS WHERE dispositivo_id = %s", (id_dispositivo,))
                cantidad_tickets = cursor.fetchone()[0]
                nodo.cerrar_conexion()
                if cantidad_tickets > 0:
                    print("Ya hay un ticket abierto para este dispositivo.")
                    return

        # Encontrar la sucursal con la menor carga de trabajo
        id_sucursal_minima = min(carga_trabajo_por_sucursal, key=carga_trabajo_por_sucursal.get)

        # Conectar con la sucursal seleccionada
        nodo_activo = next(nodo for nodo in nodos if nodo.id_nodo == id_sucursal_minima)
        if nodo_activo.conectar():
            cursor = nodo_activo.connection.cursor()

            # Seleccionar un ingeniero disponible al azar
            cursor.execute("SELECT id FROM INGENIEROS ORDER BY RAND() LIMIT 1")
            id_ingeniero = cursor.fetchone()[0]

            # Insertar el ticket en la base de datos
            cursor.execute("INSERT INTO TICKETS (titulo, descripcion, usuario_id, ingeniero_id, dispositivo_id, estado) VALUES (%s, %s, %s, %s, %s, %s)",
                           ('Ticket Titulo', 'Descripcion del ticket', id_usuario, id_ingeniero, id_dispositivo, 'Abierto'))
            nodo_activo.connection.commit()
            print(f"Ticket levantado en nodo {nodo_activo.id_nodo}")

            # Actualizar la carga de trabajo de la sucursal
            carga_trabajo_por_sucursal[id_sucursal_minima] += 1
        else:
            print(f"No se pudo conectar con el nodo {nodo_activo.id_nodo} para levantar el ticket.")
    except Error as e:
        print(f"Error al levantar ticket: {e}")
    finally:
        if nodo_activo and nodo_activo.connection and nodo_activo.connection.is_connected():
            nodo_activo.cerrar_conexion()
        lock.release()

def cerrar_ticket(id_ticket):
    lock.acquire()
    nodo_activo = random.choice(nodos)
    try:
        if nodo_activo.conectar():
            cursor = nodo_activo.connection.cursor()
            cursor.execute("UPDATE TICKETS SET estado = %s WHERE id = %s", ('Cerrado', id_ticket))
            nodo_activo.connection.commit()
            print(f"Ticket {id_ticket} cerrado en nodo {nodo_activo.id_nodo}")
        else:
            print(f"No se pudo conectar con el nodo {nodo_activo.id_nodo} para cerrar el ticket.")
    except Error as e:
        print(f"Error al cerrar ticket: {e}")
    finally:
        if nodo_activo.connection and nodo_activo.connection.is_connected():
            nodo_activo.cerrar_conexion()
        lock.release()

def menu_usuario():
    while True:
        print("\nMenú Usuario:")
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
        print("\nMenú Ingeniero:")
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
            if nodo_activo.conectar():
                cursor = nodo_activo.connection.cursor()
                cursor.execute("INSERT INTO DISPOSITIVOS (tipo, marca, modelo, usuario_id, nodo) VALUES (%s, %s, %s, %s, %s)",
                               (tipo, marca, modelo, usuario_id, nodo_asignado))
                nodo_activo.connection.commit()
                nodo_activo.cerrar_conexion()
                print(f"Dispositivo {modelo} agregado y asignado al nodo {nodo_asignado}")
            else:
                print(f"No se pudo conectar con el nodo {nodo_activo.id_nodo} para agregar el dispositivo.")
        elif opcion == "3":
            break
        else:
            print("Opción no válida, por favor intente de nuevo.")

def menu_sucursal():
    while True:
        print("\nMenú Sucursal:")
        print("1. Consultar Usuarios")
        print("2. Actualizar Lista de Usuarios")
        print("3. Levantar Ticket")
        print("4. Cerrar Ticket")
        print("5. Salir")
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            nodo_activo = random.choice(nodos)
            if nodo_activo.conectar():
                cursor = nodo_activo.connection.cursor()
                cursor.execute("SELECT * FROM USUARIOS")
                usuarios = cursor.fetchall()
                for usuario in usuarios:
                    print(usuario)
                nodo_activo.cerrar_conexion()
            else:
                print(f"No se pudo conectar con el nodo {nodo_activo.id_nodo} para consultar usuarios.")
        elif opcion == "2":
            nodo_activo = random.choice(nodos)
            if nodo_activo.conectar():
                id_usuario = input("Ingrese el ID del usuario: ")
                nombre = input("Ingrese el nombre del usuario: ")
                email = input("Ingrese el correo del usuario: ")
                telefono = input("Ingrese el telefono del usuario: ")
                cursor = nodo_activo.connection.cursor()
                cursor.execute("UPDATE USUARIOS SET nombre=%s, email=%s, telefono=%s WHERE id=%s", (nombre, email, telefono, id_usuario))
                nodo_activo.connection.commit()
                nodo_activo.cerrar_conexion()
                print("Usuario actualizado correctamente")
            else:
                print(f"No se pudo conectar con el nodo {nodo_activo.id_nodo} para actualizar el usuario.")
        elif opcion == "3":
            id_usuario = input("Ingrese su ID de usuario: ")
            id_dispositivo = input("Ingrese el ID del dispositivo: ")
            levantar_ticket(id_usuario, id_dispositivo)
        elif opcion == "4":
            id_ticket = input("Ingrese el ID del ticket: ")
            cerrar_ticket(id_ticket)
        elif opcion == "5":
            break
        else:
            print("Opción no válida, por favor intente de nuevo.")

def main():
    while True:
        print("\nMenú Principal:")
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
    main()


