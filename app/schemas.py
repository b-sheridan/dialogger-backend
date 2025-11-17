from __future__ import annotations

from pydantic import BaseModel


class TitleBase(BaseModel):
    name: str
    slug: str


class TitleCreate(TitleBase):
    pass


class TitleOut(TitleBase):
    id: int

    class Config:
        orm_mode = True
