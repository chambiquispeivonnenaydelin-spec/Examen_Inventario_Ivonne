import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for

# Configuración de rutas absoluta
ruta_base = os.path.abspath(os.path.dirname(__file__))
ruta_templates = os.path.join(ruta_base, 'templates')

app = Flask(__name__, template_folder=ruta_templates)

def conectar_db():
    conexion = sqlite3.connect(os.path.join(ruta_base, 'inventario.db'))
    conexion.row_factory = sqlite3.Row
    return conexion

@app.route('/')
def index():
    conexion = conectar_db()
    productos = conexion.execute('SELECT * FROM productos').fetchall()
    conexion.close()
    return render_template('index.html', productos=productos)

@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':
        nombre = request.form['nombre']
        categoria = request.form['categoria']
        precio = request.form['precio']
        stock = request.form['stock']

        conexion = conectar_db()
        conexion.execute('INSERT INTO productos (nombre, categoria, precio, stock) VALUES (?, ?, ?, ?)',
                         (nombre, categoria, precio, stock))
        conexion.commit()
        conexion.close()
        return redirect(url_for('index'))
    return render_template('registrar.html')

@app.route('/eliminar/<int:id>')
def eliminar(id):
    conexion = conectar_db()
    conexion.execute('DELETE FROM productos WHERE id = ?', (id,))
    conexion.commit()
    conexion.close()
    return redirect(url_for('index'))

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    conn = sqlite3.connect('inventario.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        categoria = request.form['categoria']
        precio = request.form['precio']
        stock = request.form['stock']
        
        cursor.execute("UPDATE productos SET nombre=?, categoria=?, precio=?, stock=? WHERE id=?", 
                       (nombre, categoria, precio, stock, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    cursor.execute("SELECT * FROM productos WHERE id=?", (id,))
    producto = cursor.fetchone()
    conn.close()
    return render_template('editar.html', producto=producto)

if __name__ == '__main__':
    app.run(debug=True)