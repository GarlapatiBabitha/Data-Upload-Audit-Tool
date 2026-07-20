from flask import Flask, request, jsonify
import os
import json

from services.audit_service import audit_file
from services.db_service import (
    init_db,
    insert_record,
    get_all_records
)
app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

# Create database

init_db()
@app.route(
    "/upload",
    methods=["POST"]
)

def upload_file():

    try:
        file = request.files["file"]
        user = request.form.get(
            "user",
            "unknown"
        )
        file_path = os.path.join(
            UPLOAD_FOLDER,
            file.filename
        )
        file.save(
            file_path
        )
        size = round(
            os.path.getsize(file_path)
            /
            1024,
            2
        )
        result = audit_file(
            file_path,
            file.filename,
            f"{size} KB",
            user
        )
        # save history
        insert_record(
            result
        )
        return jsonify(
            result
        )
    except Exception as e:
        return jsonify(
            {
                "error":str(e)
            }
        )

@app.route(
    "/history",
    methods=["GET"]
)
def history():
    records = get_all_records()
    result = []
    for row in records:
        try:

            validation = json.loads(
                row[6]
            ) if row[6] else {}
        except json.JSONDecodeError:
            validation = {}
        result.append({
            "id": row[0],
            "filename": row[1],
            "user": row[2],
            "score": row[3],
            "status": row[4],
            "date": row[5],
            "validation": validation
        })
    return jsonify(result)
if __name__=="__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )