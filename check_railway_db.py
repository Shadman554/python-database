
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from models import Disease, Book, Drug, User, DictionaryWord

# Use Railway database URL
DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    print("No DATABASE_URL found. Make sure you're connected to Railway database.")
    exit(1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def check_database():
    db = SessionLocal()
    
    try:
        # Check if tables exist and count records
        diseases_count = db.query(Disease).count()
        books_count = db.query(Book).count()
        drugs_count = db.query(Drug).count()
        users_count = db.query(User).count()
        words_count = db.query(DictionaryWord).count()
        
        print(f"📊 Railway Database Status:")
        print(f"  - Diseases: {diseases_count}")
        print(f"  - Books: {books_count}")
        print(f"  - Drugs: {drugs_count}")
        print(f"  - Users: {users_count}")
        print(f"  - Dictionary Words: {words_count}")
        
        if diseases_count == 0:
            print("\n❌ No diseases found in Railway database")
            print("Run: python import_railway_data.py to import data")
        else:
            print("\n✅ Railway database has data!")
            
            # Show a few sample diseases
            sample_diseases = db.query(Disease).limit(3).all()
            print(f"\nSample diseases:")
            for disease in sample_diseases:
                print(f"  - {disease.name} ({disease.kurdish})")
        
    except Exception as e:
        print(f"Error checking database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_database()
