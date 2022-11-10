# Jake Martin - A01158619
# ACIT3855

import connexion
from connexion import NoContent
import swagger_ui_bundle
import requests
from flask_cors import CORS, cross_origin
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from stat_class import Stats
import os
import json
import yaml
import logging
import logging.config
import datetime as dt

# load app config
with open("app_config.yml", "r") as f:
    app_config = yaml.safe_load(f.read())

# load logging config
with open("log_config.yml", "r") as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

# create logger
logger = logging.getLogger("basicLogger")

DB_ENGINE = create_engine(f"sqlite:///{app_config['datastore']['filename']}")
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)


def request_answers(last_updated):

    ans_req = requests.get(
        url=app_config["eventstore"]["url"] +
        f"/getAns?timestamp={last_updated}"
    )

    # log info message with number of events received
    # log error message if not status_code 200
    if ans_req.status_code != 200:
        logger.error(f"Error, status code received: {ans_req.status_code}")
        num_answers = None
        max_randInt_answers = None
    else:
        logger.info(f"Number of answer events received: {len(ans_req.json())}")

        # for each event in request, log debug message if includes trace_id
        if len(ans_req.json()) > 0:
            ans_rand_int = []
            # print(ans_req.json())
            for event in ans_req.json():
                if event:
                    logger.debug(str(event["trace_id"]))
                    ans_rand_int.append(event["randomInt"])

            # calc stats
            num_answers = len(ans_req.json())
            max_randInt_answers = max(ans_rand_int)
        else:
            num_answers = None
            max_randInt_answers = None

    return num_answers, max_randInt_answers


def request_questions(last_updated):
    que_req = requests.get(
        url=app_config["eventstore"]["url"] +
        f"/getQue?timestamp={last_updated}"
    )
    # log info message with number of events received
    # log error message if not status_code 200
    if que_req.status_code != 200:
        logger.error(f"Error, status code received: {que_req.status_code}")
        num_questions = None
        max_randInt_questions = None
    else:
        logger.info(
            f"Number of question events received: {len(que_req.json())}")

        # for each event in request, log debug message if includes trace_id
        if len(que_req.json()) > 0:
            que_rand_int = []
            # print(que_req.json())
            for event in que_req.json():
                if event:
                    logger.debug(str(event["trace_id"]))
                    que_rand_int.append(event["randomInt"])

            # calc stats
            num_questions = len(que_req.json())
            max_randInt_questions = max(que_rand_int)
        else:
            num_questions = None
            max_randInt_questions = None

    return num_questions, max_randInt_questions


def get_stats():
    """show stats info on request @ /stats"""
    print('\n')
    logger.info("Request has started.")

    session = DB_SESSION()
    results = session.query(Stats).order_by(Stats.last_updated.desc()).first()
    session.close()

    if results is None:
        logger.error("Error, Statistics do not exist.")
        return "Statistics do not exits.", 404

    results_to_dict = {}
    results_to_dict["num_answers"] = results.num_answers
    results_to_dict["max_randInt_answers"] = results.max_randInt_answers
    results_to_dict["num_questions"] = results.num_questions
    results_to_dict["max_randInt_questions"] = results.max_randInt_questions
    results_to_dict["last_updated"] = results.last_updated.strftime(
        "%Y-%m-%d %H:%M:%S")

    logger.debug(f'Content from DB query: {results_to_dict}')
    logger.info("Request complete.")
    print('\n')

    return results_to_dict, 200


def populate_stats():
    """periodically update stats"""
    print('\n')
    # log info message for start
    logger.info("Periodic Processing has started.")

    # read current stats in attempt to get latest stored stats
    session = DB_SESSION()
    results = session.query(Stats).order_by(Stats.last_updated.desc()).first()
    session.close()
    if results is None:
        last_updated = dt.datetime.strptime(
            "2020-01-01 12:12:12", "%Y-%m-%d %H:%M:%S")
        stats = Stats(
            # 12,
            # 12,
            # 12,
            # 12,
            num_answers=12,  # stats["num_answers"],
            max_randInt_answers=12,  # stats["max_randInt_answers"],
            num_questions=12,  # stats["num_questions"],
            max_randInt_questions=12,  # stats["max_randInt_questions"],
            last_updated=last_updated,
        )
        session.add(stats)
        session.commit()
        session.close()
        latest_stored = last_updated

    # print(results.last_updated)

    # get current datetime
    # latest_stored = results[0]["last_updated"]
    # current_datetime = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    current_datetime = dt.datetime.now()
    latest_stored = results.last_updated.strftime("%Y-%m-%d %H:%M:%S")

    # query get endpoints running in storage service
    num_answers, max_randInt_answers = request_answers(latest_stored)
    num_questions, max_randInt_questions = request_questions(latest_stored)

    # write stats to SQLite db
    if num_answers != None and num_questions != None:
        stats = Stats(
            num_answers=num_answers,
            max_randInt_answers=max_randInt_answers,
            num_questions=num_questions,
            max_randInt_questions=max_randInt_questions,
            last_updated=current_datetime,
        )
        session.add(stats)
        session.commit()
        session.close()

    # log info message for end
    logger.info("Periodic Processing has ended.")
    print('\n')


def init_scheduler():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(populate_stats, "interval",
                  seconds=app_config["scheduler"]["period_sec"])
    sched.start()


app = connexion.FlaskApp(__name__, specification_dir="")
CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    init_scheduler()
    app.run(port=8100, use_reloader=False)
