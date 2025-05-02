from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Función para conectar a la base de datos
def get_db():
    conn = sqlite3.connect('game_data.db')  # Nombre del archivo de la base de datos
    conn.row_factory = sqlite3.Row
    return conn

# Crear las tablas en la base de datos si no existen
def create_tables():
    conn = get_db()
    cursor = conn.cursor()

    # Tabla de personajes
    cursor.execute('''CREATE TABLE IF NOT EXISTS characters (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        race TEXT,
                        class TEXT,
                        level INTEGER,
                        background TEXT,
                        alignment TEXT,
                        abilities TEXT,
                        skills TEXT,
                        hit_points INTEGER,
                        equipment TEXT,
                        notes TEXT)''')

    # Tabla de NPCs y lore
    cursor.execute('''CREATE TABLE IF NOT EXISTS npcs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        role TEXT,
                        description TEXT,
                        stats TEXT,
                        location TEXT,
                        notes TEXT)''')

    # Tabla de lugares
    cursor.execute('''CREATE TABLE IF NOT EXISTS locations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        description TEXT,
                        map_url TEXT,
                        notes TEXT)''')

    # Tabla de eventos e historia
    cursor.execute('''CREATE TABLE IF NOT EXISTS events (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        description TEXT,
                        date TEXT,
                        characters_involved TEXT,
                        notes TEXT)''')

    # Tabla de objetos e inventario
    cursor.execute('''CREATE TABLE IF NOT EXISTS inventory (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        type TEXT,
                        description TEXT,
                        owner_id INTEGER,
                        FOREIGN KEY (owner_id) REFERENCES characters (id))''')

    conn.commit()
    conn.close()

# Ruta para guardar un personaje
@app.route('/store_character', methods=['POST'])
def store_character():
    content = request.json
    name = content.get("name")
    race = content.get("race")
    char_class = content.get("class")
    level = content.get("level", 1)
    background = content.get("background")
    alignment = content.get("alignment")
    abilities = content.get("abilities", {})
    skills = content.get("skills", {})
    hit_points = content.get("hit_points", 10)
    equipment = content.get("equipment", [])
    notes = content.get("notes", "")

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO characters 
                      (name, race, class, level, background, alignment, abilities, skills, hit_points, equipment, notes)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                   (name, race, char_class, level, background, alignment, str(abilities), str(skills), hit_points, str(equipment), notes))
    conn.commit()
    conn.close()

    return jsonify({"message": "Character stored successfully", "data": content}), 201

# Ruta para guardar un NPC
@app.route('/store_npc', methods=['POST'])
def store_npc():
    content = request.json
    name = content.get("name")
    role = content.get("role")
    description = content.get("description")
    stats = content.get("stats", {})
    location = content.get("location", "")
    notes = content.get("notes", "")

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO npcs (name, role, description, stats, location, notes) 
                      VALUES (?, ?, ?, ?, ?, ?)''',
                   (name, role, description, str(stats), location, notes))
    conn.commit()
    conn.close()

    return jsonify({"message": "NPC stored successfully", "data": content}), 201

# Ruta para recuperar personajes
@app.route('/get_characters', methods=['GET'])
def get_characters():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM characters")
    rows = cursor.fetchall()
    data = [dict(row) for row in rows]
    conn.close()
    return jsonify(data), 200

# Ruta para limpiar la base de datos
@app.route('/clear', methods=['POST'])
def clear_data():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM characters")
    cursor.execute("DELETE FROM npcs")
    cursor.execute("DELETE FROM locations")
    cursor.execute("DELETE FROM events")
    cursor.execute("DELETE FROM inventory")
    conn.commit()
    conn.close()
    return jsonify({"message": "Data cleared successfully"}), 200

if __name__ == '__main__':
    create_tables()  # Crear las tablas si no existen
    app.run(debug=True)
