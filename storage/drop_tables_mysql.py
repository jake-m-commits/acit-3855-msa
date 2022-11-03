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
        DROP TABLE questions, answers
        """
)

db_conn.commit()
db_conn.close()
