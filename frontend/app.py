#
import streamlit as st


st.set_page_config(
    page_title="Audit Tool",
    page_icon="📊",
    layout="wide"
)


# =============================
# GLOBAL DARK THEME
# =============================

st.markdown(
    """
    <style>

    .stApp {

        background-color:#15151D;

    }


    header[data-testid="stHeader"] {

        background-color:#15151D;

    }


    header[data-testid="stHeader"] button {

        background-color:#15151D;

        color:white;

    }


    div[data-testid="stToolbar"] {

        background-color:#15151D;

    }


    h1,h2,h3,h4,h5,h6,p,span,label {

        color:white !important;

    }


    section[data-testid="stSidebar"] {

        background-color:#15151D;

    }


    .block-container {

        padding-top:2rem;

    }



    .welcome-card {

        background:#1F2937;

        padding:50px;

        border-radius:20px;

        text-align:center;

        border:1px solid #374151;

        margin-top:80px;

    }


.welcome-title {

    font-size:40px;
    font-weight:bold;
    color:white !important;

}


.description-text {

    font-size:20px;
    color:#D1D5DB;
    margin-top:20px;

}


    .feature-box {

        background:#111827;

        padding:20px;

        border-radius:15px;

        text-align:center;

        border:1px solid #374151;

        margin-top:30px;

    }


    </style>

    """,

    unsafe_allow_html=True
)

# =============================
# HOME CONTENT
# =============================

st.html(
    """
    <div class="welcome-card">

        <div class="welcome-title">
            📊 Data Upload Audit Tool
        </div>

        <div class="description-text">
            Upload your datasets and analyze data quality,
            consistency, and validation issues automatically.
        </div>

    </div>
    """
)

# Feature cards

col1, col2, col3 = st.columns(3)


with col1:

    st.markdown(
        """
        <div class="feature-box">

        <h3>📤 Upload Data</h3>

        <p>
        Upload CSV or Excel files
        for automated auditing.
        </p>

        </div>
        """,

        unsafe_allow_html=True
    )



with col2:

    st.markdown(
        """
        <div class="feature-box">

        <h3>🔍 Data Validation</h3>

        <p>
        Detect missing values,
        duplicates, and schema issues.
        </p>

        </div>
        """,

        unsafe_allow_html=True
    )



with col3:

    st.markdown(
        """
        <div class="feature-box">

        <h3>📊 Audit Reports</h3>

        <p>
        View quality scores and
        detailed audit history.
        </p>

        </div>
        """,

        unsafe_allow_html=True
    )