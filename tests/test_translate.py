from __future__ import annotations

import pytest

from app.models import Entry, Scene, Project
from app.services.translate import get_prompt, stream_ocr_and_translation, stream_translation


def test_get_prompt_doesnt_barf(example_scene):
    """Sanity test that this doesn't throw."""
    prompt = get_prompt(example_scene.entries[-1])
    assert prompt


@pytest.mark.asyncio
@pytest.mark.openai
async def test_stream_translation(example_scene):
    async for token in stream_translation(example_scene.entries[-1]):
        assert token


@pytest.mark.asyncio
@pytest.mark.openai
async def test_stream_ocr_and_translation():
    project = Project(name='Xenogears')
    scene = Scene(project=project)
    entry = Entry(scene=scene, image_path='tests/data/xenogears-320-240.png')

    async for (text, translation) in stream_ocr_and_translation(entry):
        entry.text = text
        entry.translation = translation

    assert entry.text
    assert entry.translation
