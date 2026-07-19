# import pandas as pd


# import pandas as pd


# def load_file(file_path):

#     if file_path.endswith(".csv"):

#         df = pd.read_csv(file_path)

#     elif file_path.endswith(".xlsx"):

#         df = pd.read_excel(file_path)

#     else:

#         raise ValueError(
#             "Unsupported file format. Upload CSV or Excel file."
#         )


#     return df




import pandas as pd

def load_file(file_path):

    try:
        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path)

        elif file_path.endswith(".xlsx"):
            df = pd.read_excel(file_path)

        else:
            return None, "Unsupported file format"

    except Exception:
        return None, "File is corrupted or unreadable"

    # Empty file check
    if df.shape[0] == 0 and df.shape[1] == 0:
        return df, "File is empty"

    return df, None