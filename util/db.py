import mysql.connector
from config import DB_CONFIG

def get_db_connection():
    return mysql.connector.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"],
        auth_plugin=DB_CONFIG.get("auth_plugin"),
        use_pure=True,
    )
