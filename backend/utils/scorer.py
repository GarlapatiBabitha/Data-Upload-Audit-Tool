
def calculate_score(df, validation):

    score = 100

    total_cells = df.shape[0] * df.shape[1]

    if total_cells == 0:
        return 0

    missing_count = sum(
        item["missing_count"]
        for item in validation["missing_values"]
    )
    score -= (missing_count / total_cells) * 70
    duplicate_rows = validation["duplicates"]

    if len(df) > 0:
        score -= (duplicate_rows / len(df)) * 20

    score -= len(validation["schema_errors"]) * 5
    score -= len(validation["type_issues"]) * 5
    score -= len(validation["consistency_issues"]) * 2

    return max(0, round(score, 2))

