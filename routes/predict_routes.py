# routes/predict_routes.py
from flask import Blueprint, request, jsonify
from util.db import get_db_connection

predict_bp = Blueprint("predict_bp", __name__)

@predict_bp.route("/predict", methods=["POST"])
def predict():
    """
    Body JSON: {"symptom_ids":[1,4,7]}
    Vrátí seřazený seznam nemocí s počtem shod (match_count) a závažností.
    """
    ids = (request.json or {}).get("symptom_ids", [])
    if not ids:
        return jsonify([])

    fmt = ", ".join(["%s"] * len(ids))
    sql = f"""
        SELECT d.id,
               d.diseases_name,
               d.diseases_description,
               d.severity,
               COUNT(*)               AS match_count
          FROM Diseases d
          JOIN Disease_Symptoms ds ON d.id = ds.disease_id
         WHERE ds.symptom_id IN ({fmt})
      GROUP BY d.id
      ORDER BY match_count DESC,
               FIELD(d.severity,'high','medium','low')
    """

    cnx = get_db_connection()
    cur = cnx.cursor(dictionary=True)
    cur.execute(sql, ids)
    rows = cur.fetchall()
    cur.close(); cnx.close()
    return jsonify(rows)
