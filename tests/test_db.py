from __future__ import annotations

from app.models import Title


def test_can_insert_and_query_title(session):
    # Insert a row
    title = Title(name='Test Work')
    session.add(title)
    session.commit()
    session.refresh(title)

    # Query it back
    result = session.query(Title).filter_by(slug='test-work').first()

    assert result is not None
    assert result.name == 'Test Work'
    assert result.slug == 'test-work'
    assert result.id


def test_example_scene(example_scene):
    assert example_scene.id is not None
    assert example_scene.lines != []
