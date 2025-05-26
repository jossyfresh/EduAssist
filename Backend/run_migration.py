import sqlite3
import os

def run_migration():
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path to the database file
    db_path = os.path.join(script_dir, "eduassist.db")
    
    # Connect to SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Enable foreign keys
        cursor.execute("PRAGMA foreign_keys = ON")
        
        # Run the migration
        cursor.execute("ALTER TABLE courses RENAME COLUMN created_by TO creator_id")
        
        # Commit the changes
        conn.commit()
        print("Migration completed successfully!")
    except Exception as e:
        print(f"Error running migration: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    run_migration() 