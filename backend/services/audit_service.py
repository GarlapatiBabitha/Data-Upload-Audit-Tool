import os
from datetime import datetime

from utils.file_loader import load_file
from utils.validator import validate_data
from utils.scorer import calculate_score

def audit_file(file_path, file_name, file_size, user):

    df, file_error = load_file(file_path)

    # 🚨 FILE LEVEL FAILURE
    if file_error:

        metadata = {
            "file_name": file_name,
            "file_size": file_size,
            "user": user,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "Failed"
        }

        summary = {
            "rows": 0 if df is None else int(df.shape[0]),
            "columns": 0 if df is None else int(df.shape[1]),
            "duplicates": 0
        }

        validation = {
            "missing_values": [],
            "duplicates": 0,
            "schema_errors": [file_error],
            "type_issues": [],
            "consistency_issues": [],
            "additional_checks": ["File validation failed"],
            "datatypes": {}
        }

        return {
            "metadata": metadata,
            "summary": summary,
            "score": 0,
            "validation": validation
        }

    # ✅ NORMAL FLOW
    validation = validate_data(df)
    score = calculate_score(df, validation)

    # STATUS LOGIC
    if score >= 90:
        status = "Success"
    elif score >= 75:
        status = "Warning"
    else:
        status = "Failed"

    metadata = {
        "file_name": file_name,
        "file_size": file_size,
        "user": user,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": status
    }

    summary = {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "duplicates": validation["duplicates"]
    }

    return {
        "metadata": metadata,
        "summary": summary,
        "score": score,
        "validation": validation
    }

