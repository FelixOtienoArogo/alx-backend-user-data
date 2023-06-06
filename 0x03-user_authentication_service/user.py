#!/usr/bin/env python3
"""User model."""
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


engine = create_engine("sqlite:///:memory", echo=False)
Base = declarative_base()


class User(Base):
    """Model for table named users."""

    __tablename__: str = 'users'

    id: Column = Column(Integer, primary_key=True)
    email: Column = Column(String(length=250), nullable=False)
    hashed_password: Column = Column(String(length=250), nullable=False)
    session_id: Column = Column(String(length=250), nullable=True)
    reset_token: Column = Column(String(length=250), nullable=True)
