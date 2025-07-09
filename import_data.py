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

def import_books(db: Session):
    """Import books from JSON file"""
    try:
        with open('attached_assets/books_1752089134448.json', 'r', encoding='utf-8') as f:
            books_data = json.load(f)
        
        for book_data in books_data:
            # Check if book already exists
            existing_book = db.query(Book).filter(Book.id == book_data['id']).first()
            if existing_book:
                continue
                
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
        
        db.commit()
        print(f"Imported {len(books_data)} books")
    except Exception as e:
        print(f"Error importing books: {e}")
        db.rollback()

def import_diseases(db: Session):
    """Import diseases from JSON file"""
    try:
        with open('attached_assets/diseases_1752089134448.json', 'r', encoding='utf-8') as f:
            diseases_data = json.load(f)
        
        for disease_data in diseases_data:
            # Check if disease already exists
            existing_disease = db.query(Disease).filter(Disease.id == disease_data['id']).first()
            if existing_disease:
                continue
                
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
        
        db.commit()
        print(f"Imported {len(diseases_data)} diseases")
    except Exception as e:
        print(f"Error importing diseases: {e}")
        db.rollback()

def import_drugs(db: Session):
    """Import drugs from JSON file"""
    try:
        with open('attached_assets/drugs_1752089134449.json', 'r', encoding='utf-8') as f:
            drugs_data = json.load(f)
        
        for drug_data in drugs_data:
            # Check if drug already exists
            existing_drug = db.query(Drug).filter(Drug.id == drug_data['id']).first()
            if existing_drug:
                continue
                
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
        
        db.commit()
        print(f"Imported {len(drugs_data)} drugs")
    except Exception as e:
        print(f"Error importing drugs: {e}")
        db.rollback()

def import_dictionary_words(db: Session):
    """Import dictionary words from JSON file"""
    try:
        with open('attached_assets/words_1752089134451.json', 'r', encoding='utf-8') as f:
            words_data = json.load(f)
        
        for word_data in words_data:
            # Check if word already exists
            existing_word = db.query(DictionaryWord).filter(DictionaryWord.id == word_data['id']).first()
            if existing_word:
                continue
                
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
        
        db.commit()
        print(f"Imported {len(words_data)} dictionary words")
    except Exception as e:
        print(f"Error importing dictionary words: {e}")
        db.rollback()

def import_users(db: Session):
    """Import users from JSON file"""
    try:
        with open('attached_assets/users_1752089134450.json', 'r', encoding='utf-8') as f:
            users_data = json.load(f)
        
        for user_data in users_data:
            # Check if user already exists
            existing_user = db.query(User).filter(User.id == user_data['id']).first()
            if existing_user:
                continue
                
            user = User(
                id=user_data['id'],
                username=user_data.get('username', ''),
                email=f"{user_data.get('username', 'user')}@example.com",  # Generate email since not provided
                hashed_password="$2b$12$placeholder",  # Placeholder password hash
                is_active=True,
                is_admin=False,
                total_points=user_data.get('total_points', 0),
                today_points=user_data.get('today_points', 0),
                created_at=datetime.utcnow(),
                last_updated=convert_timestamp(user_data.get('last_updated', {}))
            )
            db.add(user)
        
        db.commit()
        print(f"Imported {len(users_data)} users")
    except Exception as e:
        print(f"Error importing users: {e}")
        db.rollback()

def import_questions(db: Session):
    """Import questions from JSON file"""
    try:
        with open('attached_assets/questions_1752089134450.json', 'r', encoding='utf-8') as f:
            questions_data = json.load(f)
        
        for question_data in questions_data:
            # Check if question already exists
            existing_question = db.query(Question).filter(Question.id == question_data['id']).first()
            if existing_question:
                continue
                
            question = Question(
                id=question_data['id'],
                text=question_data.get('text', ''),
                user_id=question_data.get('userId', ''),
                user_name=question_data.get('userName', ''),
                user_email=question_data.get('userEmail', ''),
                user_photo=question_data.get('userPhoto', ''),
                likes=question_data.get('likes', 0),
                timestamp=convert_timestamp(question_data.get('timestamp', {}))
            )
            db.add(question)
        
        db.commit()
        print(f"Imported {len(questions_data)} questions")
    except Exception as e:
        print(f"Error importing questions: {e}")
        db.rollback()

def import_notifications(db: Session):
    """Import notifications from JSON file"""
    try:
        with open('attached_assets/notifications_1752089134449.json', 'r', encoding='utf-8') as f:
            notifications_data = json.load(f)
        
        for notification_data in notifications_data:
            # Check if notification already exists
            existing_notification = db.query(Notification).filter(Notification.id == notification_data['id']).first()
            if existing_notification:
                continue
                
            notification = Notification(
                id=notification_data['id'],
                title=notification_data.get('title', ''),
                body=notification_data.get('body', ''),
                image_url=notification_data.get('imageUrl', ''),
                timestamp=convert_timestamp(notification_data.get('timestamp', {}))
            )
            db.add(notification)
        
        db.commit()
        print(f"Imported {len(notifications_data)} notifications")
    except Exception as e:
        print(f"Error importing notifications: {e}")
        db.rollback()

def import_staff(db: Session):
    """Import staff from JSON file"""
    try:
        with open('attached_assets/staff_1752089134450.json', 'r', encoding='utf-8') as f:
            staff_data = json.load(f)
        
        for staff_member_data in staff_data:
            # Check if staff member already exists
            existing_staff = db.query(Staff).filter(Staff.id == staff_member_data['id']).first()
            if existing_staff:
                continue
                
            staff_member = Staff(
                id=staff_member_data['id'],
                name=staff_member_data.get('name', ''),
                job=staff_member_data.get('job', ''),
                description=staff_member_data.get('description', ''),
                photo=staff_member_data.get('photo', ''),
                facebook=staff_member_data.get('facebook', ''),
                instagram=staff_member_data.get('instagram', ''),
                twitter=staff_member_data.get('twitter', ''),
                snapchat=staff_member_data.get('snapchat', '')
            )
            db.add(staff_member)
        
        db.commit()
        print(f"Imported {len(staff_data)} staff members")
    except Exception as e:
        print(f"Error importing staff: {e}")
        db.rollback()

def import_tutorial_videos(db: Session):
    """Import tutorial videos from JSON file"""
    try:
        with open('attached_assets/tutorialVideos_1752089134450.json', 'r', encoding='utf-8') as f:
            videos_data = json.load(f)
        
        for video_data in videos_data:
            # Check if video already exists
            existing_video = db.query(TutorialVideo).filter(TutorialVideo.id == video_data['id']).first()
            if existing_video:
                continue
                
            video = TutorialVideo(
                id=video_data['id'],
                title=video_data.get('Title', ''),
                video_id=video_data.get('VideoID', ''),
                created_at=datetime.utcnow()
            )
            db.add(video)
        
        db.commit()
        print(f"Imported {len(videos_data)} tutorial videos")
    except Exception as e:
        print(f"Error importing tutorial videos: {e}")
        db.rollback()

def import_normal_ranges(db: Session):
    """Import normal ranges from JSON file"""
    try:
        with open('attached_assets/Normal_Ranges_1752089134449.json', 'r', encoding='utf-8') as f:
            ranges_data = json.load(f)
        
        for range_data in ranges_data:
            # Check if range already exists
            existing_range = db.query(NormalRange).filter(NormalRange.id == range_data['id']).first()
            if existing_range:
                continue
                
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
        
        db.commit()
        print(f"Imported {len(ranges_data)} normal ranges")
    except Exception as e:
        print(f"Error importing normal ranges: {e}")
        db.rollback()

def import_app_links(db: Session):
    """Import app links from JSON file"""
    try:
        with open('attached_assets/app_links_1752089134448.json', 'r', encoding='utf-8') as f:
            links_data = json.load(f)
        
        for link_data in links_data:
            # Check if link already exists
            existing_link = db.query(AppLink).filter(AppLink.id == link_data['id']).first()
            if existing_link:
                continue
                
            app_link = AppLink(
                id=link_data['id'],
                url=link_data.get('url', '')
            )
            db.add(app_link)
        
        db.commit()
        print(f"Imported {len(links_data)} app links")
    except Exception as e:
        print(f"Error importing app links: {e}")
        db.rollback()

def import_about(db: Session):
    """Import about information from JSON file"""
    try:
        with open('attached_assets/about_page_1752089134447.json', 'r', encoding='utf-8') as f:
            about_data = json.load(f)
        
        for about_item in about_data:
            # Check if about already exists
            existing_about = db.query(About).filter(About.id == about_item['id']).first()
            if existing_about:
                continue
                
            about = About(
                id=about_item['id'],
                text=about_item.get('text', ''),
                exported_at=datetime.utcnow()
            )
            db.add(about)
        
        db.commit()
        print(f"Imported {len(about_data)} about entries")
    except Exception as e:
        print(f"Error importing about information: {e}")
        db.rollback()

def main():
    """Main function to run all imports"""
    db = SessionLocal()
    
    try:
        print("Starting data import...")
        
        # Import all data
        import_books(db)
        import_diseases(db)
        import_drugs(db)
        import_dictionary_words(db)
        import_users(db)
        import_questions(db)
        import_notifications(db)
        import_staff(db)
        import_tutorial_videos(db)
        import_normal_ranges(db)
        import_app_links(db)
        import_about(db)
        
        print("Data import completed successfully!")
        
    except Exception as e:
        print(f"Error during data import: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()
