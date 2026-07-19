# import os
# import sqlite3

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# DB = os.path.join(BASE_DIR, "database", "db.sqlite3")

# os.makedirs(os.path.dirname(DB), exist_ok=True)


# def init_db():
#     conn = sqlite3.connect(DB)
#     cur = conn.cursor()

#     cur.execute("""
#     CREATE TABLE IF NOT EXISTS audit_logs (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         filename TEXT,
#         user TEXT,
#         score REAL,
#         status TEXT,
#         date TEXT,
#         report TEXT
#     )
#     """)

#     conn.commit()
#     conn.close()


# def insert_record(data):
#     conn = sqlite3.connect(DB)
#     cur = conn.cursor()

#     cur.execute("""
#     INSERT INTO audit_logs (filename, user, score, status, date, report)
#     VALUES (?, ?, ?, ?, ?, ?)
#     """, data)

#     conn.commit()
#     conn.close()


# def get_all_records():
#     conn = sqlite3.connect(DB)
#     cur = conn.cursor()

#     cur.execute("SELECT * FROM audit_logs")
#     rows = cur.fetchall()
#     conn.close()

#     return rows








import os
import sqlite3
import json


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


DB = os.path.join(
    BASE_DIR,
    "database",
    "db.sqlite3"
)



os.makedirs(
    os.path.dirname(DB),
    exist_ok=True
)



def init_db():

    conn = sqlite3.connect(DB)

    cur = conn.cursor()


    cur.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        filename TEXT,

        user TEXT,

        score REAL,

        status TEXT,

        date TEXT,

        report TEXT

    )
    """)


    conn.commit()

    conn.close()





def insert_record(result):


    conn = sqlite3.connect(DB)

    cur = conn.cursor()



    cur.execute("""
    INSERT INTO audit_logs
    (
        filename,
        user,
        score,
        status,
        date,
        report
    )

    VALUES (?,?,?,?,?,?)

    """,

    (

        result["metadata"]["file_name"],

        result["metadata"]["user"],

        result["score"],

        result["metadata"]["status"],

        result["metadata"]["timestamp"],

        json.dumps(result["validation"])

    ))

    conn.commit()

    conn.close()

def get_all_records():


    conn = sqlite3.connect(DB)

    cur = conn.cursor()



    cur.execute(
        """
        SELECT *
        FROM audit_logs
        ORDER BY id DESC
        """
    )


    rows = cur.fetchall()



    conn.close()



    return rows