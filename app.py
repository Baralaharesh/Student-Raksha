import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
from datetime import datetime

# ==================== PAGE CONFIG - ATTRACTIVE THEME ====================
st.set_page_config(
    page_title="Raksha Cyber Command",
    page_icon="🚔",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom Police Theme CSS
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

# ==================== SESSION STATE - LIVE DATA ====================
if 'crime_data' not in st.session_state:
    st.session_state.crime_data = pd.DataFrame({
        "Area": ["Jagannaickpur", "Gandhinagar", "Sarpavaram", "Turangi", "Kakinada Port", "Indrapalem"],
        "Lat": [16.9881, 16.9605, 17.0131, 17.0015, 16.9511, 17.0185],
        "Lon": [82.2389, 82.2356, 82.2638, 82.2285, 82.2456, 82.2521],
        "Crime": ["Aviator Betting", "SBI KYC Scam", "Nude Call Blackmail", "Loan App Harassment", "Aviator Betting", "FedEx Scam"],
        "Cases": [47, 23, 18, 12, 31, 9],
        "Threat": ["Critical", "High", "Medium", "Medium", "Critical", "Low"]
    })

# ==================== HEADER ====================
st.title("🚔 RAKSHA CYBER COMMAND CENTER")
st.markdown("### Kakinada District | Live Crime Intelligence | Student Network")
st.markdown("---")

# ==================== MAIN LAYOUT - MAP + STATS ====================
col1, col2 = st.columns([3, 1.2])

with col1:
    st.subheader("🗺️ Live Scam Hotspot Map")

    # Create Map
    m = folium.Map(
        location=[16.9891, 82.2475],
        zoom_start=12,
        tiles="CartoDB dark_matter",
        attr="Kakinada Cyber Police"
    )

    # Add Heat Circles
    for idx, row in st.session_state.crime_data.iterrows():
        # Color based on threat level
        color_map = {"Critical": "#FF0000", "High": "#FF6B00", "Medium": "#FFD700", "Low": "#90EE90"}
        color = color_map.get(row["Threat"], "blue")

        # Radius based on cases
        radius = row["Cases"] * 50

        # Popup HTML - Attractive
        popup_html = f"""
        <div style="font-family: Arial; width: 200px;">
            <h4 style="color: #FF4B4B; margin: 0;">📍 {row['Area']}</h4>
            <hr style="margin: 5px 0;">
            <b>Crime:</b> {row['Crime']}<br>
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

        # Add label
        folium.Marker(
            [row["Lat"], row["Lon"]],
            icon=folium.DivIcon(html=f"""<div style="font-size: 10pt; color: white;
            text-shadow: 1px 1px 2px black; font-weight: bold;">{row['Area']}</div>""")
        ).add_to(m)

    # Display Map
    st_data = st_folium(m, width=None, height=550, returned_objects=["last_object_clicked"])

with col2:
    st.subheader("🔥 Live Statistics")

    # Metrics
    total_cases = st.session_state.crime_data["Cases"].sum()
    critical_areas = len(st.session_state.crime_data[st.session_state.crime_data["Threat"] == "Critical"])

    st.metric("Total Alerts Today", f"{total_cases}", "+23")
    st.metric("Critical Zones", f"{critical_areas}", "Needs Raid")
    st.metric("Top Scam", "Aviator Betting", "56% Cases")

    st.markdown("---")
    st.markdown("#### 🚨 Top Hotspots")

    # Sorted by cases
    sorted_df = st.session_state.crime_data.sort_values("Cases", ascending=False)

    for idx, row in sorted_df.iterrows():
        if row["Threat"] == "Critical":
            st.error(f"**{row['Area']}**\n{row['Cases']} cases - {row['Crime']}")
        elif row["Threat"] == "High":
            st.warning(f"**{row['Area']}**\n{row['Cases']} cases - {row['Crime']}")
        else:
            st.info(f"**{row['Area']}**\n{row['Cases']} cases")

    st.caption(f"🕐 Last Updated: {datetime.now().strftime('%d %b %Y, %I:%M %p')}")

# ==================== FOOTER ====================
st.markdown("---")
col3, col4, col5 = st.columns(3)
with col3:
    st.success("✅ **100% Anonymous** - No personal data collected")
with col4:
    st.info("📊 **Data Source**: Student Intelligence Network")
with col5:
    st.warning("⚠️ **For Official Use** - Kakinada Cyber Police")

# ==================== CHAT SIMULATOR - DEMO KE ====================
with st.expander("🧪 Demo: Add New Alert - Test Chesei"):
    test_area = st.selectbox("Select Area", st.session_state.crime_data["Area"].tolist())
    test_crime = st.selectbox("Crime Type", ["Aviator Betting", "SBI KYC Scam", "Nude Call", "Loan App"])

    if st.button("➕ Add Alert to Map"):
        # Update count
        idx = st.session_state.crime_data[st.session_state.crime_data["Area"] == test_area].index[0]
        st.session_state.crime_data.loc[idx, "Cases"] += 1

        # Update threat level
        new_cases = st.session_state.crime_data.loc[idx, "Cases"]
        if new_cases > 30:
            st.session_state.crime_data.loc[idx, "Threat"] = "Critical"
        elif new_cases > 15:
            st.session_state.crime_data.loc[idx, "Threat"] = "High"

        st.success(f"Alert Added! {test_area} lo case count penchindi. Map refresh chey.")
        st.rerun()
