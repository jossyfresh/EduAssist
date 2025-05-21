import sqlite3
import os

def init_db():
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path to the database file
    db_path = os.path.join(script_dir, "app.db")
    
    # Path to the schema file
    schema_path = os.path.join(script_dir, "migrations", "sqlite_schema.sql")
    
    # Read the schema file
    with open(schema_path, 'r') as f:
        schema = f.read()
    
    # Connect to SQLite database (this will create the file if it doesn't exist)
    conn = sqlite3.connect(db_path)
    
    try:
        # Execute the schema
        conn.executescript(schema)
        conn.commit()
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Error initializing database: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    init_db() 