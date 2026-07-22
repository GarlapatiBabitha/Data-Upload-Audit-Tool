
from datetime import datetime

from utils.file_loader import load_file
from utils.validator import validate_data
from utils.scorer import calculate_score


def audit_file(file_path, file_name, file_size, user):

    df, file_error = load_file(file_path)
    
    # File Loading Failed
    if file_error:
        metadata = {
            "file_name": file_name,
            "file_size": file_size,
            "user": user,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "Failed"
        }
        summary = {
            "rows": 0,
            "columns": 0,
            "duplicates": 0,
            "missing_values": 0,
            "missing_percentage": 0,
            "duplicate_percentage": 0,
            "memory_usage_mb": 0
        }
        validation = {
            "missing_values": [],
            "duplicates": 0,
            "schema_errors": [file_error],
            "type_issues": [],
            "consistency_issues": [],
            "constant_columns": [],
            "blank_strings": [],
            "whitespace_columns": [],
            "mixed_type_columns": [],
            "outliers": [],
            "empty_rows": 0,
            "additional_checks": ["File validation failed"],
            "datatypes": {},
            "summary": {}
        }
        return {
            "metadata": metadata,
            "summary": summary,
            "score": 0,
            "validation": validation
        }
    
    # Run Validation
    validation = validate_data(df)
    score = calculate_score(df, validation)
    status = "Success" if score >= 80 else "Failed"
 
    # Metadata
    metadata = {
        "file_name": file_name,
        "file_size": file_size,
        "user": user,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": status
    }

    # Summary
    summary = {
        "rows": validation["summary"]["rows"],
        "columns": validation["summary"]["columns"],
        "duplicates": validation["duplicates"],
        "duplicate_percentage": validation["summary"]["duplicate_percentage"],
        "missing_values": validation["summary"]["total_missing"],
        "missing_percentage": validation["summary"]["missing_percentage"],
        "memory_usage_mb": validation["summary"]["memory_mb"],
        "empty_rows": validation["empty_rows"],
        "constant_columns": len(validation["constant_columns"]),
        "mixed_datatype_columns": len(validation["mixed_type_columns"]),
        "blank_string_columns": len(validation["blank_strings"]),
        "whitespace_columns": len(validation["whitespace_columns"]),
        "outlier_columns": len(validation["outliers"]),
        "schema_errors": len(validation["schema_errors"]),
        "datatype_issues": len(validation["type_issues"]),
        "consistency_issues": len(validation["consistency_issues"])
    }
    return {

        "metadata": metadata,
        "summary": summary,
        "score": score,
        "validation": validation
    }