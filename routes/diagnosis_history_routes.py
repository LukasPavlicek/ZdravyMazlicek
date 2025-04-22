# routes/diagnosis_history_routes.py
from flask import Blueprint, request, jsonify
from util.db import get_db_connection

history_bp = Blueprint('history_bp', __name__)

@history_bp.route('/', methods=['GET'])
def get_all_history():
    """
    Vrátí všechny záznamy z diagnosis_history včetně pet_name.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
               id,
               user_id,
               pet_id,
               pet_name,
               disease_id,
               symptoms,
               diagnosis,
               search_date
              FROM diagnosis_history
            ORDER BY search_date DESC
        """)
        records = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(records), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@history_bp.route('/', methods=['POST'])
def create_history_record():
    """
    Přidá nový záznam do diagnosis_history.
    Pokud uživatel nemá registrovaného mazlíčka, lze předat pet_name (druh).
    """
    try:
        data       = request.json
        user_id    = data.get('user_id')
        pet_id     = data.get('pet_id')       # může být None
        pet_name   = data.get('pet_name')     # jméno mazlíčka nebo druh ("Pes"/"Kočka")
        disease_id = data.get('disease_id')
        symptoms   = data.get('symptoms')     # např. JSON array nebo čárkami oddělený string
        diagnosis  = data.get('diagnosis', '')

        conn   = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO diagnosis_history
            (user_id, pet_id, pet_name, disease_id, symptoms, diagnosis)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            user_id,
            pet_id if pet_id else None,
            pet_name,
            disease_id,
            symptoms,
            diagnosis
        ))
        conn.commit()
        new_id = cursor.lastrowid
        cursor.close()
        conn.close()

        return jsonify({"message": "Záznam o diagnóze vytvořen", "history_id": new_id}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@history_bp.route('/<int:history_id>', methods=['GET'])
def get_history_record(history_id):
    try:
        conn   = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
               id, user_id, pet_id, pet_name,
               disease_id, symptoms, diagnosis, search_date
              FROM diagnosis_history
             WHERE id = %s
        """, (history_id,))
        record = cursor.fetchone()
        cursor.close()
        conn.close()

        if not record:
            return jsonify({"message": "Záznam nenalezen"}), 404
        return jsonify(record), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@history_bp.route('/<int:history_id>', methods=['PUT'])
def update_history_record(history_id):
    try:
        data          = request.json
        new_symptoms  = data.get('symptoms')
        new_diagnosis = data.get('diagnosis')

        conn   = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE diagnosis_history
               SET symptoms = %s,
                   diagnosis = %s
             WHERE id = %s
        """, (new_symptoms, new_diagnosis, history_id))
        conn.commit()
        affected = cursor.rowcount
        cursor.close()
        conn.close()

        if affected == 0:
            return jsonify({"message": "Záznam nenalezen"}), 404
        return jsonify({"message": "Záznam upraven"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@history_bp.route('/<int:history_id>', methods=['DELETE'])
def delete_history_record(history_id):
    try:
        conn   = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM diagnosis_history WHERE id = %s", (history_id,))
        conn.commit()
        affected = cursor.rowcount
        cursor.close()
        conn.close()

        if affected == 0:
            return jsonify({"message": "Záznam nenalezen"}), 404
        return jsonify({"message": "Záznam smazán"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
