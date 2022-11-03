from sqlalchemy import Column, Integer, String, DateTime
from base import Base


class Stats(Base):
    """Processing Statistics"""

    __tablename__ = "stats"

    id = Column(Integer, primary_key=True)
    num_answers = Column(Integer, nullable=False)
    max_randInt_answers = Column(Integer, nullable=True)
    num_questions = Column(Integer, nullable=False)
    max_randInt_questions = Column(Integer, nullable=True)
    last_updated = Column(DateTime, nullable=False)


def __init__(self, num_answers, max_randInt_answers, num_questions, max_randInt_questions, last_updated):
    """Initializes a processing statistics object"""
    self.num_answers = num_answers
    self.max_randInt_answers = max_randInt_answers
    self.num_questions = num_questions
    self.max_randInt_questions = max_randInt_questions
    self.last_updated = last_updated


def to_dict(self):
    """dictionary representation of a statistics"""
    this = {}
    this["num_answers"] = self.num_answers
    this["max_randInt_answers"] = self.max_randInt_answers
    this["num_questions"] = self.num_questions
    this["max_randInt_questions"] = self.max_randInt_questions
    this["last_updated"] = self.last_updated.strftime("%Y-%m-%d %H:%M:%S")
    return this
