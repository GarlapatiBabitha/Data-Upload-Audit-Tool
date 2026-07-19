import streamlit as st
import requests
st.set_page_config(
    page_title="Data Audit Tool",
    page_icon="📤",
    layout="wide"
)

st.markdown(
    """
    <style>
    /* MAIN BACKGROUND */
    .stApp {
        background-color:#15151D;
    }
    /* HEADER / TOP BAR */
    header[data-testid="stHeader"] {
        background-color:#15151D !important;
    }
    div[data-testid="stToolbar"] {
        background-color:#15151D !important;
    }
    div[data-testid="stToolbar"] button {
        background-color:#15151D !important;
        color:white !important;
    }
    /* SIDEBAR */
    section[data-testid="stSidebar"] {
        background-color:#15151D !important;
    }
    section[data-testid="stSidebar"] * {
        color:white !important;
    }
    /* TEXT */
    h1,h2,h3,h4,h5,h6,p,span,label {
        color:white !important;
    }
    /* INPUT BOX */
    div[data-testid="stTextInput"] input {
        background-color:#1F2937;
        color:white;
        border-radius:10px;
        border:1px solid #374151;
    }

    /* FILE UPLOADER */
    section[data-testid="stFileUploader"] {
        background-color:#1F2937;
        border-radius:15px;
        padding:20px;
        border:1px solid #374151;
    }

    /* BUTTON */
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
        color:white;
    }

    /* METRIC CARDS */
    div[data-testid="metric-container"] {
        background:#1F2937;
        padding:15px;
        border-radius:12px;
        border:1px solid #374151;
    }

    /* DATAFRAME */
    div[data-testid="stDataFrame"] {
        background:#1F2937;
    }

    /* REMOVE TOP SPACE */
    .block-container {
        padding-top:2rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("""
<style>

/* Make uploader instruction text visible */
div[data-testid="stFileUploader"] p {
    color: black !important;   /* 👈 THIS fixes your issue */
    font-weight: 500;
}

/* Make "Browse files" text visible */
div[data-testid="stFileUploader"] span {
    color: black !important;
    font-weight: bold;
}

/* Optional: Fix small icon/text contrast */
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

    username = st.text_input(
        "👤 Enter Username",
        placeholder="Enter your username"
    )

    uploaded_file = st.file_uploader(
        "Upload CSV / Excel file",
        type=["csv", "xlsx"]
    )

    run_btn = st.button("🚀 Run Audit")

if uploaded_file and run_btn:

    if username.strip() == "":
        st.warning("Please enter username before running audit")
        st.stop()

    files = {
        "file": (
            uploaded_file.name,
            uploaded_file.getvalue()
        )
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

        st.header("📄 File Metadata")

        metadata = result["metadata"]

        c1,c2,c3,c4 = st.columns(4)

        c1.metric("File Name", metadata["file_name"])
        c2.metric("File Size", metadata["file_size"])
        c3.metric("Uploaded By", metadata["user"])
        c4.metric("Status", metadata["status"])

        st.write("🕒 Upload Time:", metadata["timestamp"])

        st.divider()

        st.header("📊 Dataset Summary")

        summary = result["summary"]

        a,b,c,d = st.columns(4)

        a.metric("Total Rows", summary["rows"])
        b.metric("Total Columns", summary["columns"])
        c.metric("Duplicate Rows", summary["duplicates"])
        d.metric("Quality Score", f"{result['score']}%")

        st.divider()
        st.header("🔍 Validation Report")

        validation = result["validation"]

        # Missing Values
        st.subheader("Missing Values")

        if validation["missing_values"]:
            st.dataframe(validation["missing_values"], use_container_width=True)
        else:
            st.success("✅ No missing values detected")

        # Schema
        st.subheader("Schema Validation")

        if validation["schema_errors"]:
            for error in validation["schema_errors"]:
                st.error(error)
        else:
            st.success("✅ Schema is correct")

        # Additional Checks
        st.subheader("Additional Checks")

        if validation["additional_checks"]:
            for item in validation["additional_checks"]:
                st.write("✅", item)
        else:
            st.info("No additional issues found")

        # Data Types
        st.subheader("Column Data Types")

        st.dataframe(validation["datatypes"], use_container_width=True)