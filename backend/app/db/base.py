"""Declarative base: the registry that maps ORM models to database tables."""
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass