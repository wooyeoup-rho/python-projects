import sqlite3
import textwrap

db = sqlite3.connect("books-collection.db")

cursor = db.cursor()

query = textwrap.dedent("""
    CREATE TABLE books(
        id INTEGER PRIMARY KEY,
        title varchar(250) NOT NULL UNIQUE,
        author varchar(250) NOT NULL,
        rating FLOAT NOT NULL
    )
""")

cursor.execute(query)

cursor.execute(
    textwrap.dedent("""
        INSERT INTO books VALUES(
            1, "Murder on the Orient Express", "Agatha Christie", '5'
        )
    """)
)

db.commit()