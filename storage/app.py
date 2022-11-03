# Jake Martin - A01158619
# ACIT3855

import connexion
from connexion import NoContent

from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from post_question import Question
from post_answer import Answer

import yaml
import logging
import logging.config
import datetime as dt

import json
from pykafka import KafkaClient
from pykafka.common import OffsetType
from threading import Thread

# load app config
with open("app_config.yml", "r") as f:
    app_config = yaml.safe_load(f.read())

# load logging config
with open("log_config.yml", "r") as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

# create logger
logger = logging.getLogger("basicLogger")

DB_USER = app_config["datastore"]["user"]
DB_PASS = app_config["datastore"]["password"]
DB_HOST = app_config["datastore"]["hostname"]
DB_PORT = app_config["datastore"]["port"]
DB_DB = app_config["datastore"]["db"]

# log attempt to connect to AWS vm mysql
logger.info(f"Connecting to DB. Hostname:{DB_HOST}, Port:{DB_PORT}")

DB_ENGINE = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_DB}"
)
# DB_ENGINE = create_engine("sqlite:///readings.sqlite")
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)


def add_answers(body):
    """Receives an answer post"""

    session = DB_SESSION()

    ap = Answer(
        body["answer_id"],
        body["description"],
        body["answer"],
        body["randomInt"],
        body["trace_id"],
    )

    try:
        session.add(ap)
        session.commit()
        session.close()
        logger.debug(
            f"Stored event add_answers request with a trace id of {body['trace_id']}"
        )
    except IntegrityError:
        logger.debug('Duplicate entry detected, Rolling back...')
        session.rollback()

    return NoContent, 201


def add_questions(body):
    """Receives a question post"""

    session = DB_SESSION()

    qp = Question(
        body["question_id"],
        body["description"],
        body["question"],
        body["randomInt"],
        body["trace_id"],
    )

    try:
        session.add(qp)
        session.commit()
        session.close()
        logger.debug(
            f"Stored event add_questions request with a trace id of {body['trace_id']}"
        )
    except IntegrityError:
        logger.debug('Duplicate entry detected, Rolling back...')
        session.rollback()

    return NoContent, 201


def get_answer(timestamp):
    """Get answer with timestamp"""

    session = DB_SESSION()
    timestamp_datetime = dt.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    answers = session.query(Answer).filter(
        Answer.date_created >= timestamp_datetime)
    results = []

    for answer in answers:
        results.append(answer.to_dict())

    session.close()
    logger.info(
        f"Query for Answers after {timestamp} returns {len(results)} results")

    return results, 200


def get_question(timestamp):
    """Get answer with timestamp"""

    session = DB_SESSION()
    timestamp_datetime = dt.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    questions = session.query(Question).filter(
        Question.date_created >= timestamp_datetime
    )
    results = []

    for question in questions:
        results.append(question.to_dict())

    session.close()
    logger.info(
        f"Query for Questions after {timestamp} returns {len(results)} results")

    return results, 200


def process_messages():
    """ Process event messages """
    hostname = "%s:%d" % (app_config["events"]["hostname"],
                          app_config["events"]["port"])

    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config["events"]["topic"])]

    # Create a consume on a consumer group, that only reads new messages
    # (uncommitted messages) when the service re-starts (i.e., it doesn't
    # read all the old messages from the history in the message queue).
    consumer = topic.get_simple_consumer(consumer_group=b'event_group',
                                        reset_offset_on_start=False,
                                        auto_offset_reset=OffsetType.LATEST)

    # This is blocking - it will wait for a new message
    for msg in consumer:
        msg_str = msg.value.decode('utf-8')
        msg = json.loads(msg_str)
        logger.info("Message: %s" % msg)
        payload = msg["payload"]
        if msg["type"] == "answer":
            # Store the answer event to the DB
            logger.info(f'Adding answer event to DB: {payload}')
            add_answers(payload)
        elif msg["type"] == "question":
            # Store the question event to the DB
            logger.info(f'Adding question event to DB: {payload}')
            add_questions(payload)
        # Commit the new message as being read
        consumer.commit_offsets()


app = connexion.FlaskApp(__name__, specification_dir="")
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    t1 = Thread(target=process_messages)
    t1.setDaemon(True)
    t1.start()
    app.run(port=8090, debug=True)
