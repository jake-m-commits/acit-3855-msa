import mysql.connector
import yaml

# load app config
with open("app_config.yml", "r") as f:
    app_config = yaml.safe_load(f.read())

DB_USER = app_config["datastore"]["user"]
DB_PASS = app_config["datastore"]["password"]
DB_HOST = app_config["datastore"]["hostname"]
DB_PORT = app_config["datastore"]["port"]
DB_DB = app_config["datastore"]["db"]

db_conn = mysql.connector.connect(
    host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_DB
)
db_cursor = db_conn.cursor()

db_cursor.execute(
    """
          CREATE TABLE questions
          (id INT NOT NULL AUTO_INCREMENT,
           question_id INTEGER NOT NULL,
           description VARCHAR(250) NOT NULL,
           question VARCHAR(250) NOT NULL,
           randomInt INTEGER NOT NULL,
           trace_id VARCHAR(100) NOT NULL UNIQUE,
           date_created VARCHAR(100) NOT NULL,
           CONSTRAINT questions_pk PRIMARY KEY (id))
          """
)

db_cursor.execute(
    """
          CREATE TABLE answers
          (id INT NOT NULL AUTO_INCREMENT,
           answer_id INTEGER NOT NULL,
           description VARCHAR(250) NOT NULL,
           answer VARCHAR(250) NOT NULL,
           randomInt INTEGER NOT NULL,
           trace_id VARCHAR(100) NOT NULL UNIQUE,
           date_created VARCHAR(100) NOT NULL,
           CONSTRAINT answers_pk PRIMARY KEY (id))
          """
)

db_conn.commit()
db_conn.close()
