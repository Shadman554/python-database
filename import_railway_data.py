import json
import os
from datetime import datetime
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Book, Disease, Drug, DictionaryWord, User, Question, Notification, Staff, TutorialVideo, NormalRange, AppLink, About

# Create all tables
Base.metadata.create_all(bind=engine)

def convert_timestamp(timestamp_obj):
    """Convert Firebase timestamp to datetime"""
    if isinstance(timestamp_obj, dict) and '_seconds' in timestamp_obj:
        return datetime.fromtimestamp(timestamp_obj['_seconds'])
    return datetime.utcnow()

def import_data_to_railway():
    """Import all data to Railway database with duplicate handling"""
    db = SessionLocal()
    
    try:
        print("Starting Railway data import...")
        
        # Import books
        try:
            with open('attached_assets/books_1752089134448.json', 'r', encoding='utf-8') as f:
                books_data = json.load(f)
            
            imported_books = 0
            for book_data in books_data:
                existing_book = db.query(Book).filter(Book.id == book_data['id']).first()
                if not existing_book:
                    book = Book(
                        id=book_data['id'],
                        title=book_data.get('title', ''),
                        description=book_data.get('description', ''),
                        category=book_data.get('category', ''),
                        cover_url=book_data.get('coverUrl', ''),
                        download_url=book_data.get('downloadUrl', ''),
                        added_at=convert_timestamp(book_data.get('addedAt', {}))
                    )
                    db.add(book)
                    imported_books += 1
            
            db.commit()
            print(f"✓ Imported {imported_books} books")
        except Exception as e:
            print(f"Error importing books: {e}")
            db.rollback()
        
        # Import diseases
        try:
            with open('attached_assets/diseases_1752089134448.json', 'r', encoding='utf-8') as f:
                diseases_data = json.load(f)
            
            imported_diseases = 0
            for disease_data in diseases_data:
                existing_disease = db.query(Disease).filter(Disease.id == disease_data['id']).first()
                if not existing_disease:
                    disease = Disease(
                        id=disease_data['id'],
                        name=disease_data.get('name', ''),
                        kurdish=disease_data.get('kurdish', ''),
                        symptoms=disease_data.get('symptoms', ''),
                        cause=disease_data.get('cause', ''),
                        control=disease_data.get('control', ''),
                        created_at=datetime.utcnow()
                    )
                    db.add(disease)
                    imported_diseases += 1
            
            db.commit()
            print(f"✓ Imported {imported_diseases} diseases")
        except Exception as e:
            print(f"Error importing diseases: {e}")
            db.rollback()
        
        # Import drugs
        try:
            with open('attached_assets/drugs_1752089134449.json', 'r', encoding='utf-8') as f:
                drugs_data = json.load(f)
            
            imported_drugs = 0
            for drug_data in drugs_data:
                existing_drug = db.query(Drug).filter(Drug.id == drug_data['id']).first()
                if not existing_drug:
                    drug = Drug(
                        id=drug_data['id'],
                        name=drug_data.get('name', ''),
                        usage=drug_data.get('usage', ''),
                        side_effect=drug_data.get('sideEffect', ''),
                        other_info=drug_data.get('otherInfo', ''),
                        drug_class=drug_data.get('class', ''),
                        created_at=convert_timestamp(drug_data.get('createdAt', {}))
                    )
                    db.add(drug)
                    imported_drugs += 1
            
            db.commit()
            print(f"✓ Imported {imported_drugs} drugs")
        except Exception as e:
            print(f"Error importing drugs: {e}")
            db.rollback()
        
        # Import dictionary words
        try:
            with open('attached_assets/words_1752089134451.json', 'r', encoding='utf-8') as f:
                words_data = json.load(f)
            
            imported_words = 0
            for word_data in words_data:
                existing_word = db.query(DictionaryWord).filter(DictionaryWord.id == word_data['id']).first()
                if not existing_word:
                    word = DictionaryWord(
                        id=word_data['id'],
                        name=word_data.get('name', ''),
                        kurdish=word_data.get('kurdish', ''),
                        arabic=word_data.get('arabic', ''),
                        description=word_data.get('description', ''),
                        barcode=word_data.get('barcode'),
                        is_saved=word_data.get('isSaved', False),
                        is_favorite=word_data.get('isFavorite', False)
                    )
                    db.add(word)
                    imported_words += 1
            
            db.commit()
            print(f"✓ Imported {imported_words} dictionary words")
        except Exception as e:
            print(f"Error importing dictionary words: {e}")
            db.rollback()
        
        # Import users
        try:
            with open('attached_assets/users_1752089134450.json', 'r', encoding='utf-8') as f:
                users_data = json.load(f)
            
            imported_users = 0
            for user_data in users_data:
                existing_user = db.query(User).filter(User.id == user_data['id']).first()
                if not existing_user:
                    user = User(
                        id=user_data['id'],
                        username=user_data.get('username', ''),
                        email=f"{user_data.get('username', 'user')}@example.com",
                        hashed_password="$2b$12$placeholder",
                        is_active=True,
                        is_admin=False,
                        total_points=user_data.get('total_points', 0),
                        today_points=user_data.get('today_points', 0),
                        created_at=datetime.utcnow(),
                        last_updated=convert_timestamp(user_data.get('last_updated', {}))
                    )
                    db.add(user)
                    imported_users += 1
            
            db.commit()
            print(f"✓ Imported {imported_users} users")
        except Exception as e:
            print(f"Error importing users: {e}")
            db.rollback()
        
        # Import normal ranges
        try:
            with open('attached_assets/Normal_Ranges_1752089134449.json', 'r', encoding='utf-8') as f:
                ranges_data = json.load(f)
            
            imported_ranges = 0
            for range_data in ranges_data:
                existing_range = db.query(NormalRange).filter(NormalRange.id == range_data['id']).first()
                if not existing_range:
                    normal_range = NormalRange(
                        id=range_data['id'],
                        name=range_data.get('name', ''),
                        species=range_data.get('species', ''),
                        category=range_data.get('category', ''),
                        unit=range_data.get('unit', ''),
                        min_value=range_data.get('minValue', ''),
                        max_value=range_data.get('maxValue', '')
                    )
                    db.add(normal_range)
                    imported_ranges += 1
            
            db.commit()
            print(f"✓ Imported {imported_ranges} normal ranges")
        except Exception as e:
            print(f"Error importing normal ranges: {e}")
            db.rollback()
        
        print("\n✓ Railway data import completed successfully!")
        
        # Show final counts
        books_count = db.query(Book).count()
        diseases_count = db.query(Disease).count()
        drugs_count = db.query(Drug).count()
        users_count = db.query(User).count()
        words_count = db.query(DictionaryWord).count()
        ranges_count = db.query(NormalRange).count()
        
        print(f"\n📊 Final Railway Database Status:")
        print(f"  - Books: {books_count}")
        print(f"  - Diseases: {diseases_count}")
        print(f"  - Drugs: {drugs_count}")
        print(f"  - Users: {users_count}")
        print(f"  - Dictionary Words: {words_count}")
        print(f"  - Normal Ranges: {ranges_count}")
        print(f"  - Total Records: {books_count + diseases_count + drugs_count + users_count + words_count + ranges_count}")
        
    except Exception as e:
        print(f"Error during data import: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    import_data_to_railway()