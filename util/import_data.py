# util/import_data.py
import pandas as pd
from pathlib import Path
from util.db import get_db_connection

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"

CSV_MAP = {
    "Symptoms":           ("symptoms.csv",         ["symptoms_name", "symptoms_description"]),
    "Diseases":           ("diseases.csv",         ["diseases_name", "diseases_description", "severity"]),
    "Disease_Symptoms":   ("disease_symptoms.csv", ["disease_id", "symptom_id"]),
    "Articles":           ("articles.csv",         ["title", "content", "category"]),
}

def bulk_insert(table, df, cols, cnx):
    placeholders = ", ".join(["%s"] * len(cols))
    sql = f"INSERT INTO {table} ({', '.join(cols)}) VALUES ({placeholders})"
    with cnx.cursor() as cur:
        cur.executemany(sql, df[cols].values.tolist())
        cnx.commit()
        print(f"{cur.rowcount} řádků vloženo do {table}")

def main():
    cnx = get_db_connection()
    print("Připojeno k DB")

    for table, (filename, cols) in CSV_MAP.items():
        path = DATA_DIR / filename
        df = pd.read_csv(path)
        bulk_insert(table, df, cols, cnx)

    cnx.close()
    print("Hotovo – data importována.")

if __name__ == "__main__":
    main()
