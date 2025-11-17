from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Title
from app.schemas import TitleCreate, TitleOut

router = APIRouter()


@router.post('/', response_model=TitleOut)
def create_title(payload: TitleCreate, db: Session = Depends(get_db)):
    title = Title(name=payload.name, slug=payload.slug)
    db.add(title)
    db.commit()
    db.refresh(title)
    return title


@router.get('/', response_model=list[TitleOut])
def list_titles(db: Session = Depends(get_db)):
    return db.query(Title).all()
