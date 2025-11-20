from __future__ import annotations

from pydantic import BaseModel


class ProjectBase(BaseModel):
    name: str
    slug: str | None = None


class ProjectCreate(ProjectBase):
    pass


class ProjectOut(ProjectBase):
    id: int

    class Config:
        orm_mode = True


class SceneCreate(BaseModel):
    project_id: int
    name: str


class SceneOut(BaseModel):
    id: int
    project_id: int
    name: str

    class Config:
        orm_mode = True


class LineCreate(BaseModel):
    scene_id: int
    speaker_id: int | None = None
    text: str


class LineOut(BaseModel):
    id: int
    scene_id: int
    speaker_id: int | None
    text: str

    class Config:
        orm_mode = True
