from __future__ import annotations

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models import Base, Title


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


def test_can_insert_and_query_title(session):
    # Insert a row
    title = Title(name='Test Work', slug='test-work')
    session.add(title)
    session.commit()
    session.refresh(title)

    # Query it back
    result = session.query(Title).filter_by(slug='test-work').first()

    assert result is not None
    assert result.name == 'Test Work'
    assert result.slug == 'test-work'
    assert result.id
