# routes/user_routes.py
from flask import Blueprint, request, jsonify
from util.db import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash

user_bp = Blueprint('user_bp', __name__)

# (A) Získání všech uživatelů
@user_bp.route('/', methods=['GET'])
def get_all_users():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, user_name, email, created_at FROM Users")
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(users), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# (B) Získání konkrétního uživatele podle ID
@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, user_name, email, created_at FROM Users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user is None:
            return jsonify({"message": "Uživatel nenalezen"}), 404

        return jsonify(user), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# (C) Vytvoření nového uživatele (hashování hesla)
@user_bp.route('/', methods=['POST'])
def create_user():
    try:
        data = request.json
        user_name = data.get('user_name')
        raw_password = data.get('user_password')
        email = data.get('email')

        # Hashování hesla
        hashed_password = generate_password_hash(raw_password)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Users (user_name, user_password, email)
            VALUES (%s, %s, %s)
        """, (user_name, hashed_password, email))
        conn.commit()
        new_id = cursor.lastrowid
        cursor.close()
        conn.close()

        return jsonify({"message": "Uživatel vytvořen", "user_id": new_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# (D) Úprava uživatele + přegenerování hesla (pokud je nové heslo zadáno)
@user_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        data = request.json
        new_name = data.get('user_name')
        new_password = data.get('user_password')  # pokud bude None, nebudeme měnit
        new_email = data.get('email')

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Nejprve načteme stávajícího uživatele, abychom zjistili stávající heslo
        cursor.execute("SELECT user_password FROM Users WHERE id = %s", (user_id,))
        row = cursor.fetchone()
        if not row:
            cursor.close()
            conn.close()
            return jsonify({"message": "Uživatel nenalezen"}), 404

        hashed_password = row['user_password']

        # Pokud uživatel pošle new_password, zahashujeme ho, jinak ponecháme starý
        if new_password:
            hashed_password = generate_password_hash(new_password)

        cursor.execute("""
            UPDATE Users
               SET user_name = %s,
                   user_password = %s,
                   email = %s
             WHERE id = %s
        """, (new_name, hashed_password, new_email, user_id))
        conn.commit()
        affected = cursor.rowcount
        cursor.close()
        conn.close()

        if affected == 0:
            return jsonify({"message": "Uživatel nenalezen"}), 404
        return jsonify({"message": "Uživatel upraven"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# (E) Smazání uživatele
@user_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Users WHERE id = %s", (user_id,))
        conn.commit()
        affected = cursor.rowcount
        cursor.close()
        conn.close()

        if affected == 0:
            return jsonify({"message": "Uživatel nenalezen"}), 404

        return jsonify({"message": "Uživatel smazán"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# (F) Ukázka loginu (kontrola hesla)
@user_bp.route('/login', methods=['POST'])
def login():
    """
    Příklad, jak ověřit heslo.
    Ověřuje se email + raw_password, porovná se s hashovaným heslem.
    V reálné aplikaci by se generoval např. JWT token, session apod.
    """
    try:
        data = request.json
        email = data.get('email')
        raw_password = data.get('user_password')

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, user_password FROM Users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if not user:
            return jsonify({"message": "Uživatel nenalezen"}), 404

        stored_hash = user["user_password"]
        if check_password_hash(stored_hash, raw_password):
            # Heslo je správné
            return jsonify({"message": "Přihlášení úspěšné", "user_id": user["id"]}), 200
        else:
            return jsonify({"message": "Špatné heslo"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500
