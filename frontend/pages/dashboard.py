import streamlit as st
import requests
import pandas as pd

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)

st.markdown(
    """
    <style>
    .stApp {
        background-color:#15151D;
    }
    header[data-testid="stHeader"] {

        background-color:#15151D !important;
    }
    header[data-testid="stHeader"] > div {
        background-color:#15151D !important;
    }

    div[data-testid="stToolbar"] {
        background-color:#15151D !important;
    }

    div[data-testid="stToolbar"] button {
        background-color:#15151D !important;
        color:white !important;
    }

    button[kind="header"] {
        background-color:#15151D !important;
        color:white !important;
    }

    section[data-testid="stSidebar"] {
        background-color:#15151D !important;
    }
    section[data-testid="stSidebar"] > div {
        background-color:#15151D !important;
    }

    section[data-testid="stSidebar"] * {
        color:white !important;
    }

    h1,h2,h3,h4,h5,h6,p,span,label {
        color:white !important;
    }

    .block-container {
        padding-top:2rem;
    }

    .summary-card {
        padding:15px;
        border-radius:15px;
        color:white;
        height:120px;
        margin-bottom:20px;
        text-align:center;
    }
    .summary-card h4 {
        margin-top:-10px;
        margin-bottom:5px;
        font-size:25px;
    }
    .summary-card h1 {
        margin-top:0px;
        margin-bottom:0px;
        font-size:38px;
        line-height:1;

    }
    .total-card {
        background:#2563EB;
    }
    .success-card {
        background:#16A34A;
    }
    .failed-card {
        background:#DC2626;
    }
   .score-card {
        background:#9333EA;
    }

    .file-card {
        background:#1F2937;
        padding:25px;
        border-radius:18px;
        border:1px solid #374151;
        min-height:250px;
    }
   .file-title {
        font-size:22px;
        color:white;
    }
    .small-text {
        color:#D1D5DB;
        font-size:15px;
    }
    div.stButton > button {
        width:100%;
        border-radius:10px;
        background:#374151;
        color:white;
        border:none;
    }
    div.stButton > button:hover {
        background:#4B5563;
        color:white;
    }

    div[data-testid="stDataFrame"] {
        background:#1F2937;
    }
    </style>

    """,

    unsafe_allow_html=True
)
st.title(
    "📊 Dashboard"
)
try:
    response = requests.get(
        "http://127.0.0.1:5000/history",
        timeout=10
    )
    data = response.json()
except Exception:
    st.error(
        "Backend is not running"
    )
    st.stop()

if not data:
    st.info(
        "No uploaded files found"
    )
    st.stop()

df = pd.DataFrame(data)
st.subheader(
    "📈 Summary"
)
total = len(df)
success = len(
    df[
        df["status"]=="Success"
    ]
)
failed = len(
    df[
        df["status"]=="Failed"
    ]
)
avg_score = round(
    df["score"].mean(),
    2
)
c1,c2,c3,c4 = st.columns(4)
with c1:

    st.markdown(
        f"""
        <div class="summary-card total-card">
        <h4>Total Uploads</h4>
        <h1>{total}</h1>
        </div>
        """,
        unsafe_allow_html=True
    )
with c2:

    st.markdown(
        f"""
        <div class="summary-card success-card">
        <h4>Successful</h4>
        <h1>{success}</h1>
        </div>
        """,
        unsafe_allow_html=True
    )
with c3:
    st.markdown(
        f"""
        <div class="summary-card failed-card">
        <h4>Failed</h4>
        <h1>{failed}</h1>
        </div>
        """,
        unsafe_allow_html=True
    )



with c4:
    st.markdown(
        f"""
        <div class="summary-card score-card">
        <h4>Average Score</h4>
        <h1>{avg_score}%</h1>
        </div>
        """,
        unsafe_allow_html=True
    )
st.divider()
st.subheader(
    "📂 Uploaded Files"
)
columns = st.columns(2)
for index,row in df.iterrows():
    with columns[index % 2]:
        with st.container():
            st.markdown(
                f"""
                <div class="file-card">
                <div class="file-title">
                📄 {row['filename']}
                </div>
                <br>
                <h4>
                {"🟢 Success" if row['status']=="Success" else "🔴 Failed"}
                </h4>
                <p class="small-text">
                👤 Uploaded By : {row['user']}
                </p>
                <p class="small-text">
                📅 Date : {row['date']}
                </p>
                <h3>
                ⭐ {row['score']}%
                </h3>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.write("")
            if st.button(
                "View Details",
                key=f"details_{row['id']}"
            ):
                st.session_state[
                    "selected_file"
                ] = row["id"]


                st.rerun()
st.divider()

# =============================
# REPORT DETAILS (FINAL WORKING)
# =============================

import json

# ✅ Ensure session state exists
if "selected_file" not in st.session_state:
    st.session_state["selected_file"] = None


# ✅ Show report only if selected
if st.session_state["selected_file"] is not None:

    selected_id = st.session_state["selected_file"]

    report = df[df["id"] == selected_id].iloc[0]

    # ✅ Convert validation safely
    validation = report["validation"]
    if isinstance(validation, str):
        try:
            validation = json.loads(validation)
        except:
            validation = {}

    st.divider()
    st.header("📄 Audit Report")

    # =============================
    # CLOSE BUTTON
    # =============================
    if st.button("❌ Close Report"):
        st.session_state["selected_file"] = None
        st.rerun()

    st.divider()

    # =============================
    # STATUS DISPLAY
    # =============================
    status = report.get("status", "Failed")

    if status == "Success":
        st.success("🟢 Audit Successful")
    elif status == "Warning":
        st.warning("🟡 Audit Completed with Warnings")
    else:
        st.error("🔴 Audit Failed")

    # =============================
    # FILE METADATA
    # =============================
    st.header("📄 File Metadata")

    m1, m2, m3, m4 = st.columns(4)

    m1.metric("File Name", report.get("filename", "-"))
    m2.metric("Uploaded By", report.get("user", "-"))
    m3.metric("Score", f"{report.get('score', 0)}%")
    m4.metric("Status", status)

    st.write("📅 Uploaded Date:", report.get("date", "-"))

    st.divider()

    # =============================
    # DATASET SUMMARY
    # =============================
    st.header("📊 Dataset Summary")

    rows = report.get("rows", 0)
    cols = report.get("columns", 0)
    duplicates = validation.get("duplicates", 0) if isinstance(validation, dict) else 0

    s1, s2, s3 = st.columns(3)

    s1.metric("Total Rows", rows)
    s2.metric("Total Columns", cols)
    s3.metric("Duplicate Rows", duplicates)

    st.divider()

    # =============================
    # VALIDATION REPORT
    # =============================
    st.header("🔍 Validation Report")

    if not isinstance(validation, dict) or not validation:
        st.error("No validation data available (file may be empty or corrupted)")
    else:

        # -------------------------
        # Missing Values
        # -------------------------
        st.subheader("Missing Values")

        if validation.get("missing_values"):
            st.dataframe(
                pd.DataFrame(validation["missing_values"]),
                use_container_width=True
            )
        else:
            st.success("✅ No missing values detected")

        # -------------------------
        # Duplicate Rows
        # -------------------------
        st.subheader("Duplicate Rows")
        st.info(validation.get("duplicates", 0))

        # -------------------------
        # Schema Validation
        # -------------------------
        st.subheader("Schema Validation")

        if validation.get("schema_errors"):
            for err in validation["schema_errors"]:
                st.error(err)
        else:
            st.success("✅ Schema is correct")

        # -------------------------
        # Additional Checks
        # -------------------------
        st.subheader("Additional Checks")

        if validation.get("additional_checks"):
            for item in validation["additional_checks"]:
                st.write("✅", item)
        else:
            st.info("No additional issues found")

        # -------------------------
        # Data Types
        # -------------------------
        st.subheader("Column Data Types")

        datatypes = validation.get("datatypes", {})

        if datatypes:
            st.dataframe(
                pd.DataFrame(
                    datatypes.items(),
                    columns=["Column", "Datatype"]
                ),
                use_container_width=True
            )
        else:
            st.warning("No datatype info available")