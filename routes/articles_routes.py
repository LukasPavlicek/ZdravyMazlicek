# routes/articles_routes.py
from flask import Blueprint, request, jsonify
from util.db import get_db_connection


articles_bp = Blueprint('articles_bp', __name__)

@articles_bp.route('/', methods=['GET'])
def get_all_articles():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Articles")
        articles = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(articles), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@articles_bp.route('/<int:article_id>', methods=['GET'])
def get_article(article_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Articles WHERE id = %s", (article_id,))
        article = cursor.fetchone()
        cursor.close()
        conn.close()

        if article is None:
            return jsonify({"message": "Článek nenalezen"}), 404
        return jsonify(article), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@articles_bp.route('/', methods=['POST'])
def create_article():
    try:
        data = request.json
        title = data.get('title')
        content = data.get('content')
        category = data.get('category', '')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Articles (title, content, category)
            VALUES (%s, %s, %s)
        """, (title, content, category))
        conn.commit()
        new_id = cursor.lastrowid
        cursor.close()
        conn.close()

        return jsonify({"message": "Článek vytvořen", "article_id": new_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@articles_bp.route('/<int:article_id>', methods=['PUT'])
def update_article(article_id):
    try:
        data = request.json
        new_title = data.get('title')
        new_content = data.get('content')
        new_category = data.get('category')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Articles
               SET title = %s,
                   content = %s,
                   category = %s
             WHERE id = %s
        """, (new_title, new_content, new_category, article_id))
        conn.commit()
        affected = cursor.rowcount
        cursor.close()
        conn.close()

        if affected == 0:
            return jsonify({"message": "Článek nenalezen"}), 404
        return jsonify({"message": "Článek upraven"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@articles_bp.route('/<int:article_id>', methods=['DELETE'])
def delete_article(article_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Articles WHERE id = %s", (article_id,))
        conn.commit()
        affected = cursor.rowcount
        cursor.close()
        conn.close()

        if affected == 0:
            return jsonify({"message": "Článek nenalezen"}), 404
        return jsonify({"message": "Článek smazán"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
