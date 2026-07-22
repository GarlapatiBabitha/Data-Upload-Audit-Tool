
import pandas as pd

def validate_data(df):

    validation = {}
    # Missing Values
    missing_values = []
    missing = df.isnull().sum()

    for column, count in missing.items():
        if count > 0:
            missing_values.append({
                "column": column,
                "missing_count": int(count)
            })
    validation["missing_values"] = missing_values
    
    # Duplicate Rows
    validation["duplicates"] = int(df.duplicated().sum())
    
    # Schema Errors
    schema_errors = []
    for column in df.columns:
        if df[column].isnull().all():
            schema_errors.append(
                f"{column} column has no data"
            )
    duplicate_columns = df.columns[
        df.columns.duplicated()
    ].tolist()
    for column in duplicate_columns:
        schema_errors.append(
            f"Duplicate column: {column}"
        )
    validation["schema_errors"] = schema_errors
   
    # Datatype Validation
    datatypes = {}
    type_issues = []
    for column in df.columns:
        dtype = str(df[column].dtype)
        datatypes[column] = dtype
        if "int" in dtype or "float" in dtype:
            if (
                df[column]
                .astype(str)
                .str.contains("[a-zA-Z]", regex=True)
                .any()
            ):
                type_issues.append(
                    f"Invalid values in numeric column: {column}"
                )
    validation["datatypes"] = datatypes
    validation["type_issues"] = type_issues


    # Consistency Check
    consistency_issues = []
    for column in df.columns:
        unique_ratio = (
            df[column].nunique(dropna=True) / len(df)
            if len(df) > 0 else 0
        )
        if unique_ratio < 0.01:
            consistency_issues.append(
                f"{column} has too many repeated values"
            )
    validation["consistency_issues"] = consistency_issues
    
    # Empty Rows
    empty_rows = int(df.isnull().all(axis=1).sum())
    validation["empty_rows"] = empty_rows
    
    # Constant Columns
    constant_columns = []
    for column in df.columns:
        if df[column].nunique(dropna=False) == 1:
            constant_columns.append(column)
    validation["constant_columns"] = constant_columns

    # Blank Strings
    blank_strings = []
    for column in df.select_dtypes(include="object"):
        blank_count = (
            df[column]
            .fillna("")
            .astype(str)
            .str.strip()
            .eq("")
            .sum()
        )
        if blank_count > 0:
            blank_strings.append({
                "column": column,
                "count": int(blank_count)
            })
    validation["blank_strings"] = blank_strings
    
    # Leading / Trailing Spaces
    whitespace_columns = []
    for column in df.select_dtypes(include="object"):

        has_space = (
            df[column]
            .fillna("")
            .astype(str)
            .str.match(r"^\s+|\s+$")
            .any()
        )
        if has_space:

            whitespace_columns.append(column)
    validation["whitespace_columns"] = whitespace_columns
    
    # Mixed Datatypes
    mixed_type_columns = []
    for column in df.columns:
        detected = (
            df[column]
            .dropna()
            .map(type)
            .nunique()
        )
        if detected > 1:

            mixed_type_columns.append(column)
    validation["mixed_type_columns"] = mixed_type_columns

    # Outlier Detection
    outliers = []
    numeric = df.select_dtypes(include="number")
    for column in numeric.columns:
        q1 = numeric[column].quantile(0.25)
        q3 = numeric[column].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        count = int(
            (
                (numeric[column] < lower) |
                (numeric[column] > upper)
            ).sum()
        )
        if count > 0:
            outliers.append({
                "column": column,
                "count": count
            })
    validation["outliers"] = outliers
    
    # Dataset Summary
    total_missing = int(df.isnull().sum().sum())
    total_cells = len(df) * len(df.columns)
    validation["summary"] = {
        "rows": len(df),
        "columns": len(df.columns),
        "memory_mb": round(
            df.memory_usage(deep=True).sum() /
            (1024 * 1024),
            2
        ),
        "total_missing": total_missing,
        "missing_percentage": round(
            (total_missing / total_cells) * 100,
            2
        ) if total_cells else 0,
        "duplicate_percentage": round(
            (validation["duplicates"] / len(df)) * 100,
            2
        ) if len(df) else 0
    }
    
    # Additional Checks
    validation["additional_checks"] = [
        f"Empty rows : {empty_rows}",
        f"Total rows : {len(df)}",
        f"Total columns : {len(df.columns)}",
        f"Memory Usage : {validation['summary']['memory_mb']} MB",
        f"Missing % : {validation['summary']['missing_percentage']}%",
        f"Duplicate % : {validation['summary']['duplicate_percentage']}%"
    ]
    return validation