from flask import Flask, request, jsonify, render_template
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB_NAME = 'inventario.db'

@app.route('/registrar', methods=['POST'])
def registrar():
    data = request.get_json()
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Crear tabla si no existe
    c.execute('''
        CREATE TABLE IF NOT EXISTS equipos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE,
            sistema TEXT,
            ram INTEGER,
            procesador TEXT,
            disco INTEGER,
            ip TEXT,
            fecha TEXT
        )
    ''')

    # Intentar actualizar primero
    c.execute('''
        UPDATE equipos SET
            sistema = ?,
            ram = ?,
            procesador = ?,
            disco = ?,
            ip = ?,
            fecha = ?
        WHERE nombre = ?
    ''', (
        data['sistema'],
        data['ram'],
        data['procesador'],
        data['disco'],
        data['ip'],
        datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        data['nombre']
    ))

    # Si no se actualizó ninguna fila, insertar nuevo registro
    if c.rowcount == 0:
        c.execute('''
            INSERT INTO equipos (nombre, sistema, ram, procesador, disco, ip, fecha)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['nombre'],
            data['sistema'],
            data['ram'],
            data['procesador'],
            data['disco'],
            data['ip'],
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ))

    conn.commit()
    conn.close()
    return jsonify({'status': 'ok'})

@app.route('/prueba')
def prueba():
    return "Servidor activo"

@app.route('/')
def ver_equipos():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM equipos ORDER BY fecha DESC")
    equipos = cursor.fetchall()
    conn.close()
    return render_template('index.html', equipos=equipos)

import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5050))  # Render asigna automáticamente el puerto
    app.run(host='0.0.0.0', port=port, debug=True)