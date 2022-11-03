import sqlite3

conn = sqlite3.connect("stats.sqlite")
c = conn.cursor()
c.execute(
    """
CREATE TABLE stats
(id INTEGER PRIMARY KEY ASC,
num_answers INTEGER NOT NULL,
max_randInt_answers INTEGER,
num_questions INTEGER NOT NULL,
max_randInt_questions INTEGER,
last_updated VARCHAR(100) NOT NULL)
"""
)
conn.commit()
conn.close()
