import sqlite3
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
DB_PATH = os.getenv("DATABASE_PATH")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tests (
            test_id TEXT PRIMARY KEY,
            patient_id TEXT NOT NULL,
            clinic_id TEXT NOT NULL,
            test_type TEXT NOT NULL,
            result TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def insert_test(data):
    conn = sqlite3.connect(DB_PATH)
    try:
        
        conn.execute("BEGIN") 
        cursor = conn.cursor()
        
        # Check for duplicate test_id
        cursor.execute("SELECT test_id FROM tests WHERE test_id = ?", (data['test_id'],))
        if cursor.fetchone():
            return "EXISTS"

        query = "INSERT INTO tests (test_id, patient_id, clinic_id, test_type, result, created_at) VALUES (?, ?, ?, ?, ?, ?)"
        params = (
            data['test_id'], data['patient_id'], data['clinic_id'], 
            data['test_type'], data['result'], datetime.now().isoformat()
        )
        cursor.execute(query, params)
        conn.commit() 
        return "SUCCESS"
    except Exception as e:
        # Rollback on failure
        conn.rollback() 
        raise e
    finally:
        conn.close()

def get_tests_by_clinic(clinic_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tests WHERE clinic_id = ?", (clinic_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows