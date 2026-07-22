
def calculate_score(df, validation):

    score = 100

    summary = validation["summary"]

    # Missing Values (Overall)
    missing_pct = summary["missing_percentage"]

    if missing_pct >= 50:
        score -= 40
    elif missing_pct >= 40:
        score -= 35
    elif missing_pct >= 30:
        score -= 30
    elif missing_pct >= 20:
        score -= 20
    elif missing_pct >= 10:
        score -= 10
    elif missing_pct >= 5:
        score -= 5

    # Duplicate Rows
    duplicate_pct = summary["duplicate_percentage"]

    if duplicate_pct >= 20:
        score -= 20
    elif duplicate_pct >= 10:
        score -= 15
    elif duplicate_pct >= 5:
        score -= 10
    elif duplicate_pct >= 2:
        score -= 5
    elif duplicate_pct >= 1:
        score -= 2

    # Empty Columns
    empty_columns = 0

    for error in validation["schema_errors"]:

        if "has no data" in error:
            empty_columns += 1

    score -= empty_columns * 8


    # Duplicate Column Names

    duplicate_columns = 0

    for error in validation["schema_errors"]:

        if "Duplicate column" in error:
            duplicate_columns += 1

    score -= duplicate_columns * 5

    # Datatype Issues
    score -= len(validation["type_issues"]) * 5

    
    # Consistency Issues
    score -= len(validation["consistency_issues"]) * 2

   
    # Constant Columns
    score -= len(validation["constant_columns"]) * 3

    # Blank Strings
    blank_penalty = 0

    for item in validation["blank_strings"]:

        if item["count"] > 0:
            blank_penalty += 1

    score -= blank_penalty

    # Whitespace Issues
    score -= len(validation["whitespace_columns"])

    # Mixed Datatype Columns
    score -= len(validation["mixed_type_columns"]) * 4
    
    
    # Outliers
    if len(validation["outliers"]) > 0:

        penalty = min(
            len(validation["outliers"]) * 2,
            10
        )

        score -= penalty

    # Empty Rows
    rows = summary["rows"]

    if rows > 0:

        empty_pct = (
            validation["empty_rows"] / rows
        ) * 100

        if empty_pct >= 20:
            score -= 15
        elif empty_pct >= 10:
            score -= 10
        elif empty_pct >= 5:
            score -= 5

    # Clamp Score
    if score < 0:
        score = 0

    if score > 100:
        score = 100

    return round(score, 2)