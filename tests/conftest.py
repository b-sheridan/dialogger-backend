from __future__ import annotations

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models import Base, Character, Line, Scene, Title


# Use SQLite in-memory DB for tests
TEST_DATABASE_URL = 'sqlite:///:memory:'


@pytest.fixture
def session():
    engine = create_engine(TEST_DATABASE_URL, future=True)
    TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

    # Create fresh schema for each test
    Base.metadata.create_all(bind=engine)

    db = TestingSession()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def example_scene(session):
    xenogears = Title(name='Xenogears', slug='xenogears')

    fei = Character(name='フェイ', title=xenogears)
    aruru = Character(name='アルル', title=xenogears)

    scene = Scene(
        title=xenogears,
        name='プロローグ、フェイとアルル',
        lines=[
            Line(
                character=fei,
                original_text="""やあ、アルル。
それが花嫁のドレスかい？""",
            ),
            Line(
                character=aruru,
                original_text="""フェイ！？
ああ……、ビックリした！""",
            ),
        ],
    )

    session.add(scene)
    session.commit()

    return scene
