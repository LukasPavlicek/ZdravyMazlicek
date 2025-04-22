# routes/disease_routes.py
from flask import Blueprint, request, jsonify
from util.db import get_db_connection


disease_bp = Blueprint('disease_bp', __name__)

@disease_bp.route('/', methods=['GET'])
def get_all_diseases():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, diseases_name, diseases_description, severity
              FROM Diseases
        """)
        diseases = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(diseases), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@disease_bp.route('/<int:disease_id>', methods=['GET'])
def get_disease(disease_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, diseases_name, diseases_description, severity
              FROM Diseases
             WHERE id = %s
        """, (disease_id,))
        disease = cursor.fetchone()
        cursor.close()
        conn.close()

        if disease is None:
            return jsonify({"message": "Nemoc nenalezena"}), 404
        return jsonify(disease), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@disease_bp.route('/', methods=['POST'])
def create_disease():
    try:
        data = request.json
        name = data.get('diseases_name')
        desc = data.get('diseases_description', '')
        severity = data.get('severity', 'low')  # 'low', 'medium', 'high'

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Diseases (diseases_name, diseases_description, severity)
            VALUES (%s, %s, %s)
        """, (name, desc, severity))
        conn.commit()
        new_id = cursor.lastrowid
        cursor.close()
        conn.close()

        return jsonify({"message": "Nemoc vytvořena", "disease_id": new_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@disease_bp.route('/<int:disease_id>', methods=['PUT'])
def update_disease(disease_id):
    try:
        data = request.json
        name = data.get('diseases_name')
        desc = data.get('diseases_description')
        severity = data.get('severity')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Diseases
               SET diseases_name = %s,
                   diseases_description = %s,
                   severity = %s
             WHERE id = %s
        """, (name, desc, severity, disease_id))
        conn.commit()
        affected = cursor.rowcount
        cursor.close()
        conn.close()

        if affected == 0:
            return jsonify({"message": "Nemoc nenalezena"}), 404
        return jsonify({"message": "Nemoc upravena"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@disease_bp.route('/<int:disease_id>', methods=['DELETE'])
def delete_disease(disease_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Diseases WHERE id = %s", (disease_id,))
        conn.commit()
        affected = cursor.rowcount
        cursor.close()
        conn.close()

        if affected == 0:
            return jsonify({"message": "Nemoc nenalezena"}), 404
        return jsonify({"message": "Nemoc smazána"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
