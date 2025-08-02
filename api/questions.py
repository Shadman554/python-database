from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import models
import schemas
import crud
from database import get_db
from auth import get_current_user, get_current_admin_user, security
from utils import create_paginated_response
import uuid

router = APIRouter()

@router.get("/by-user/{user_name}", response_model=schemas.PaginatedResponse)
async def get_questions_by_user(
    user_name: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get questions by user name"""
    questions = db.query(models.Question).filter(models.Question.user_name.ilike(f"%{user_name}%")).offset(skip).limit(limit).all()
    total = db.query(models.Question).filter(models.Question.user_name.ilike(f"%{user_name}%")).count()
    return create_paginated_response(questions, total, skip // limit + 1, limit)

@router.get("/", response_model=schemas.PaginatedResponse)
async def get_questions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get all questions with pagination"""
    try:
        questions = crud.get_items(db, models.Question, skip, limit)
        total = crud.count_items(db, models.Question)
        return create_paginated_response(questions, total, skip // limit + 1, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve questions: {str(e)}")

@router.get("/{question_id}", response_model=schemas.Question)
async def get_question(question_id: str, db: Session = Depends(get_db)):
    """Get a specific question by ID"""
    question = crud.get_item(db, models.Question, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question

@router.post("/", response_model=schemas.Question)
async def create_question(
    question: schemas.QuestionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(lambda: get_current_user(security, db))
):
    """Create a new question"""
    try:
        question_data = question.dict()
        question_data['id'] = str(uuid.uuid4())
        question_data['user_id'] = current_user.id
        question_data['user_name'] = current_user.username
        question_data['user_email'] = current_user.email
        
        db_question = crud.create_item(db, models.Question, question_data)
        
        # Award points for asking a question
        crud.update_user_points(db, current_user.id, 5)
        
        # Send notification for new question
        from utils import send_content_notification
        await send_content_notification("question", question_data.get('question', 'New Question'), question_data['id'])
        
        return db_question
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create question: {str(e)}")

@router.put("/{question_id}", response_model=schemas.Question)
async def update_question(
    question_id: str,
    question: schemas.QuestionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(lambda: get_current_user(security, db))
):
    """Update a question (only by owner or admin)"""
    db_question = crud.get_item(db, models.Question, question_id)
    if not db_question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    # Check if user owns the question or is admin
    if db_question.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to update this question")
    
    try:
        updated_question = crud.update_item(db, db_question, question.dict())
        return updated_question
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update question: {str(e)}")

@router.delete("/{question_id}")
async def delete_question(
    question_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(lambda: get_current_user(security, db))
):
    """Delete a question (only by owner or admin)"""
    db_question = crud.get_item(db, models.Question, question_id)
    if not db_question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    # Check if user owns the question or is admin
    if db_question.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to delete this question")
    
    try:
        crud.delete_item(db, db_question)
        return {"message": "Question deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete question: {str(e)}")

@router.post("/{question_id}/like")
async def like_question(
    question_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(lambda: get_current_user(security, db))
):
    """Like a question"""
    db_question = crud.get_item(db, models.Question, question_id)
    if not db_question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    try:
        db_question.likes += 1
        db.commit()
        
        # Award points to question owner for getting a like
        if db_question.user_id != current_user.id:
            crud.update_user_points(db, db_question.user_id, 1)
        
        return {"message": "Question liked", "likes": db_question.likes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to like question: {str(e)}")

@router.get("/user/{user_id}")
async def get_user_questions(
    user_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get all questions by a specific user"""
    try:
        questions = db.query(models.Question).filter(models.Question.user_id == user_id).offset(skip).limit(limit).all()
        total = db.query(models.Question).filter(models.Question.user_id == user_id).count()
        return create_paginated_response(questions, total, skip // limit + 1, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve user questions: {str(e)}")
