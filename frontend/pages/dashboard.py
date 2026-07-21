   
# import streamlit as st
# import requests
# import pandas as pd
# import json

# st.set_page_config(
#     page_title="Dashboard",
#     page_icon="📊",
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
#     header[data-testid="stHeader"] > div {
#         background-color:#15151D !important;
#     }

#     div[data-testid="stToolbar"] {
#         background-color:#15151D !important;
#     }

#     div[data-testid="stToolbar"] button {
#         background-color:#15151D !important;
#         color:white !important;
#     }

#     button[kind="header"] {
#         background-color:#15151D !important;
#         color:white !important;
#     }

#     section[data-testid="stSidebar"] {
#         background-color:#15151D !important;
#     }
#     section[data-testid="stSidebar"] > div {
#         background-color:#15151D !important;
#     }

#     section[data-testid="stSidebar"] * {
#         color:white !important;
#     }

#     h1,h2,h3,h4,h5,h6,p,span,label {
#         color:white !important;
#     }

#     .block-container {
#         padding-top:2rem;
#     }

#     .summary-card {
#         padding:15px;
#         border-radius:15px;
#         color:white;
#         height:120px;
#         margin-bottom:20px;
#         text-align:center;
#     }
#     .summary-card h4 {
#         margin-top:-10px;
#         margin-bottom:5px;
#         font-size:25px;
#     }
#     .summary-card h1 {
#         margin-top:0px;
#         margin-bottom:0px;
#         font-size:38px;
#         line-height:1;

#     }
#     .total-card {
#         background:#2563EB;
#     }
#     .success-card {
#         background:#16A34A;
#     }
#     .failed-card {
#         background:#DC2626;
#     }
#    .score-card {
#         background:#9333EA;
#     }

#     .file-card {
#         background:#1F2937;
#         padding:25px;
#         border-radius:18px;
#         border:1px solid #374151;
#         min-height:250px;
#     }
#    .file-title {
#         font-size:22px;
#         color:white;
#     }
#     .small-text {
#         color:#D1D5DB;
#         font-size:15px;
#     }
#     div.stButton > button {
#         width:100%;
#         border-radius:10px;
#         background:#374151;
#         color:white;
#         border:none;
#     }
#     div.stButton > button:hover {
#         background:#4B5563;
#         color:white;
#     }

#     div[data-testid="stDataFrame"] {
#         background:#1F2937;
#     }
#     </style>

#     """,

#     unsafe_allow_html=True
# )
# st.title(
#     "📊 Dashboard"
# )
# try:
#     response = requests.get(
#         "http://127.0.0.1:5000/history",
#         timeout=10
#     )
#     data = response.json()
# except Exception:
#     st.error(
#         "Backend is not running"
#     )
#     st.stop()

# if not data:
#     st.info(
#         "No uploaded files found"
#     )
#     st.stop()

# df = pd.DataFrame(data)
# original_df = df.copy()

# # 🔍 Search / Score Filter
# search = st.text_input("🔍 Search files or enter minimum score", "")

# if search:
#     search_lower = search.lower()

#     # If user enters a number → filter by score
#     if search.isdigit():
#         score_filter = float(search)
#         df = df[df["score"] >= score_filter]

#     else:
#         # Normal text search
#         df = df[
#             df.apply(
#                 lambda row: (
#                     search_lower in str(row.get("filename", "")).lower()
#                     or search_lower in str(row.get("user", "")).lower()
#                     or search_lower in str(row.get("status", "")).lower()
#                 ),
#                 axis=1
#             )
#         ]
        
# st.subheader(
#     "📈 Summary"
# )
# total = len(original_df)
# success = len(
#     original_df[
#         original_df["status"]=="Success"
#     ]
# )
# failed = len(
#     original_df[
#         original_df["status"]=="Failed"
#     ]
# )
# avg_score = round(
#     original_df["score"].mean(),
#     2
# )
# c1,c2,c3,c4 = st.columns(4)
# with c1:

#     st.markdown(
#         f"""
#         <div class="summary-card total-card">
#         <h4>Total Uploads</h4>
#         <h1>{total}</h1>
#         </div>
#         """,
#         unsafe_allow_html=True
#     )
# with c2:

#     st.markdown(
#         f"""
#         <div class="summary-card success-card">
#         <h4>Successful</h4>
#         <h1>{success}</h1>
#         </div>
#         """,
#         unsafe_allow_html=True
#     )
# with c3:
#     st.markdown(
#         f"""
#         <div class="summary-card failed-card">
#         <h4>Failed</h4>
#         <h1>{failed}</h1>
#         </div>
#         """,
#         unsafe_allow_html=True
#     )



# with c4:
#     st.markdown(
#         f"""
#         <div class="summary-card score-card">
#         <h4>Average Score</h4>
#         <h1>{avg_score}%</h1>
#         </div>
#         """,
#         unsafe_allow_html=True
#     )
# st.divider()
# st.subheader(
#     "📂 Uploaded Files"
# )
# columns = st.columns(2)
# for index, row in df.reset_index(drop=True).iterrows():
#     with columns[index % 2]:
#         with st.container():
#             st.markdown(
#                 f"""
#                 <div class="file-card">
#                 <div class="file-title">
#                 📄 {row['filename']}
#                 </div>
#                 <br>
#                 <h4>
#                 {"🟢 Success" if row['status']=="Success" else "🔴 Failed"}
#                 </h4>
#                 <p class="small-text">
#                 👤 Uploaded By : {row['user']}
#                 </p>
#                 <p class="small-text">
#                 📅 Date : {row['date']}
#                 </p>
#                 <h3>
#                 ⭐ {row['score']}%
#                 </h3>
#                 </div>
#                 """,
#                 unsafe_allow_html=True
#             )
#             st.write("")
#             if st.button(
#                 "View Details",
#                 key=f"details_{row['id']}"
#             ):
#                 st.session_state[
#                     "selected_file"
#                 ] = row["id"]


#                 st.rerun()
# st.divider()

# # Ensure session state exists
# if "selected_file" not in st.session_state:
#     st.session_state["selected_file"] = None

# # Show report only if selected
# if st.session_state["selected_file"] is not None:

#     selected_id = st.session_state["selected_file"]

#     # Fetch latest data from backend
#     try:
#         response = requests.get(
#             "http://127.0.0.1:5000/history",
#             timeout=10
#         )
#         fresh_data = response.json()
#         fresh_df = pd.DataFrame(fresh_data)
#     except:
#         st.error("Failed to fetch data from DB")
#         st.stop()

#     # Filter using ID
#     report = fresh_df[fresh_df["id"] == selected_id].iloc[0]

#     # Convert validation safely
#     validation = report["validation"]
#     if isinstance(validation, str):
#         try:
#             validation = json.loads(validation)
#         except:
#             validation = {}

#     st.divider()
#     st.header("📄 Audit Report")

#     # Close button
#     if st.button("❌ Close Report"):
#         st.session_state["selected_file"] = None
#         st.rerun()

#     st.divider()

#     # Status display
#     status = report.get("status", "Failed")

#     if status == "Success":
#         st.success("🟢 Audit Successful")
#     elif status == "Warning":
#         st.warning("🟡 Audit Completed with Warnings")
#     else:
#         st.error("🔴 Audit Failed")

#     # =============================
#     # FILE METADATA (FROM DB)
#     # =============================
#     st.header("📄 File Metadata")

#     m1, m2, m3, m4 = st.columns(4)

#     m1.metric("File Name", report.get("filename", "-"))
#     m2.metric("Uploaded By", report.get("user", "-"))
#     m3.metric("Score", f"{report.get('score', 0)}%")
#     m4.metric("Status", status)

#     st.write("📅 Uploaded Date:", report.get("date", "-"))

#     st.divider()

#     # =============================
#     # VALIDATION REPORT (ONLY STORED PART)
#     # =============================
#     st.header("🔍 Validation Report")

#     if not isinstance(validation, dict) or not validation:
#         st.error("No validation data available")
#     else:

#         # Missing Values
#         st.subheader("Missing Values")
#         if validation.get("missing_values"):
#             st.dataframe(
#                 pd.DataFrame(validation["missing_values"]),
#                 use_container_width=True
#             )
#         else:
#             st.success("✅ No missing values detected")

#         # Duplicate Rows (only if present)
#         if "duplicates" in validation:
#             st.subheader("Duplicate Rows")
#             st.info(validation.get("duplicates", 0))

#         # Schema Validation
#         st.subheader("Schema Validation")
#         if validation.get("schema_errors"):
#             for err in validation["schema_errors"]:
#                 st.error(err)
#         else:
#             st.success("✅ Schema is correct")

#         # Additional Checks
#         st.subheader("Additional Checks")
#         if validation.get("additional_checks"):
#             for item in validation["additional_checks"]:
#                 st.write("✅", item)
#         else:
#             st.info("No additional issues found")

#         # Data Types
#         st.subheader("Column Data Types")
#         datatypes = validation.get("datatypes", {})

#         if datatypes:
#             st.dataframe(
#                 pd.DataFrame(
#                     datatypes.items(),
#                     columns=["Column", "Datatype"]
#                 ),
#                 use_container_width=True
#             )
#         else:
#             st.warning("No datatype info available")
    
    


import streamlit as st
import requests
import pandas as pd
import json

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

# ================= CSS =================
st.markdown("""
<style>
.stApp { background-color:#15151D; }

header[data-testid="stHeader"],
div[data-testid="stToolbar"] {
    background-color:#15151D !important;
}

section[data-testid="stSidebar"] {
    background-color:#15151D !important;
}

section[data-testid="stSidebar"] * {
    color:white !important;
}

.block-container { padding-top:2rem; }

/* ===== SUMMARY CARDS ===== */
.summary-card {
    padding:15px;
    border-radius:15px;
    color:white;
    height:120px;
    text-align:center;
}
.summary-card h4 {
    margin-top:-10px;
    margin-bottom:5px;
    font-size:25px;
}
.summary-card h1 {
    margin:0;
    font-size:38px;
}
.total-card { background:#2563EB; }
.success-card { background:#16A34A; }
.failed-card { background:#DC2626; }
.score-card { background:#9333EA; }

/* ===== FILE CARDS (ORIGINAL STYLE) ===== */
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

/* ===== META CARDS ===== */
.meta-card {
    background:#1F2937;
    padding:20px;
    border-radius:16px;
    border:1px solid #374151;
    text-align:center;
}
.meta-title {
    color:#9CA3AF;
    font-size:14px;
}
.meta-value {
    color:white;
    font-size:20px;
    font-weight:bold;
}

/* ===== TABLE ===== */
table {
    width:100%;
    border-collapse:collapse;
    background:#1F2937;
}
th, td {
    padding:10px;
    border-bottom:1px solid #374151;
    color:white;
}
th { background:#111827; }

/* ===== BUTTON ===== */
div.stButton > button {
    width:100%;
    border-radius:10px;
    background:#374151;
    color:white;
    border:none;
}
div.stButton > button:hover {
    background:#4B5563;
}
/* ===== FIX TEXT VISIBILITY ===== */

/* Main titles */
h1, h2, h3, h4, h5, h6 {
    color: white !important;
}

/* Streamlit labels, inputs, text */
label, .stTextInput label, .stMarkdown, .stSubheader {
    color: white !important;
}

/* Search input text */
input {
    color: white !important;
    background-color:#1F2937 !important;
}

/* Placeholder text */
input::placeholder {
    color:#9CA3AF !important;
}

/* Fix dataframe / tables text */
div[data-testid="stDataFrame"] * {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

st.title("📊 Dashboard")

# ================= FETCH =================
try:
    data = requests.get("http://127.0.0.1:5000/history").json()
except:
    st.error("Backend not running")
    st.stop()

if not data:
    st.info("No uploaded files found")
    st.stop()

df = pd.DataFrame(data)
original_df = df.copy()

# ================= SEARCH =================
search = st.text_input("🔍 Search files or enter minimum score")

if search:
    if search.isdigit():
        df = df[df["score"] >= float(search)]
    else:
        s = search.lower()
        df = df[df.apply(lambda r:
            s in str(r["filename"]).lower() or
            s in str(r["user"]).lower() or
            s in str(r["status"]).lower(), axis=1)]

# ================= SUMMARY =================
st.subheader("📈 Summary")

c1,c2,c3,c4 = st.columns(4)

c1.markdown(f"<div class='summary-card total-card'><h4>Total Uploads</h4><h1>{len(original_df)}</h1></div>", True)
c2.markdown(f"<div class='summary-card success-card'><h4>Successful</h4><h1>{len(original_df[original_df['status']=='Success'])}</h1></div>", True)
c3.markdown(f"<div class='summary-card failed-card'><h4>Failed</h4><h1>{len(original_df[original_df['status']=='Failed'])}</h1></div>", True)
c4.markdown(f"<div class='summary-card score-card'><h4>Average Score</h4><h1>{round(original_df['score'].mean(),2)}%</h1></div>", True)

st.divider()

# ================= FILE CARDS =================
st.subheader("📂 Uploaded Files")

cols = st.columns(2)

for i, row in df.reset_index(drop=True).iterrows():
    with cols[i % 2]:

        st.markdown(f"""
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
        """, unsafe_allow_html=True)

        if st.button("View Details", key=f"id_{row['id']}"):
            st.session_state["selected_file"] = row["id"]
            st.rerun()

# ================= REPORT =================
if "selected_file" not in st.session_state:
    st.session_state["selected_file"] = None

if st.session_state["selected_file"]:

    report = pd.DataFrame(requests.get("http://127.0.0.1:5000/history").json())
    report = report[report["id"] == st.session_state["selected_file"]].iloc[0]

    validation = report["validation"]
    if isinstance(validation, str):
        validation = json.loads(validation)

    st.divider()

    col1, col2 = st.columns([6,1])
    with col1:
        st.header("📄 Audit Report")
    with col2:
        if st.button("❌ Close"):
            st.session_state["selected_file"] = None
            st.rerun()

    st.divider()

    # ===== META CARDS =====
    st.header("📄 File Metadata")

    m1,m2,m3,m4 = st.columns(4)

    m1.markdown(f"<div class='meta-card'><div class='meta-title'>File Name</div><div class='meta-value'>{report['filename']}</div></div>", True)
    m2.markdown(f"<div class='meta-card'><div class='meta-title'>Uploaded By</div><div class='meta-value'>{report['user']}</div></div>", True)
    m3.markdown(f"<div class='meta-card'><div class='meta-title'>Score</div><div class='meta-value'>{report['score']}%</div></div>", True)
    m4.markdown(f"<div class='meta-card'><div class='meta-title'>Status</div><div class='meta-value'>{report['status']}</div></div>", True)

    st.write("🕒 Upload Time:", report["date"])

    st.divider()

    # ===== VALIDATION =====
    st.header("🔍 Validation Report")

    st.subheader("Missing Values")
    if validation.get("missing_values"):
        st.markdown(pd.DataFrame(validation["missing_values"]).to_html(index=False), True)
    else:
        st.success("✅ No missing values")

    st.subheader("Schema Validation")
    if validation.get("schema_errors"):
        for e in validation["schema_errors"]:
            st.error(e)
    else:
        st.success("✅ Schema is correct")

    st.subheader("Additional Checks")
    if validation.get("additional_checks"):
        for x in validation["additional_checks"]:
            st.write("✅", x)
    else:
        st.info("No issues found")

    st.subheader("Column Data Types")

    dt_df = pd.DataFrame(
        list(validation.get("datatypes", {}).items()),
        columns=["Column", "Data Type"]
    )

    st.markdown(dt_df.to_html(index=False), True)