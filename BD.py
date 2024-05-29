import mysql.connector
from mysql.connector import Error
import random

def otorgar_privilegios(host, user, password, user_to_grant, ip_nodo):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )

        if connection.is_connected():
            cursor = connection.cursor()
            grant_privileges_query = f"""
            GRANT INSTERT ADD SELECT ON 'SOPORTE' TO '{user_to_grant}'@'{ip_nodo}' WITH GRANT OPTION;
            FLUSH PRIVILEGES;
            """
            cursor.execute(grant_privileges_query)
            connection.commit()
            print(f"Todos los privilegios han sido otorgados al usuario '{user_to_grant}' desde la IP '{ip_address}'")
    except Error as e:
        print(f"Error al otorgar privilegios: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Conexión a la base de datos MySQL cerrada")

# CREATE USER '{user_to_grant}'@'{ip_nodo}' IDENTIFIED BY '{password}';

# Parámetros de conexión
host = 'localhost'  # Cambia esto según sea necesario
user = 'root'
password = '1234'
user_to_grant = 'root'  # El usuario al que quieres otorgar privilegios
ip_nodo = '192.168.30.132'  # La IP desde la cual el usuario se conectará

# Otorgar privilegios
otorgar_privilegios(host, user, password, user_to_grant, ip_nodo)

host = 'localhost'  # Cambia esto según sea necesario
user = 'root'
password = '1234'
user_to_grant = 'root'  # El usuario al que quieres otorgar privilegios
ip_nodo = '192.168.30.133'  # La IP desde la cual el usuario se conectará

# Otorgar privilegios
otorgar_privilegios(host, user, password, user_to_grant, ip_nodo)

host = 'localhost'  # Cambia esto según sea necesario
user = 'root'
password = '1234'
user_to_grant = 'root'  # El usuario al que quieres otorgar privilegios
ip_nodo = '192.168.30.134'  # La IP desde la cual el usuario se conectará

# Otorgar privilegios
otorgar_privilegios(host, user, password, user_to_grant, ip_nodo)


