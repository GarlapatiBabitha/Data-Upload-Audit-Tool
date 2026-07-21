
# import streamlit as st
# import requests

# st.set_page_config(
#     page_title="Data Audit Tool",
#     page_icon="📤",
#     layout="wide"
# )

# st.markdown(
#     """
#     <style>
#     .stApp {
#         background-color:#15151D;
#     }
#     header[data-testid="stHeader"] {
#         background-color:#15151D !important;
#     }
#     div[data-testid="stToolbar"] {
#         background-color:#15151D !important;
#     }
#     div[data-testid="stToolbar"] button {
#         background-color:#15151D !important;
#         color:white !important;
#     }
#     section[data-testid="stSidebar"] {
#         background-color:#15151D !important;
#     }
#     section[data-testid="stSidebar"] * {
#         color:white !important;
#     }
#     h1,h2,h3,h4,h5,h6,p,span,label {
#         color:white !important;
#     }
#     div[data-testid="stTextInput"] input {
#         background-color:#1F2937;
#         color:white;
#         border-radius:10px;
#         border:1px solid #374151;
#     }
#     section[data-testid="stFileUploader"] {
#         background-color:#1F2937;
#         border-radius:15px;
#         padding:20px;
#         border:1px solid #374151;
#     }
#     div.stButton > button {
#         width:100%;
#         background:#2563EB;
#         color:white;
#         border-radius:10px;
#         border:none;
#         padding:10px;
#         font-weight:bold;
#     }
#     div.stButton > button:hover {
#         background:#1D4ED8;
#         color:white;
#     }
#     div[data-testid="metric-container"] {
#         background:#1F2937;
#         padding:15px;
#         border-radius:12px;
#         border:1px solid #374151;
#     }
#     div[data-testid="stDataFrame"] {
#         background:#1F2937;
#     }
#     .block-container {
#         padding-top:2rem;
#     }

#     /* -------- NEW CARD UI -------- */
#     .card {
#         background: #1F2937;
#         padding: 20px;
#         border-radius: 16px;
#         border: 1px solid #374151;
#         text-align: center;
#         box-shadow: 0px 4px 20px rgba(0,0,0,0.4);
#     }
#     .card-title {
#         color: #9CA3AF;
#         font-size: 14px;
#         margin-bottom: 8px;
#     }
#     .card-value {
#         color: white;
#         font-size: 20px;
#         font-weight: bold;
#     }

#     /* -------- TABLE STYLE -------- */
#     [data-testid="stDataFrame"] {
#         border: 1px solid #374151;
#         border-radius: 10px;
#         overflow: hidden;
#     }
#     thead tr th {
#         background-color: #111827 !important;
#         color: white !important;
#         font-weight: bold;
#     }
#     tbody tr {
#         background-color: #1F2937 !important;
#         color: white !important;
#     }
#     tbody tr:hover {
#         background-color: #374151 !important;
#     }

#     </style>
#     """,
#     unsafe_allow_html=True
# )

# st.markdown("""
# <style>
# div[data-testid="stFileUploader"] p {
#     color: black !important;
#     font-weight: 500;
# }
# div[data-testid="stFileUploader"] span {
#     color: black !important;
#     font-weight: bold;
# }
# div[data-testid="stFileUploader"] small {
#     color: black !important;
# }
# </style>
# """, unsafe_allow_html=True)

# st.markdown(
#     "<h1 style='text-align:center;'>📤 Data Upload Audit Tool</h1>",
#     unsafe_allow_html=True
# )

# st.divider()

# col1, col2, col3 = st.columns([1,2,1])

# with col2:
#     username = st.text_input(
#         "👤 Enter Username",
#         placeholder="Enter your username"
#     )

#     uploaded_file = st.file_uploader(
#         "Upload CSV / Excel file",
#         type=["csv", "xlsx"]
#     )

#     run_btn = st.button("🚀 Run Audit")

# # CARD FUNCTION
# def card(title, value):
#     return f"""
#     <div class="card">
#         <div class="card-title">{title}</div>
#         <div class="card-value">{value}</div>
#     </div>
#     """

# if uploaded_file and run_btn:

#     if username.strip() == "":
#         st.warning("Please enter username before running audit")
#         st.stop()

#     files = {
#         "file": (
#             uploaded_file.name,
#             uploaded_file.getvalue()
#         )
#     }
#     data = {
#         "user": username.strip()
#     }

#     try:
#         response = requests.post(
#             "http://127.0.0.1:5000/upload",
#             files=files,
#             data=data,
#             timeout=30
#         )

#         result = response.json()

#     except requests.exceptions.ConnectionError:
#         st.error("Backend server is not running")
#         st.stop()

#     except Exception as e:
#         st.error(str(e))
#         st.stop()

#     if "error" in result:
#         st.error(result["error"])

#     else:
#         st.success("✅ Audit Completed Successfully")

#         st.divider()

#         st.header("📄 File Metadata")

#         metadata = result["metadata"]

#         c1, c2, c3, c4 = st.columns(4)

#         c1.markdown(card("File Name", metadata["file_name"]), unsafe_allow_html=True)
#         c2.markdown(card("File Size", metadata["file_size"]), unsafe_allow_html=True)
#         c3.markdown(card("Uploaded By", metadata["user"]), unsafe_allow_html=True)
#         c4.markdown(card("Status", metadata["status"]), unsafe_allow_html=True)

#         st.markdown(
#             f"<p style='color:#9CA3AF;'>🕒 Upload Time: {metadata['timestamp']}</p>",
#             unsafe_allow_html=True
#         )

#         st.divider()

#         st.header("📊 Dataset Summary")

#         summary = result["summary"]

#         a, b, c, d = st.columns(4)

#         a.markdown(card("Total Rows", summary["rows"]), unsafe_allow_html=True)
#         b.markdown(card("Total Columns", summary["columns"]), unsafe_allow_html=True)
#         c.markdown(card("Duplicate Rows", summary["duplicates"]), unsafe_allow_html=True)
#         d.markdown(card("Quality Score", f"{result['score']}%"), unsafe_allow_html=True)

#         st.divider()

#         st.header("🔍 Validation Report")

#         validation = result["validation"]

#         st.subheader("Missing Values")
#         if validation["missing_values"]:
#             st.dataframe(validation["missing_values"], use_container_width=True)
#         else:
#             st.success("✅ No missing values detected")

#         st.subheader("Schema Validation")
#         if validation["schema_errors"]:
#             for error in validation["schema_errors"]:
#                 st.error(error)
#         else:
#             st.success("✅ Schema is correct")

#         st.subheader("Additional Checks")
#         if validation["additional_checks"]:
#             for item in validation["additional_checks"]:
#                 st.write("✅", item)
#         else:
#             st.info("No additional issues found")

#         st.subheader("Column Data Types")
#         st.dataframe(validation["datatypes"], use_container_width=True)







import streamlit as st
import requests
import pandas as pd   # ✅ needed for datatypes fix

st.set_page_config(
    page_title="Data Audit Tool",
    page_icon="📤",
    layout="wide"
)

st.markdown(
    """
    <style>
    .stApp { background-color:#15151D; }

    header[data-testid="stHeader"],
    div[data-testid="stToolbar"] {
        background-color:#15151D !important;
    }

    div[data-testid="stToolbar"] button {
        background-color:#15151D !important;
        color:white !important;
    }

    section[data-testid="stSidebar"] {
        background-color:#15151D !important;
    }

    section[data-testid="stSidebar"] * {
        color:white !important;
    }

    h1,h2,h3,h4,h5,h6,p,span,label {
        color:white !important;
    }

    div[data-testid="stTextInput"] input {
        background-color:#1F2937;
        color:white;
        border-radius:10px;
        border:1px solid #374151;
    }

    section[data-testid="stFileUploader"] {
        background-color:#1F2937;
        border-radius:15px;
        padding:20px;
        border:1px solid #374151;
    }

    div.stButton > button {
        width:100%;
        background:#2563EB;
        color:white;
        border-radius:10px;
        border:none;
        padding:10px;
        font-weight:bold;
    }

    div.stButton > button:hover {
        background:#1D4ED8;
    }

    .block-container {
        padding-top:2rem;
    }

    /* CARD UI */
    .card {
        background: #1F2937;
        padding: 20px;
        border-radius: 16px;
        border: 1px solid #374151;
        text-align: center;
        box-shadow: 0px 4px 20px rgba(0,0,0,0.4);
    }

    .card-title {
        color: #9CA3AF;
        font-size: 14px;
        margin-bottom: 8px;
    }

    .card-value {
        color: white;
        font-size: 20px;
        font-weight: bold;
    }

    /* TABLE UI */
    table {
        width: 100%;
        border-collapse: collapse;
        background-color: #1F2937;
        border-radius: 10px;
        overflow: hidden;

        /* ✅ ALIGNMENT FIX */
        table-layout: fixed;
    }

    th {
        background-color: #111827;
        color: white;
        padding: 10px;
        text-align: left;
        border-bottom: 1px solid #374151;

        /* ✅ ALIGNMENT FIX */
        padding-left: 10px !important;
    }

    td {
        color: white;
        padding: 10px;
        border-bottom: 1px solid #374151;

        /* ✅ ALIGNMENT FIX */
        padding-left: 10px !important;
    }

    tr:hover {
        background-color: #374151;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# Fix uploader text visibility
st.markdown("""
<style>
div[data-testid="stFileUploader"] p,
div[data-testid="stFileUploader"] span,
div[data-testid="stFileUploader"] small {
    color: black !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    "<h1 style='text-align:center;'>📤 Data Upload Audit Tool</h1>",
    unsafe_allow_html=True
)

st.divider()

col1, col2, col3 = st.columns([1,2,1])

with col2:
    username = st.text_input("👤 Enter Username", placeholder="Enter your username")

    uploaded_file = st.file_uploader(
        "Upload CSV / Excel file",
        type=["csv", "xlsx"]
    )

    run_btn = st.button("🚀 Run Audit")

# CARD FUNCTION
def card(title, value):
    return f"""
    <div class="card">
        <div class="card-title">{title}</div>
        <div class="card-value">{value}</div>
    </div>
    """

if uploaded_file and run_btn:

    if username.strip() == "":
        st.warning("Please enter username before running audit")
        st.stop()

    files = {
        "file": (uploaded_file.name, uploaded_file.getvalue())
    }

    data = {
        "user": username.strip()
    }

    try:
        response = requests.post(
            "http://127.0.0.1:5000/upload",
            files=files,
            data=data,
            timeout=30
        )
        result = response.json()

    except requests.exceptions.ConnectionError:
        st.error("Backend server is not running")
        st.stop()

    except Exception as e:
        st.error(str(e))
        st.stop()

    if "error" in result:
        st.error(result["error"])

    else:
        st.success("✅ Audit Completed Successfully")

        st.divider()

        # ---------- METADATA ----------
        st.header("📄 File Metadata")

        metadata = result["metadata"]

        c1, c2, c3, c4 = st.columns(4)

        c1.markdown(card("File Name", metadata["file_name"]), unsafe_allow_html=True)
        c2.markdown(card("File Size", metadata["file_size"]), unsafe_allow_html=True)
        c3.markdown(card("Uploaded By", metadata["user"]), unsafe_allow_html=True)
        c4.markdown(card("Status", metadata["status"]), unsafe_allow_html=True)

        st.markdown(
            f"<p style='color:#9CA3AF;'>🕒 Upload Time: {metadata['timestamp']}</p>",
            unsafe_allow_html=True
        )

        st.divider()

        # ---------- SUMMARY ----------
        st.header("📊 Dataset Summary")

        summary = result["summary"]

        a, b, c, d = st.columns(4)

        a.markdown(card("Total Rows", summary["rows"]), unsafe_allow_html=True)
        b.markdown(card("Total Columns", summary["columns"]), unsafe_allow_html=True)
        c.markdown(card("Duplicate Rows", summary["duplicates"]), unsafe_allow_html=True)
        d.markdown(card("Quality Score", f"{result['score']}%"), unsafe_allow_html=True)

        st.divider()

        # ---------- VALIDATION ----------
        st.header("🔍 Validation Report")

        validation = result["validation"]

        # Missing values
        st.subheader("Missing Values")
        if validation["missing_values"]:
            df_missing = pd.DataFrame(validation["missing_values"])
            st.markdown(df_missing.to_html(index=False), unsafe_allow_html=True)
        else:
            st.success("✅ No missing values detected")

        # Schema
        st.subheader("Schema Validation")
        if validation["schema_errors"]:
            for error in validation["schema_errors"]:
                st.error(error)
        else:
            st.success("✅ Schema is correct")

        # Additional checks
        st.subheader("Additional Checks")
        if validation["additional_checks"]:
            for item in validation["additional_checks"]:
                st.write("✅", item)
        else:
            st.info("No additional issues found")

        # Datatypes (FINAL FIXED)
        st.subheader("Column Data Types")

        dt_df = pd.DataFrame(
            list(validation["datatypes"].items()),
            columns=["Column", "Data Type"]
        )

        st.markdown(
            dt_df.to_html(index=False, border=0),  # ✅ alignment fix
            unsafe_allow_html=True
        )