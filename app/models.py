from __future__ import annotations

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Project(Base):
    __tablename__ = 'projects'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)

    scenes: Mapped[list[Scene]] = relationship(back_populates='project', cascade='all, delete-orphan')


class Scene(Base):
    __tablename__ = 'scenes'

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey('projects.id'), nullable=False)
    name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    position: Mapped[int] = mapped_column(nullable=False, default=0)

    project: Mapped[Project] = relationship(back_populates='scenes')
    lines: Mapped[list[Line]] = relationship(back_populates='scene', cascade='all, delete-orphan', order_by='Line.position')


class Line(Base):
    __tablename__ = 'lines'

    id: Mapped[int] = mapped_column(primary_key=True)
    scene_id: Mapped[int] = mapped_column(ForeignKey('scenes.id'), nullable=False)
    position: Mapped[int] = mapped_column(nullable=False, default=0)
    speaker: Mapped[str | None] = mapped_column(Text, nullable=True)
    original_text: Mapped[str] = mapped_column(Text, nullable=False)
    translated_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    scene: Mapped[Scene] = relationship(back_populates='lines')
