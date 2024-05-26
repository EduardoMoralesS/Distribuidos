import mysql.connector
from mysql.connector import Error

def insert_engineer(nombre, apellido, email, telefono):
    try:
        # Establecer la conexión a la base de datos
        connection = mysql.connector.connect(
            host='localhost',
            database='SOPORTE',
            user='root',
            password='1234'
        )

        if connection.is_connected():
            cursor = connection.cursor()
            
            # Crear la consulta SQL para insertar datos
            insert_query = """INSERT INTO INGENIEROS (nombre, apellido, email, telefono)
                              VALUES (%s, %s, %s, %s)"""
            record = (nombre, apellido, email, telefono)
            
            # Ejecutar la consulta SQL
            cursor.execute(insert_query, record)
            connection.commit()
            print("Registro insertado exitosamente en INGENIEROS")
    
    except Error as e:
        print("Error al conectar a la base de datos", e)
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Conexión a la base de datos MySQL cerrada")

# Ejemplo de uso de la función
insert_engineer('Juan', 'Perez', 'juan.perez@example.com', '123456789')