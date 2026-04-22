import sqlite3
import os

ruta_base = os.path.abspath(os.path.dirname(__file__))

def crear_base_datos():
    conexion = sqlite3.connect(os.path.join(ruta_base, 'inventario.db'))
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    ''')
    conexion.commit()
    conexion.close()
    print("¡Base de datos creada exitosamente!")

if __name__ == '__main__':
    crear_base_datos()