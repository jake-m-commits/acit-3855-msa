# Jake Martin - A01158619
# ACIT3855

import yaml
import connexion
# from connexion import NoContent
# import swagger_ui_bundle
import logging
import logging.config
import json
from pykafka import KafkaClient
from flask_cors import CORS, cross_origin

# load app config
with open("app_config.yml", "r") as f:
    app_config = yaml.safe_load(f.read())

# load logging config
with open("log_config.yml", "r") as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

# create logger
logger = logging.getLogger("basicLogger")


def get_answer(index):
    """ get answer event from kafka via index """
    hostname = "%s:%d" % (app_config["events"]["host"],
                          app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config["events"]["topic"])]
    consumer = topic.get_simple_consumer(reset_offset_on_start=True,
                                         consumer_timeout_ms=1000)
    logger.info("Retrieving answer at index %d" % index)
    try:
        idx = 1
        for msg in consumer:
            msg_str = msg.value.decode('utf-8')
            msg = json.loads(msg_str)
            if msg['type'] == 'answer' and idx == index:
                return msg['payload'], 200
            elif msg['type'] == 'question':
                idx -= 1
            idx += 1
    except:
        logger.error("No more messages found")
    logger.error("Could not find answer at index %d" % index)
    return { "message": "Not Found"}, 404


def get_question(index):
    """ get quetion event from kafka via index """
    hostname = "%s:%d" % (app_config["events"]["host"],
                          app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config["events"]["topic"])]
    consumer = topic.get_simple_consumer(reset_offset_on_start=True,
                                         consumer_timeout_ms=1000)
    logger.info("Retrieving question at index %d" % index)
    try:
        idx = 1
        for msg in consumer:
            msg_str = msg.value.decode('utf-8')
            msg = json.loads(msg_str)
            if msg['type'] == 'question' and idx == index:
                return msg['payload'], 200
            elif msg['type'] == 'answer':
                idx -= 1
            idx += 1
    except:
        logger.error("No more messages found")
    logger.error("Could not find question at index %d" % index)
    return { "message": "Not Found"}, 404


app = connexion.FlaskApp(__name__, specification_dir="")
CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    app.run(port=8088, debug=True)

