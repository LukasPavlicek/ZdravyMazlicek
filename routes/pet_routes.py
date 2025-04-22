# routes/pet_routes.py
from flask import Blueprint, request, jsonify
from util.db import get_db_connection


pet_bp = Blueprint('pet_bp', __name__)

# Všechny mazlíčky
@pet_bp.route('/', methods=['GET'])
def get_all_pets():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Pets")
        pets = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(pets), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Jednoho mazlíčka
@pet_bp.route('/<int:pet_id>', methods=['GET'])
def get_pet(pet_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Pets WHERE id = %s", (pet_id,))
        pet = cursor.fetchone()
        cursor.close()
        conn.close()

        if pet is None:
            return jsonify({"message": "Mazlíček nenalezen"}), 404
        return jsonify(pet), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Vytvoření mazlíčka
@pet_bp.route('/', methods=['POST'])
def create_pet():
    try:
        data = request.json
        user_id = data.get('user_id')
        pet_name = data.get('pet_name')
        species = data.get('species')
        age = data.get('age', 0)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Pets (user_id, pet_name, species, age)
            VALUES (%s, %s, %s, %s)
        """, (user_id, pet_name, species, age))
        conn.commit()
        new_id = cursor.lastrowid
        cursor.close()
        conn.close()

        return jsonify({"message": "Mazlíček vytvořen", "pet_id": new_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Úprava mazlíčka
@pet_bp.route('/<int:pet_id>', methods=['PUT'])
def update_pet(pet_id):
    try:
        data = request.json
        new_name = data.get('pet_name')
        new_species = data.get('species')
        new_age = data.get('age')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Pets
               SET pet_name = %s,
                   species = %s,
                   age = %s
             WHERE id = %s
        """, (new_name, new_species, new_age, pet_id))
        conn.commit()
        affected = cursor.rowcount
        cursor.close()
        conn.close()

        if affected == 0:
            return jsonify({"message": "Mazlíček nenalezen"}), 404
        return jsonify({"message": "Mazlíček upraven"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Smazání mazlíčka
@pet_bp.route('/<int:pet_id>', methods=['DELETE'])
def delete_pet(pet_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Pets WHERE id = %s", (pet_id,))
        conn.commit()
        affected = cursor.rowcount
        cursor.close()
        conn.close()

        if affected == 0:
            return jsonify({"message": "Mazlíček nenalezen"}), 404
        return jsonify({"message": "Mazlíček smazán"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
