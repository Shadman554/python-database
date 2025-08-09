
from sqlalchemy import create_engine, text
from database import DATABASE_URL, Base
from models import Instrument, Note, UrineSlide, StoolSlide, OtherSlide
import sys

def migrate_collections():
    """Drop tutorial_videos table and create new collections"""
    
    engine = create_engine(DATABASE_URL)
    
    try:
        with engine.connect() as conn:
            # Drop tutorial_videos table
            print("Dropping tutorial_videos table...")
            conn.execute(text("DROP TABLE IF EXISTS tutorial_videos CASCADE;"))
            conn.commit()
            print("✓ Dropped tutorial_videos table")
            
        # Create new tables
        print("Creating new tables...")
        Base.metadata.create_all(bind=engine, tables=[
            Instrument.__table__,
            Note.__table__,
            UrineSlide.__table__,
            StoolSlide.__table__,
            OtherSlide.__table__
        ])
        print("✓ Created new tables:")
        print("  - instruments")
        print("  - notes") 
        print("  - urine_slides")
        print("  - stool_slides")
        print("  - other_slides")
        
        print("\n🎉 Migration completed successfully!")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    migrate_collections()
