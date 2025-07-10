import json
import os
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Use environment database URL (will use Replit's PostgreSQL)
from database import engine, SessionLocal
from models import Base, Book, Disease, Drug, DictionaryWord, User, Question, Notification, Staff, TutorialVideo, NormalRange, AppLink, About

# Create all tables
Base.metadata.create_all(bind=engine)

def convert_timestamp(timestamp_obj):
    """Convert Firebase timestamp to datetime"""
    if isinstance(timestamp_obj, dict) and '_seconds' in timestamp_obj:
        return datetime.fromtimestamp(timestamp_obj['_seconds'])
    return datetime.utcnow()

def bulk_import_books(db: Session):
    """Import books using bulk operations"""
    try:
        with open('attached_assets/books_1752089134448.json', 'r', encoding='utf-8') as f:
            books_data = json.load(f)

        # Get existing IDs
        existing_ids = {book.id for book in db.query(Book.id).all()}

        # Prepare new books
        new_books = []
        for book_data in books_data:
            if book_data['id'] not in existing_ids:
                new_books.append(Book(
                    id=book_data['id'],
                    title=book_data.get('title', ''),
                    description=book_data.get('description', ''),
                    category=book_data.get('category', ''),
                    cover_url=book_data.get('coverUrl', ''),
                    download_url=book_data.get('downloadUrl', ''),
                    added_at=convert_timestamp(book_data.get('addedAt', {}))
                ))

        if new_books:
            db.add_all(new_books)
            db.commit()
            print(f"✓ Imported {len(new_books)} books")
        else:
            print("✓ No new books to import")

    except Exception as e:
        print(f"Error importing books: {e}")
        db.rollback()

def bulk_import_diseases(db: Session):
    """Import diseases using bulk operations"""
    try:
        with open('attached_assets/diseases_1752089134448.json', 'r', encoding='utf-8') as f:
            diseases_data = json.load(f)

        existing_ids = {disease.id for disease in db.query(Disease.id).all()}

        new_diseases = []
        for disease_data in diseases_data:
            if disease_data['id'] not in existing_ids:
                new_diseases.append(Disease(
                    id=disease_data['id'],
                    name=disease_data.get('name', ''),
                    kurdish=disease_data.get('kurdish', ''),
                    symptoms=disease_data.get('symptoms', ''),
                    cause=disease_data.get('cause', ''),
                    control=disease_data.get('control', ''),
                    created_at=datetime.utcnow()
                ))

        if new_diseases:
            db.add_all(new_diseases)
            db.commit()
            print(f"✓ Imported {len(new_diseases)} diseases")
        else:
            print("✓ No new diseases to import")

    except Exception as e:
        print(f"Error importing diseases: {e}")
        db.rollback()

def bulk_import_drugs(db: Session):
    """Import drugs using bulk operations"""
    try:
        with open('attached_assets/drugs_1752089134449.json', 'r', encoding='utf-8') as f:
            drugs_data = json.load(f)

        existing_ids = {drug.id for drug in db.query(Drug.id).all()}

        new_drugs = []
        for drug_data in drugs_data:
            if drug_data['id'] not in existing_ids:
                new_drugs.append(Drug(
                    id=drug_data['id'],
                    name=drug_data.get('name', ''),
                    usage=drug_data.get('usage', ''),
                    side_effect=drug_data.get('sideEffect', ''),
                    other_info=drug_data.get('otherInfo', ''),
                    drug_class=drug_data.get('class', ''),
                    created_at=convert_timestamp(drug_data.get('createdAt', {}))
                ))

        if new_drugs:
            db.add_all(new_drugs)
            db.commit()
            print(f"✓ Imported {len(new_drugs)} drugs")
        else:
            print("✓ No new drugs to import")

    except Exception as e:
        print(f"Error importing drugs: {e}")
        db.rollback()

def bulk_import_dictionary_words(db: Session):
    """Import dictionary words using bulk operations"""
    try:
        with open('attached_assets/words_1752089134451.json', 'r', encoding='utf-8') as f:
            words_data = json.load(f)

        existing_ids = {word.id for word in db.query(DictionaryWord.id).all()}

        new_words = []
        for word_data in words_data:
            if word_data['id'] not in existing_ids:
                new_words.append(DictionaryWord(
                    id=word_data['id'],
                    name=word_data.get('name', ''),
                    kurdish=word_data.get('kurdish', ''),
                    arabic=word_data.get('arabic', ''),
                    description=word_data.get('description', ''),
                    barcode=word_data.get('barcode'),
                    is_saved=word_data.get('isSaved', False),
                    is_favorite=word_data.get('isFavorite', False)
                ))

        if new_words:
            db.add_all(new_words)
            db.commit()
            print(f"✓ Imported {len(new_words)} dictionary words")
        else:
            print("✓ No new dictionary words to import")

    except Exception as e:
        print(f"Error importing dictionary words: {e}")
        db.rollback()

def bulk_import_users(db: Session):
    """Import users using bulk operations"""
    try:
        with open('attached_assets/users_1752089134450.json', 'r', encoding='utf-8') as f:
            users_data = json.load(f)

        existing_ids = {user.id for user in db.query(User.id).all()}

        new_users = []
        for user_data in users_data:
            if user_data['id'] not in existing_ids:
                new_users.append(User(
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
                ))

        if new_users:
            db.add_all(new_users)
            db.commit()
            print(f"✓ Imported {len(new_users)} users")
        else:
            print("✓ No new users to import")

    except Exception as e:
        print(f"Error importing users: {e}")
        db.rollback()

def bulk_import_normal_ranges(db: Session):
    """Import normal ranges using bulk operations"""
    try:
        with open('attached_assets/Normal_Ranges_1752089134449.json', 'r', encoding='utf-8') as f:
            ranges_data = json.load(f)

        existing_ids = {range.id for range in db.query(NormalRange.id).all()}

        new_ranges = []
        for range_data in ranges_data:
            if range_data['id'] not in existing_ids:
                new_ranges.append(NormalRange(
                    id=range_data['id'],
                    name=range_data.get('name', ''),
                    species=range_data.get('species', ''),
                    category=range_data.get('category', ''),
                    unit=range_data.get('unit', ''),
                    min_value=range_data.get('minValue', ''),
                    max_value=range_data.get('maxValue', '')
                ))

        if new_ranges:
            db.add_all(new_ranges)
            db.commit()
            print(f"✓ Imported {len(new_ranges)} normal ranges")
        else:
            print("✓ No new normal ranges to import")

    except Exception as e:
        print(f"Error importing normal ranges: {e}")
        db.rollback()

def main():
    """Main function to run optimized imports"""
    db = SessionLocal()

    try:
        print("🚀 Starting optimized data import...")

        # Import core data first
        bulk_import_books(db)
        bulk_import_diseases(db)
        bulk_import_drugs(db)
        bulk_import_dictionary_words(db)
        bulk_import_users(db)
        bulk_import_normal_ranges(db)

        # Import the rest of the data.
        def bulk_import_questions(db: Session):
            """Import questions using bulk operations"""
            try:
                with open('attached_assets/questions_1752089134450.json', 'r', encoding='utf-8') as f:
                    questions_data = json.load(f)

                existing_ids = {question.id for question in db.query(Question.id).all()}

                new_questions = []
                for question_data in questions_data:
                    if question_data['id'] not in existing_ids:
                        new_questions.append(Question(
                            id=question_data['id'],
                            text=question_data.get('text', ''),
                            user_id=question_data.get('userId', ''),
                            user_name=question_data.get('userName', ''),
                            user_email=question_data.get('userEmail', ''),
                            user_photo=question_data.get('userPhoto', ''),
                            likes=question_data.get('likes', 0),
                            timestamp=convert_timestamp(question_data.get('timestamp', {}))
                        ))

                if new_questions:
                    db.add_all(new_questions)
                    db.commit()
                    print(f"✓ Imported {len(new_questions)} questions")
                else:
                    print("✓ No new questions to import")

            except Exception as e:
                print(f"Error importing questions: {e}")
                db.rollback()

        bulk_import_questions(db)

        def bulk_import_notifications(db: Session):
            """Import notifications using bulk operations"""
            try:
                with open('attached_assets/notifications_1752089134449.json', 'r', encoding='utf-8') as f:
                    notifications_data = json.load(f)

                existing_ids = {notification.id for notification in db.query(Notification.id).all()}

                new_notifications = []
                for notification_data in notifications_data:
                    if notification_data['id'] not in existing_ids:
                        new_notifications.append(Notification(
                            id=notification_data['id'],
                            title=notification_data.get('title', ''),
                            body=notification_data.get('body', ''),
                            image_url=notification_data.get('imageUrl', ''),
                            timestamp=convert_timestamp(notification_data.get('timestamp', {}))
                        ))

                if new_notifications:
                    db.add_all(new_notifications)
                    db.commit()
                    print(f"✓ Imported {len(new_notifications)} notifications")
                else:
                    print("✓ No new notifications to import")

            except Exception as e:
                print(f"Error importing notifications: {e}")
                db.rollback()
        bulk_import_notifications(db)

        def bulk_import_staff(db: Session):
            """Import staff using bulk operations"""
            try:
                with open('attached_assets/staff_1752089134450.json', 'r', encoding='utf-8') as f:
                    staff_data = json.load(f)

                existing_ids = {staff.id for staff in db.query(Staff.id).all()}

                new_staff = []
                for staff_data in staff_data:
                    if staff_data['id'] not in existing_ids:
                        new_staff.append(Staff(
                            id=staff_data['id'],
                            name=staff_data.get('name', ''),
                            job=staff_data.get('job', ''),
                            description=staff_data.get('description', ''),
                            photo=staff_data.get('photo', ''),
                            facebook=staff_data.get('facebook', ''),
                            instagram=staff_data.get('instagram', ''),
                            twitter=staff_data.get('twitter', ''),
                            snapchat=staff_data.get('snapchat', '')
                        ))

                if new_staff:
                    db.add_all(new_staff)
                    db.commit()
                    print(f"✓ Imported {len(new_staff)} staff members")
                else:
                    print("✓ No new staff members to import")

            except Exception as e:
                print(f"Error importing staff: {e}")
                db.rollback()

        bulk_import_staff(db)

        def bulk_import_tutorial_videos(db: Session):
            """Import tutorial videos using bulk operations"""
            try:
                with open('attached_assets/tutorialVideos_1752089134450.json', 'r', encoding='utf-8') as f:
                    videos_data = json.load(f)

                existing_ids = {video.id for video in db.query(TutorialVideo.id).all()}

                new_videos = []
                for video_data in videos_data:
                    if video_data['id'] not in existing_ids:
                        new_videos.append(TutorialVideo(
                            id=video_data['id'],
                            title=video_data.get('Title', ''),
                            video_id=video_data.get('VideoID', ''),
                            created_at=datetime.utcnow()
                        ))

                if new_videos:
                    db.add_all(new_videos)
                    db.commit()
                    print(f"✓ Imported {len(new_videos)} tutorial videos")
                else:
                    print("✓ No new tutorial videos to import")

            except Exception as e:
                print(f"Error importing tutorial videos: {e}")
                db.rollback()

        bulk_import_tutorial_videos(db)

        def bulk_import_app_links(db: Session):
            """Import app links using bulk operations"""
            try:
                with open('attached_assets/app_links_1752089134448.json', 'r', encoding='utf-8') as f:
                    links_data = json.load(f)

                existing_ids = {link.id for link in db.query(AppLink.id).all()}

                new_links = []
                for link_data in links_data:
                    if link_data['id'] not in existing_ids:
                        new_links.append(AppLink(
                            id=link_data['id'],
                            url=link_data.get('url', '')
                        ))

                if new_links:
                    db.add_all(new_links)
                    db.commit()
                    print(f"✓ Imported {len(new_links)} app links")
                else:
                    print("✓ No new app links to import")

            except Exception as e:
                print(f"Error importing app links: {e}")
                db.rollback()

        bulk_import_app_links(db)

        def bulk_import_about(db: Session):
            """Import about information using bulk operations"""
            try:
                with open('attached_assets/about_page_1752089134447.json', 'r', encoding='utf-8') as f:
                    about_data = json.load(f)

                existing_ids = {about.id for about in db.query(About.id).all()}

                new_abouts = []
                for about_data in about_data:
                    if about_data['id'] not in existing_ids:
                        new_abouts.append(About(
                            id=about_data['id'],
                            text=about_data.get('text', ''),
                            exported_at=datetime.utcnow()
                        ))

                if new_abouts:
                    db.add_all(new_abouts)
                    db.commit()
                    print(f"✓ Imported {len(new_abouts)} about entries")
                else:
                    print("✓ No new about entries to import")

            except Exception as e:
                print(f"Error importing about information: {e}")
                db.rollback()
        bulk_import_about(db)

        print("\n✅ Data import completed successfully!")

        # Show final counts
        books_count = db.query(Book).count()
        diseases_count = db.query(Disease).count()
        drugs_count = db.query(Drug).count()
        users_count = db.query(User).count()
        words_count = db.query(DictionaryWord).count()
        ranges_count = db.query(NormalRange).count()
        questions_count = db.query(Question).count()
        notifications_count = db.query(Notification).count()
        staff_count = db.query(Staff).count()
        videos_count = db.query(TutorialVideo).count()
        links_count = db.query(AppLink).count()
        about_count = db.query(About).count()

        print(f"\n📊 Database Status:")
        print(f"  - Books: {books_count}")
        print(f"  - Diseases: {diseases_count}")
        print(f"  - Drugs: {drugs_count}")
        print(f"  - Users: {users_count}")
        print(f"  - Dictionary Words: {words_count}")
        print(f"  - Normal Ranges: {ranges_count}")
        print(f"  - Questions: {questions_count}")
        print(f"  - Notifications: {notifications_count}")
        print(f"  - Staff: {staff_count}")
        print(f"  - Tutorial Videos: {videos_count}")
        print(f"  - App Links: {links_count}")
        print(f"  - About: {about_count}")

    except Exception as e:
        print(f"❌ Error during import: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()