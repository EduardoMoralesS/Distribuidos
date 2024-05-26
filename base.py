import mysql.connector
from mysql.connector import Error
import random

def insertar_inges(inges):
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
            
            for inge in inges:
                cursor.execute(insert_query, inge)
                connection.commit()
            
            print("Registros insertados exitosamente en INGENIEROS")
    
    except Error as e:
        print("Error al conectar a la base de datos", e)
    
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("Conexión a la base de datos MySQL cerrada")

def insertar_usuarios(usuarios):
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
            insert_query = """INSERT INTO USUARIOS (nombre, apellido, email, telefono)
                              VALUES (%s, %s, %s, %s)"""
            
            for usuario in usuarios:
                cursor.execute(insert_query, usuario)
                connection.commit()
            
            print("Registros insertados exitosamente en USUARIOS")
    
    except Error as e:
        print("Error al conectar a la base de datos", e)
    
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("Conexión a la base de datos MySQL cerrada")

def insertar_dispos(nombre, tipo, marca, modelo, usuario_id):
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
            insert_query = """INSERT INTO DISPOSITIVOS (nombre, tipo, marca, modelo, usuario_id)
                              VALUES (%s, %s, %s, %s, %s)"""
            record = (nombre, tipo, marca, modelo, usuario_id)
            
            # Ejecutar la consulta SQL
            cursor.execute(insert_query, record)
            connection.commit()
            print("Registro insertado exitosamente en DISPOSITIVOS")
    
    except Error as e:
        print("Error al conectar a la base de datos", e)
    
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("Conexión a la base de datos MySQL cerrada")

# Lista de ingenieros a insertar (30 datos)
inges = [
    ('Juan', 'Perez', 'juan.perez@example.com', '123456789'),
    ('Ana', 'Lopez', 'ana.lopez@example.com', '987654321'),
    ('Carlos', 'Ramirez', 'carlos.ramirez@example.com', '456123789'),
    ('Maria', 'Garcia', 'maria.garcia@example.com', '789456123'),
    ('Luis', 'Martinez', 'luis.martinez@example.com', '321654987'),
    ('Laura', 'Hernandez', 'laura.hernandez@example.com', '654789321'),
    ('Jose', 'Gonzalez', 'jose.gonzalez@example.com', '147258369'),
    ('Marta', 'Sanchez', 'marta.sanchez@example.com', '963852741'),
    ('Pedro', 'Diaz', 'pedro.diaz@example.com', '852741963'),
    ('Sofia', 'Rodriguez', 'sofia.rodriguez@example.com', '741852963'),
    ('Fernando', 'Torres', 'fernando.torres@example.com', '369258147'),
    ('Elena', 'Ruiz', 'elena.ruiz@example.com', '258147369'),
    ('Pablo', 'Vazquez', 'pablo.vazquez@example.com', '147369258'),
    ('Isabel', 'Jimenez', 'isabel.jimenez@example.com', '258963147'),
    ('Ricardo', 'Moreno', 'ricardo.moreno@example.com', '369147258'),
    ('Carmen', 'Alvarez', 'carmen.alvarez@example.com', '147258963'),
    ('Miguel', 'Castro', 'miguel.castro@example.com', '258369147'),
    ('Alicia', 'Mendez', 'alicia.mendez@example.com', '369147852'),
    ('Rafael', 'Romero', 'rafael.romero@example.com', '741963258'),
    ('Angela', 'Navarro', 'angela.navarro@example.com', '852369741'),
    ('Victor', 'Ortega', 'victor.ortega@example.com', '963147852'),
    ('Sandra', 'Ramos', 'sandra.ramos@example.com', '741258963'),
    ('Adrian', 'Vega', 'adrian.vega@example.com', '258741369'),
    ('Patricia', 'Silva', 'patricia.silva@example.com', '369852147'),
    ('Francisco', 'Molina', 'francisco.molina@example.com', '852963741'),
    ('Beatriz', 'Herrera', 'beatriz.herrera@example.com', '963741258'),
    ('Javier', 'Guzman', 'javier.guzman@example.com', '147963852'),
    ('Rosa', 'Gil', 'rosa.gil@example.com', '258147852'),
    ('Alberto', 'Iglesias', 'alberto.iglesias@example.com', '369258963'),
    ('Monica', 'Delgado', 'monica.delgado@example.com', '741369852')
]

usuarios = [
    ('Miguel', 'Castro', 'miguel.castro@example.com', '258369147'),
    ('Alicia', 'Mendez', 'alicia.mendez@example.com', '369147852'),
    ('Rafael', 'Romero', 'rafael.romero@example.com', '741963258'),
    ('Angela', 'Navarro', 'angela.navarro@example.com', '852369741'),
    ('Monica', 'Delgado', 'monica.delgado@example.com', '741369852'),
    ('Pedro', 'Diaz', 'pedro.diaz@example.com', '852741963'),
    ('Sofia', 'Rodriguez', 'sofia.rodriguez@example.com', '741852963'),
    ('Fernando', 'Torres', 'fernando.torres@example.com', '369258147'),
    ('Elena', 'Ruiz', 'elena.ruiz@example.com', '258147369'),
    ('Pablo', 'Vazquez', 'pablo.vazquez@example.com', '147369258'),
    ('Juan', 'Perez', 'juan.perez@example.com', '123456789'),
    ('Ana', 'Lopez', 'ana.lopez@example.com', '987654321'),
    ('Carlos', 'Ramirez', 'carlos.ramirez@example.com', '456123789'),
    ('Maria', 'Garcia', 'maria.garcia@example.com', '789456123'),
    ('Luis', 'Martinez', 'luis.martinez@example.com', '321654987'),
    ('Laura', 'Hernandez', 'laura.hernandez@example.com', '654789321'),
    ('Jose', 'Gonzalez', 'jose.gonzalez@example.com', '147258369'),
    ('Marta', 'Sanchez', 'marta.sanchez@example.com', '963852741'),
    ('Victor', 'Ortega', 'victor.ortega@example.com', '963147852'),
    ('Sandra', 'Ramos', 'sandra.ramos@example.com', '741258963'),
    ('Beatriz', 'Herrera', 'beatriz.herrera@example.com', '963741258'),
    ('Javier', 'Guzman', 'javier.guzman@example.com', '147963852'),
    ('Rosa', 'Gil', 'rosa.gil@example.com', '258147852'),
    ('Alberto', 'Iglesias', 'alberto.iglesias@example.com', '369258963'),
    ('Monica', 'Delgado', 'monica.delgado@example.com', '741369852'),
    ('Isabel', 'Jimenez', 'isabel.jimenez@example.com', '258963147'),
    ('Ricardo', 'Moreno', 'ricardo.moreno@example.com', '369147258'),
    ('Carmen', 'Alvarez', 'carmen.alvarez@example.com', '147258963'),
    ('Adrian', 'Vega', 'adrian.vega@example.com', '258741369'),
    ('Patricia', 'Silva', 'patricia.silva@example.com', '369852147'),
    ('Francisco', 'Molina', 'francisco.molina@example.com', '852963741'),
]

# Insertar los datos en la tabla INGENIEROS
insertar_inges(inges)
# Insertar los datos en la tabla USUARIOS
insertar_usuarios(usuarios)

# Generar 30 dispositivos
for i in range(30):
    nombre_dispositivo = f"Dispositivo {i+1}"
    tipo_dispositivo = random.choice(['Laptop', 'Teléfono', 'Tablet', 'Impresora'])
    marca_dispositivo = random.choice(['Dell', 'HP', 'Apple', 'Samsung'])
    modelo_dispositivo = f"Modelo {i+1}"
    usuario_id = random.randint(1, 30)  # Selecciona un usuario aleatorio del 1 al 30
    insertar_dispos(nombre_dispositivo, tipo_dispositivo, marca_dispositivo, modelo_dispositivo, usuario_id)

