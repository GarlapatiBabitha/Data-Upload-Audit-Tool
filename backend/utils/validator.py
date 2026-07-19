def validate_data(df):

    validation = {}

    # -------------------------
    # Missing Values
    # -------------------------
    missing_values = []
    missing = df.isnull().sum()

    for column, count in missing.items():
        if count > 0:
            missing_values.append({
                "column": column,
                "missing_count": int(count)
            })

    validation["missing_values"] = missing_values

    # -------------------------
    # Duplicate Rows
    # -------------------------
    duplicates = int(df.duplicated().sum())
    validation["duplicates"] = duplicates

    # -------------------------
    # Schema Validation
    # -------------------------
    schema_errors = []

    for column in df.columns:
        if df[column].isnull().all():
            schema_errors.append(f"{column} column has no data")

    duplicate_columns = df.columns[df.columns.duplicated()].tolist()

    for column in duplicate_columns:
        schema_errors.append(f"Duplicate column: {column}")

    validation["schema_errors"] = schema_errors

    # -------------------------
    # Data Types
    # -------------------------
    datatypes = {}
    type_issues = []

    for column in df.columns:
        dtype = str(df[column].dtype)
        datatypes[column] = dtype

        # 🚨 Example check: numeric columns having strings
        if "int" in dtype or "float" in dtype:
            if df[column].astype(str).str.contains("[a-zA-Z]").any():
                type_issues.append(f"Invalid values in numeric column: {column}")

    validation["datatypes"] = datatypes
    validation["type_issues"] = type_issues

    # -------------------------
    # Consistency Check
    # -------------------------
    consistency_issues = []

    for column in df.columns:
        unique_ratio = df[column].nunique() / len(df) if len(df) > 0 else 0

        if unique_ratio < 0.01:
            consistency_issues.append(f"{column} has too many repeated values")

    validation["consistency_issues"] = consistency_issues

    # -------------------------
    # Additional Info
    # -------------------------
    additional_checks = []

    empty_rows = int(df.isnull().all(axis=1).sum())

    additional_checks.append(f"Empty rows: {empty_rows}")
    additional_checks.append(f"Total rows: {len(df)}")
    additional_checks.append(f"Total columns: {len(df.columns)}")

    validation["additional_checks"] = additional_checks

    return validation

