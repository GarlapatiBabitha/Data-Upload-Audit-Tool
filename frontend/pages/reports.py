import streamlit as st
from utils.api import get_history
import pandas as pd
from io import BytesIO

st.set_page_config(
    page_title="Reports",
    page_icon="📄",
    layout="wide"
)

st.markdown("""
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

/* METRIC CARDS */
div[data-testid="metric-container"] {
    background:#1F2937;
    padding:15px;
    border-radius:12px;
    border:1px solid #374151;
    text-align:center;
}

/* DOWNLOAD BUTTON */
div.stDownloadButton > button {
    width:100%;
    background:#2563EB;
    color:white;
    border-radius:10px;
    border:none;
    padding:10px;
    font-weight:bold;
}

div.stDownloadButton > button:hover {
    background:#1D4ED8;
}

/* REMOVE TOP SPACE */
.block-container {
    padding-top:2rem;
}

/* CUSTOM TABLE */
.custom-table {
    width: 100%;
    border-collapse: collapse;
    background-color: #1F2937;
    color: white;
}

.custom-table th {
    background-color: #111827;
    padding: 10px;
    border: 1px solid white;
    text-align: left;
}

.custom-table td {
    padding: 10px;
    border: 1px solid white;
}

.custom-table tr:hover {
    background-color: #374151;
}

/* ✅ SCROLLABLE TABLE CONTAINER */
.table-container {
    max-height: 400px;   /* adjust height if needed */
    overflow-y: auto;
    border-radius: 10px;
    border: 1px solid #374151;
}

</style>
""", unsafe_allow_html=True)

st.markdown(
    "<h1 style='text-align:center;'>📄 Audit Reports</h1>",
    unsafe_allow_html=True
)
data = get_history()

if not data:
    st.warning("No audit records available or backend not connected")
    st.stop()
    
df = pd.DataFrame(data)

# ===================== SUMMARY =====================
st.subheader("📊 Report Summary")

total_uploads = len(df)
success_count = len(df[df["status"] == "Success"])
failed_count = len(df[df["status"] == "Failed"])
average_score = round(df["score"].mean(), 2)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Uploads", total_uploads)
col2.metric("Successful", success_count)
col3.metric("Failed", failed_count)
col4.metric("Average Score", f"{average_score}%")

st.divider()

# ===================== TABLE =====================
st.subheader("📋 Upload History")

df_display = df.copy()

df_display.insert(0, "S.No", range(1, len(df_display)+1))

df_display.rename(columns={
    "filename": "File Name",
    "user": "Username",
    "date": "Timestamp",
    "score": "Score",
    "status": "Status"
}, inplace=True)

df_display = df_display[
    ["S.No", "File Name", "Username", "Timestamp", "Score", "Status"]
]

# Build HTML table
table_html = "<table class='custom-table'><tr>"

# Header
for col in df_display.columns:
    table_html += f"<th>{col}</th>"

table_html += "</tr>"

# Rows
for _, row in df_display.iterrows():
    table_html += "<tr>"
    for val in row:
        table_html += f"<td>{val}</td>"
    table_html += "</tr>"

table_html += "</table>"

# ✅ Wrap table inside scrollable container
st.markdown(
    f"<div class='table-container'>{table_html}</div>",
    unsafe_allow_html=True
)

st.divider()

# ===================== DOWNLOAD =====================
st.subheader("📥 Download Full Report")

download_col1, download_col2 = st.columns(2)

# CSV
with download_col1:
    csv = df_display.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download CSV",
        data=csv,
        file_name="audit_report.csv",
        mime="text/csv"
    )

# Excel
with download_col2:
    buffer = BytesIO()

    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df_display.to_excel(
            writer,
            index=False,
            sheet_name="Audit Report"
        )

    st.download_button(
        label="⬇️ Download Excel",
        data=buffer.getvalue(),
        file_name="audit_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )