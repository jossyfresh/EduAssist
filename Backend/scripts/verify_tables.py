from app.core.supabase import supabase

def verify_table(table_name):
    try:
        # Try to get table info
        response = supabase.table(table_name).select('*').limit(0).execute()
        print(f"\n{table_name} table exists!")
        print(f"Response: {response}")
        return True
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