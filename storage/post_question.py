from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime


class Question(Base):
    """Question"""

    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, nullable=False)
    description = Column(String(250), nullable=False)
    question = Column(String(250), nullable=False)
    randomInt = Column(Integer, nullable=False)
    trace_id = Column(String(100), nullable=False)
    date_created = Column(DateTime, nullable=False)

    def __init__(self, question_id, description, question, randomInt, trace_id):
        """Initializes a question post"""
        self.question_id = question_id
        self.description = description
        self.question = question
        self.randomInt = randomInt
        self.trace_id = trace_id
        self.date_created = datetime.datetime.now()

    def to_dict(self):
        """Dictionary Representation of a question post"""
        dict = {}
        dict["id"] = self.id
        dict["question_id"] = self.question_id
        dict["description"] = self.description
        dict["question"] = self.question
        dict["randomInt"] = self.randomInt
        dict["trace_id"] = self.trace_id
        dict["date_created"] = self.date_created

        return dict
