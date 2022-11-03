import sqlite3

conn = sqlite3.connect("readings.sqlite")

c = conn.cursor()
c.execute(
    """
          CREATE TABLE questions
          (id INTEGER PRIMARY KEY ASC, 
           question_id INTEGER NOT NULL,
           description VARCHAR(250) NOT NULL,
           question VARCHAR(250) NOT NULL,
           randomInt INTEGER NOT NULL,
           trace_id VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL)
          """
)

c.execute(
    """
          CREATE TABLE answers
          (id INTEGER PRIMARY KEY ASC, 
           answer_id INTEGER NOT NULL,
           description VARCHAR(250) NOT NULL,
           answer VARCHAR(250) NOT NULL,
           randomInt INTEGER NOT NULL,
           trace_id VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL)
          """
)

conn.commit()
conn.close()
