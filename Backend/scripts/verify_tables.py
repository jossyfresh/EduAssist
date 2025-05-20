# Remove supabase import and usage. Use SQLAlchemy if you want to verify tables, or just delete this script if not needed.

from sqlalchemy import inspect
from app.db.session import engine

def verify_table(table_name):
    try:
        # Use SQLAlchemy to check if the table exists
        inspector = inspect(engine)
        if table_name in inspector.get_table_names():
            print(f"\n{table_name} table exists!")
            return True
        else:
            print(f"\n{table_name} table does not exist.")
            return False
    except Exception as e:
        print(f"\nError checking {table_name} table:")
        print(f"Error: {str(e)}")
        return False

def main():
    tables = [
        'learning_paths',
        'learning_path_steps',
        'content_items',
        'user_progress'
    ]
    
    print("Verifying tables...")
    for table in tables:
        verify_table(table)

if __name__ == "__main__":
    main() 