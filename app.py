import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Raksha AP Cyber Command",
    page_icon="🚔",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
  .main {background-color: #0E1117;}
  .block-container {padding-top: 2rem;}
    h1 {color: #FF4B4B; text-align: center; font-family: 'Arial Black';
        text-shadow: 2px 2px 4px #000000;}
    h3 {color: #FAFAFA; text-align: center;}
  .stButton>button {
        background: linear-gradient(90deg, #FF4B4B 0%, #FF6B6B 100%);
        color: white; border-radius: 10px; border: none;
        padding: 0.5rem 1rem; font-weight: bold;
        box-shadow: 0 4px 6px rgba(255, 75, 0.3);
    }
  .stButton>button:hover {
        background: linear-gradient(90deg, #FF6B6B 0%, #FF4B4B 100%);
        transform: scale(1.02);
    }
    [data-testid="stMetricValue"] {color: #FF4B4B; font-size: 28px;}
</style>
""", unsafe_allow_html=True)

if 'crime_data' not in st.session_state:
    st.session_state.crime_data = pd.DataFrame({
        "District": ["Kakinada", "Visakhapatnam", "Vijayawada", "Tirupati", "Guntur", "Nellore", "Kurnool", "Rajamahendravaram", "Anantapur", "Kadapa"],
        "Lat": [16.9891, 17.6869, 16.5062, 13.6288, 16.3067, 14.4426, 15.8281, 17.0005, 14.6819, 14.4673],
        "Lon": [82.2475, 83.2185, 80.6480, 79.4192, 80.4365, 79.9865, 78.0373, 81.8040, 77.6006, 78.8242],
        "Crime": ["Aviator Betting", "Loan App Harassment", "SBI KYC Scam", "Nude Call Blackmail", "FedEx Scam", "Aviator Betting", "Loan App", "KYC Scam", "Betting", "Nude Call"],
        "Cases": [47, 62, 55, 31, 43, 28, 19, 36, 22, 17],
        "Threat": ["Critical", "Critical", "Critical", "High", "Critical", "High", "Medium", "High", "Medium", "Medium"]
    })

st.title("🚔 RAKSHA AP CYBER COMMAND CENTER")
st.markdown("### Andhra Pradesh State | Live Crime Intelligence | Student Network")
st.markdown("---")

col1, col2 = st.columns([3, 1.2])

with col1:
    st.subheader("🗺️ AP State Scam Hotspot Map")
    m = folium.Map(
        location=[15.9129, 79.7400],
        zoom_start=7,
        tiles="CartoDB dark_matter",
        attr="AP Cyber Police"
    )

    for idx, row in st.session_state.crime_data.iterrows():
        color_map = {"Critical": "#FF0000", "High": "#FF6B00", "Medium": "#FFD700", "Low": "#90EE90"}
        color = color_map.get(row["Threat"], "blue")
        radius = row["Cases"] * 50
        popup_html = f"""
        <div style="font-family: Arial; width: 200px;">
            <h4 style="color: #FF4B4B; margin: 0;">📍 {row['District']}</h4>
            <hr style="margin: 5px 0;">
            <b>Top Crime:</b> {row['Crime']}<br>
            <b>Reports:</b> {row['Cases']} cases<br>
            <b>Threat Level:</b> <span style="color: {color}; font-weight: bold;">{row['Threat']}</span><br>
            <small>Updated: {datetime.now().strftime('%I:%M %p')}</small>
        </div>
        """
        folium.CircleMarker(
            location=[row["Lat"], row["Lon"]],
            radius=max(8, row["Cases"]/2),
            popup=folium.Popup(popup_html, max_width=250),
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            weight=2
        ).add_to(m)
        folium.Marker(
            [row["Lat"], row["Lon"]],
            icon=folium.DivIcon(html=f"""<div style="font-size: 10pt; color: white;
            text-shadow: 1px 1px 2px black; font-weight: bold;">{row['District']}</div>""")
        ).add_to(m)

    st_data = st_folium(m, width=None, height=550, returned_objects=["last_object_clicked"])

with col2:
    st.subheader("🔥 Live AP Statistics")
    total_cases = st.session_state.crime_data["Cases"].sum()
    critical_districts = len(st.session_state.crime_data[st.session_state.crime_data["Threat"] == "Critical"])
    st.metric("Total Alerts - AP", f"{total_cases}", "+89")
    st.metric("Critical Districts", f"{critical_districts}", "Needs Action")
    st.metric("Top Scam AP", "Loan App + Aviator", "68% Cases")
    st.markdown("---")
    st.markdown("#### 🚨 Top Hotspot Districts")
    sorted_df = st.session_state.crime_data.sort_values("Cases", ascending=False)
    for idx, row in sorted_df.iterrows():
        if row["Threat"] == "Critical":
            st.error(f"**{row['District']}**\n{row['Cases']} cases - {row['Crime']}")
        elif row["Threat"] == "High":
            st.warning(f"**{row['District']}**\n{row['Cases']} cases - {row['Crime']}")
        else:
            st.info(f"**{row['District']}**\n{row['Cases']} cases")
    st.caption(f"🕐 Last Updated: {datetime.now().strftime('%d %b %Y, %I:%M %p')}")

st.markdown("---")
col3, col4, col5 = st.columns(3)
with col3:
    st.success("✅ **100% Anonymous** - No personal data collected")
with col4:
    st.info("📊 **Data Source**: Student Intelligence Network")
with col5:
    st.warning("⚠️ **For Official Use** - AP Cyber Police")

with st.expander("🧪 Demo: Add New Alert - Test Chesei"):
    test_district = st.selectbox("Select District", st.session_state.crime_data["District"].tolist())
    test_crime = st.selectbox("Crime Type", ["Aviator Betting", "SBI KYC Scam", "Nude Call", "Loan App Harassment"])
    if st.button("➕ Add Alert to Map"):
        idx = st.session_state.crime_data[st.session_state.crime_data["District"] == test_district].index[0]
        st.session_state.crime_data.loc[idx, "Cases"] += 1
        new_cases = st.session_state.crime_data.loc[idx, "Cases"]
        if new_cases > 50:
            st.session_state.crime_data.loc[idx, "Threat"] = "Critical"
        elif new_cases > 30:
            st.session_state.crime_data.loc[idx, "Threat"] = "High"
        st.success(f"Alert Added! {test_district} lo case count penchindi. Map refresh chey.")
        st.rerun()
