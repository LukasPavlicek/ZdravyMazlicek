# routes/symptom_routes.py
from flask import Blueprint, request, jsonify
from util.db import get_db_connection

symptom_bp = Blueprint('symptom_bp', __name__)

# ---------- REST CRUD ----------
@symptom_bp.route('/', methods=['GET'])
def get_all_symptoms():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM Symptoms")
    rows = cur.fetchall()
    cur.close(); conn.close()
    return jsonify(rows), 200

# (ostatní CRUD routy PUT/POST/DELETE beze změny …)

# ---------- 🔹 NOVÝ JSON endpoint pro frontend ----------
@symptom_bp.route('/api', methods=['GET'])
def api_symptoms():
    """
    Vrátí seznam všech příznaků (id, symptoms_name) pro <select>.
    GET /symptoms/api  →  [{"id":1,"symptoms_name":"Kašel"}, …]
    """
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id, symptoms_name FROM Symptoms ORDER BY symptoms_name;")
    data = cur.fetchall()
    cur.close(); conn.close()
    return jsonify(data)
