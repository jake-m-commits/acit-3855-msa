# Jake Martin - A01158619
# ACIT3855

import yaml
import uuid
import connexion
from connexion import NoContent
import logging
import logging.config
import json
import datetime
from pykafka import KafkaClient

HEADERS = {"content-type": "application/json"}

# load app config
with open("app_config.yml", "r") as f:
    app_config = yaml.safe_load(f.read())

# load logging config
with open("log_config.yml", "r") as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

# create logger
logger = logging.getLogger("basicLogger")


def add_answers(body):
    """Receives answer event"""

    trace = str(uuid.uuid4())
    body["trace_id"] = trace

    # req = requests.post(
    #     app_config["eventstore_answer"]["url"], json=body, headers=HEADERS)
    client = KafkaClient(hosts=f"{app_config['events']['host']}:{app_config['events']['port']}")
    topic = client.topics[str.encode(app_config['events']['topic'])]
    producer = topic.get_sync_producer()
    msg = { "type": "answer",
            "datetime" : datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "payload": body }
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))

    logger.info(
        f"Returned event add_answers response (Id: {trace}) with status 201"
    )

    return NoContent, 201


def add_questions(body):
    """Receives question event"""

    trace = str(uuid.uuid4())
    body["trace_id"] = trace

    # req = requests.post(
    #     app_config["eventstore_question"]["url"], json=body, headers=HEADERS)
    client = KafkaClient(hosts=f"{app_config['events']['host']}:{app_config['events']['port']}")
    topic = client.topics[str.encode(app_config['events']['topic'])]
    producer = topic.get_sync_producer()
    msg = { "type": "question",
            "datetime" : datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "payload": body }
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))

    logger.info(
        f"Returned event add_questions response (Id: {trace}) with status 201"
    )

    return NoContent, 201


app = connexion.FlaskApp(__name__, specification_dir="")
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    app.run(port=8080, debug=True)
