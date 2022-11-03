from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime


class Answer(Base):
    """Answer"""

    __tablename__ = "answers"

    id = Column(Integer, primary_key=True)
    answer_id = Column(Integer, nullable=False)
    description = Column(String(250), nullable=False)
    answer = Column(String(250), nullable=False)
    randomInt = Column(Integer, nullable=False)
    trace_id = Column(String(100), nullable=False)
    date_created = Column(DateTime, nullable=False)

    def __init__(self, answer_id, description, answer, randomInt, trace_id):
        """Initializes an answer post"""
        self.answer_id = answer_id
        self.description = description
        self.answer = answer
        self.randomInt = randomInt
        self.trace_id = trace_id
        self.date_created = datetime.datetime.now()

    def to_dict(self):
        """Dictionary Representation of an answer post"""
        dict = {}
        dict["id"] = self.id
        dict["answer_id"] = self.answer_id
        dict["description"] = self.description
        dict["answer"] = self.answer
        dict["randomInt"] = self.randomInt
        dict["trace_id"] = self.trace_id
        dict["date_created"] = self.date_created

        return dict
