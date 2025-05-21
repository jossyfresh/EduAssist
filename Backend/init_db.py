from app.db.init_db import init_db

if __name__ == "__main__":
    print("Creating initial data")
    init_db()
    print("Initial data created") 