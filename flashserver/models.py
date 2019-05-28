"""Flashcard models"""

from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, DateTime, String, Integer, ForeignKey

Base = declarative_base()


class Language(Base):
    """A lookup table for languages"""

    __tablename__ = 'fc_language'
    id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    language = Column(String, nullable=False)


class User(Base):
    """A user who learns."""
    __tablename__ = 'fc_user'
    id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    created_at = Column(DateTime, default=datetime.now, index=True, nullable=False)
    password_hash = Column(String(64), nullable=False)
    username = Column(String(64), nullable=False, index=True)


class PracticeList(Base):
    """A list which verbs can be linked to, to be learned in its entirety."""
    __tablename__ = 'fc_practicelist'
    id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, ForeignKey('fc_user.id'))
    list_name = Column(String, nullable=False)


class VerbGroup(Base):
    """A group of verbs (arbitrary: easy verbs, same meaning, etc.)"""

    __tablename__ = 'fc_verbgroup'
    id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    group_name = Column(String, nullable=False)
    ordering = Column(Integer, nullable=False)


class Subject(Base):
    """A subject: meaning i, you, him/her, them, etc..."""

    __tablename__ = 'fc_subject'
    id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    subject_name = Column(String, nullable=False)
    language = Column(Integer, ForeignKey('fc_language.id'))


class VerbData(Base):
    """A verb and its translation"""
    __tablename__ = 'fc_verbdata'
    id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    group_id = Column(Integer, ForeignKey('fc_verbgroup.id'))
    name = Column(String, nullable=False)
    language = Column(Integer, ForeignKey('fc_language.id'))


class TenseGroup(Base):
    """A tense"""
    __tablename__ = 'fc_tensegroup'
    id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    tense_name = Column(String, nullable=False)
    ordering = Column(Integer, nullable=False)


class VerbToList(Base):
    """Linkage to put verbs in lists"""

    __tablename__ = 'fc_verbtolist'
    id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    practice_list_id = Column(Integer, ForeignKey('fc_practicelist.id'))
    group_id = Column(Integer, ForeignKey('fc_verbgroup.id'))
    tense_id = Column(Integer, ForeignKey('fc_tensegroup.id'))


class PracticeQuestion(Base):
    """A question we can select and display to the user."""

    __tablename__ = 'fc_practicequestions'
    id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    verb_id = Column(Integer, ForeignKey('fc_verbdata.id'))
    tense_id = Column(Integer, ForeignKey('fc_tensegroup.id'))
    question_text = Column(String, nullable=False)
    answer_text = Column(String, nullable=False)
    qlang = Column(Integer, ForeignKey('fc_language.id'))
    alang = Column(Integer, ForeignKey('fc_language.id'))
    subject_id = Column(Integer, ForeignKey('fc_subject.id'))


class AnswerStatus(Base):
    """For each list, each question can be a member, if it is and has been answered, this exists"""

    __tablename__ = 'fc_answerstatus'
    id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    score = Column(Integer, nullable=False)
    question_id = Column(Integer, ForeignKey('fc_practicequestions.id'))
    last_answered = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    list_id = Column(Integer, ForeignKey('fc_practicelist.id'))
    # TODO: Add func to find num answers today


class AnswerLog(Base):
    """A log of all the answers."""

    __tablename__ = 'fc_answerlog'
    id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    question_id = Column(Integer, ForeignKey('fc_practicequestions.id'))
    value_entered = Column(String, nullable=False)
    time_answered = Column(DateTime, default=datetime.now, index=True, nullable=False)
    list_id = Column(Integer, ForeignKey('fc_practicelist.id'))
