# routes/disease_symptom_routes.py
from flask import Blueprint, request, jsonify
from util.db import get_db_connection


disease_symptom_bp = Blueprint('disease_symptom_bp', __name__)

# Získat všechny dvojice (disease_id, symptom_id)
@disease_symptom_bp.route('/', methods=['GET'])
def get_all_disease_symptoms():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Disease_Symptoms")
        links = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(links), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Přiřadit příznak k nemoci
@disease_symptom_bp.route('/', methods=['POST'])
def add_symptom_to_disease():
    try:
        data = request.json
        disease_id = data.get('disease_id')
        symptom_id = data.get('symptom_id')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Disease_Symptoms (disease_id, symptom_id)
            VALUES (%s, %s)
        """, (disease_id, symptom_id))
        conn.commit()
        new_id = cursor.lastrowid
        cursor.close()
        conn.close()

        return jsonify({"message": "Příznak přiřazen k nemoci", "id": new_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Smazat přiřazení příznaku k nemoci
@disease_symptom_bp.route('/<int:link_id>', methods=['DELETE'])
def remove_symptom_from_disease(link_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Disease_Symptoms WHERE id = %s", (link_id,))
        conn.commit()
        affected = cursor.rowcount
        cursor.close()
        conn.close()

        if affected == 0:
            return jsonify({"message": "Spojení nenalezeno"}), 404
        return jsonify({"message": "Spojení smazáno"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
