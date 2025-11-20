from __future__ import annotations

from base64 import b64encode
from typing import AsyncGenerator

from openai import AsyncOpenAI

from app.config import OPENAI_API_KEY, OPENAI_MODEL
from app.models import Entry

SEPARATOR = '\x1f'

client = AsyncOpenAI(api_key=OPENAI_API_KEY)


def get_prompt(entry: Entry) -> str:
    parts = [
        f'Translate a text from {entry.scene.project.name}.',
        'Return ONLY the translation for the last entry.',
    ]
    if entry.scene.name:
        parts.append(f'Scene: {entry.scene.name}.')
    for other_entry in entry.scene.entries:
        parts.append('-------')
        parts.append(other_entry.text)
    return '\n'.join(parts)


async def stream_translation(entry: Entry) -> AsyncGenerator[str]:
    prompt = get_prompt(entry)
    stream = await client.responses.create(model=OPENAI_MODEL, input=prompt, stream=True)
    async for event in stream:
        match event.type:
            case 'response.output_text.delta':
                yield event.delta
            case 'response.created' | 'response.in_progress' | 'response.output_item.added' | 'response.content_part.added':
                pass  # nothing to do, we're just waiting
            case 'response.output_text.done':
                return  # done
            case _:
                raise NotImplementedError(event)


async def stream_ocr_and_translation(entry: Entry) -> AsyncGenerator[tuple[str, str]]:
    assert entry.image_path, 'Entry must have been created from an image'

    prompt = [
        f'Extract and translate text from an image from {entry.scene.project.name}.',
        f'Between the extracted and translated text just insert this separator: {SEPARATOR}.',
        'The image is included with this request.',
        'Send me ONLY the extracted text and translated text; do not talk to me.',
    ]
    if len(entry.scene.entries) > 1:
        prompt.append('Previous scene context:')
        for number, prev_entry in enumerate(entry.scene.entries[:-1], 1):
            prompt.append(f'{number}. {prev_entry.text}')

    with open(entry.image_path, 'rb') as image_file:
        base64_image = b64encode(image_file.read()).decode('utf-8')

    stream = await client.responses.create(
        model=OPENAI_MODEL,
        stream=True,
        input=[
            {
                'role': 'user',
                'content': [
                    {
                        'type': 'input_text',
                        'text': '\n'.join(prompt)
                    },
                    {
                        'type': 'input_image',
                        'image_url': f'data:image/jpeg;base64,{base64_image}',
                    },
                ]
            },
        ],
    )

    text = ''
    translation = ''
    sequence = 0
    async for event in stream:
        match event.type:
            case 'response.output_text.delta':
                if event.delta == SEPARATOR:
                    sequence += 1
                elif sequence == 0:
                    text += event.delta
                elif sequence == 1:
                    translation += event.delta
                else:
                    raise RuntimeError(f'invalid sequence {sequence}')
                yield (text, translation)
            case 'response.completed':
                break
            case _:
                pass
