import streamlit as st
import requests
from dotenv import load_dotenv
import os

load_dotenv()
# Config
API_URL = os.getenv("VIN_API_URL")

# --- Page Setup ---
st.set_page_config(page_title="AutoInsight", page_icon="🚘", layout="wide")

# --- Custom CSS ---
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* Card style with gradient background */
.card {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    padding: 30px;
    border-radius: 15px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    transition: 0.3s;
    margin-bottom: 25px;
}
.card:hover {
    transform: scale(1.03);
}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg,#667eea,#764ba2);
    color: white;
    font-size: 1.2em;
    padding: 0.7em 2em;
    border-radius: 12px;
    border: none;
    transition: 0.3s;
    width: 100%;
}
.stButton>button:hover {
    background: linear-gradient(90deg,#764ba2,#667eea);
    transform: scale(1.05);
    cursor: pointer;
}

/* Section headings */
.section-header {
    color: #333;
    font-weight: 700;
    margin-bottom: 20px;
    font-size: 2em;
}

/* Sub-card titles */
.card-title {
    font-size: 1.5em;
    font-weight: 700;
    margin-bottom: 12px;
}

/* Sub-card description */
.card-desc {
    font-size: 1.1em;
    line-height: 1.6;
}
</style>
""", unsafe_allow_html=True)

# --- Landing / Info Section ---
st.markdown("""
<div style='text-align:center; padding:60px; background: linear-gradient(135deg, #667eea, #764ba2); 
            color:white; border-radius:15px; margin-bottom:40px;'>
    <h1 style='font-size:3.2em;'>🚘 AutoInsight</h1>
    <h3 style='font-size:1.5em;'>Your AI-powered Vehicle Analysis & Risk Assessment Tool</h3>
    <p style='font-size:1.2em; max-width:800px; margin:auto; line-height:1.7;'>
    Not sure what your VIN (Vehicle Identification Number) really means? AutoInsight guides you step-by-step 
    to uncover detailed vehicle info, safety insights, and risk scores. Buy smarter, sell smarter, drive safer.
    </p>
</div>
""", unsafe_allow_html=True)

# --- VIN Input Section ---
st.markdown("<h2 class='section-header' style='text-align:center;'>Enter Your VIN</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    vin = st.text_input("", placeholder="e.g. 5J6RS5H54RL006999")
    st.markdown("<br>", unsafe_allow_html=True)

    # Center the button using additional inner columns
    btn_col1, btn_col2, btn_col3 = st.columns([1,2,1])
    with btn_col2:
        generate = st.button("Generate Vehicle Summary")

# --- VIN Summary / Results Section with Validation and VIN-not-found Handling ---
if generate:
    if not vin:
        st.warning("⚠️ Please enter a VIN before generating a summary.")
    elif not vin.isalnum():
        st.warning("⚠️ Invalid VIN. A valid VIN should only contain letters and numbers.")
    else:
        with st.spinner("Fetching summary..."):
            try:
                response = requests.post(API_URL, json={"vin": vin})

                if response.status_code == 200:
                    data = response.json()
                    st.success("✅ Summary generated!")

                    res_col1, res_col2 = st.columns([3, 1])

                    # --- Vehicle Summary ---
                    with res_col1:
                        st.markdown(f"""
                        <div style='padding:25px; border-radius:12px; box-shadow: 0 4px 12px rgba(0,0,0,0.08);'>
                            <h3 style='margin-bottom:15px; color:white;'>Vehicle Summary</h3>
                            <p style='color:white; line-height:1.6;'>{data.get("summary", "No summary available.")}</p>
                        </div>
                        """, unsafe_allow_html=True)

                    # --- Risk Score ---
                    with res_col2:
                        st.markdown(f"""
                        <div style='padding:25px; border-radius:12px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); text-align:center;'>
                            <h3 style='margin-bottom:15px; color:white;'>Risk Score</h3>
                            <p style='font-size:2em; font-weight:700; color:white;'>{data.get("risk_score", "N/A")}</p>
                        </div>
                        """, unsafe_allow_html=True)

                    st.subheader("Reasoning")
                    reasoning = data.get("reasoning", [])
                    with st.expander("View detailed reasoning"):
                        if isinstance(reasoning, list) and len(reasoning) > 0:
                            for r in reasoning:
                                st.markdown(f"- {r}")
                        else:
                            st.write("No reasoning available for this VIN.")

                elif response.status_code == 404:
                    st.error(f"❌ VIN not found in dataset: {vin}.Please input a valid VIN")
                else:
                    # Other errors
                    try:
                        err_msg = response.json().get("message", response.text)
                    except Exception:
                        err_msg = response.text
                    st.error(f"⚠️ Error {response.status_code}: {err_msg}")

            except Exception as e:
                st.error(f"⚠️ Could not connect to API: {e}")

# --- Why AutoInsight Section ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align:center; color:white; font-size:2.2em;'>Why Choose AutoInsight?</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:white; max-width:750px; margin:auto; margin-bottom:30px; line-height:1.8;'>"
    "Discover the benefits for buyers, sellers, and the community, plus guidance for everyone."
    "</p>", unsafe_allow_html=True)

# --- 3-column main benefits with dual-shade gradient ---
benefit_col1, benefit_col2, benefit_col3 = st.columns(3)

benefits = [
    {"icon":"🔍", "title":"For Buyers", "desc":"Get insights into vehicle history, accidents, and hidden risks. Make informed purchasing decisions and avoid costly surprises."},
    {"icon":"🤝", "title":"For Sellers", "desc":"Show transparency with detailed vehicle summaries and risk scores. Build trust, sell faster, and boost credibility."},
    {"icon":"🌐", "title":"Community Impact", "desc":"Encourage safer, informed vehicle transactions. Everyone in the automotive community benefits from shared knowledge and improved trust."}
]

for col, b in zip([benefit_col1, benefit_col2, benefit_col3], benefits):
    with col:
        st.markdown(f"""
        <div class="card" style="text-align:center; background: linear-gradient(135deg, #667eea, #764ba2);">
            <div style="font-size:2em; margin-bottom:12px;">{b['icon']}</div>
            <div class="card-title">{b['title']}</div>
            <div class="card-desc">{b['desc']}</div>
        </div>
        """, unsafe_allow_html=True)

# --- Guidance Card (full width below) ---
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div class="card" style="text-align:center; background: linear-gradient(135deg, #667eea, #764ba2);">
    <div style="font-size:2em; font-weight:700; margin-bottom:10px;">📘 Guidance for Everyone</div>
    <div style="font-size:1.2em; line-height:1.6; max-width:800px; margin:auto;">
    Even if you're new to VINs, AutoInsight explains every detail clearly. Understand each vehicle’s history, safety, and risk, ensuring informed decisions for all users.
    </div>
</div>
""", unsafe_allow_html=True)

# --- Footer ---
st.markdown("<br><br><p style='text-align:center; color:gray;'>Powered by Streamlit & Your VIN API 🚀</p>", unsafe_allow_html=True)
