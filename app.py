import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
from datetime import datetime
import re

st.set_page_config(
    page_title="Raksha AP Cyber Command V5.1",
    page_icon="🚔",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
.main {background-color: #0E1117;}
.block-container {padding-top: 1rem;}
    h1 {color: #FF4B4B; text-align: center; font-family: 'Arial Black';
        text-shadow: 2px 2px 4px #000000;}
    h3 {color: #FAFAFA; text-align: center;}
.stButton>button {
        background: linear-gradient(90deg, #FF4B4B 0%, #FF6B6B 100%);
        color: white; border-radius: 10px; border: none;
        padding: 0.5rem 1rem; font-weight: bold;
        box-shadow: 0 4px 6px rgba(255, 75, 0.3);
    }
    [data-testid="stMetricValue"] {color: #FF4B4B; font-size: 28px;}
</style>
""", unsafe_allow_html=True)

# --- DATA ---
if 'crime_data' not in st.session_state:
    st.session_state.crime_data = pd.DataFrame({
        "District": ["Kakinada", "Visakhapatnam", "Vijayawada", "Tirupati", "Guntur", "Nellore", "Kurnool", "Rajamahendravaram", "Anantapur", "Kadapa", "Srikakulam", "Vizianagaram", "Eluru"],
        "Lat": [16.9891, 17.6869, 16.5062, 13.6288, 16.3067, 14.4426, 15.8281, 17.0005, 14.6819, 14.4673, 18.2969, 18.1067, 16.7107],
        "Lon": [82.2475, 83.2185, 80.6480, 79.4192, 80.4365, 79.9865, 78.0373, 81.8040, 77.6006, 78.8242, 83.8968, 83.3956, 81.0953],
        "Crime": ["Aviator Betting", "Loan App Harassment", "SBI KYC Scam", "Nude Call Blackmail", "FedEx Scam", "Aviator Betting", "Loan App", "KYC Scam", "Betting", "Nude Call", "UPI Scam", "OTP Fraud", "Job Scam"],
        "Cases": [47, 62, 55, 31, 43, 28, 19, 36, 22, 17, 25, 14, 33],
        "Threat": ["Critical", "Critical", "Critical", "High", "Critical", "High", "Medium", "High", "Medium", "Medium", "High", "Medium", "High"]
    })

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Namaste! Nenu Raksha AI. Meeku cyber crime gurinchi em sahayam kavalanna adagandi. Ex: 'Aviator safe aa?' or 'Phishing link check chey'"}]

# --- HEADER ---
st.title("🚔 RAKSHA AP CYBER COMMAND CENTER V5.1")
st.markdown("### AP State Live Intelligence | Satellite View + AI Chat + Phishield")
st.markdown("---")

# --- FEATURE 1: DISTRICT FILTER ---
col_filter1, col_filter2 = st.columns([2,3])
with col_filter1:
    district_list = ["All Districts - AP"] + sorted(st.session_state.crime_data["District"].tolist())
    selected_district = st.selectbox("📍 District Filter Chey:", district_list)

# Filter data based on selection
if selected_district == "All Districts - AP":
    map_data = st.session_state.crime_data
    map_center = [15.9129, 79.7400]
    map_zoom = 7
else:
    map_data = st.session_state.crime_data[st.session_state.crime_data["District"] == selected_district]
    map_center = [map_data.iloc[0]["Lat"], map_data.iloc[0]["Lon"]]
    map_zoom = 11

with col_filter2:
    st.info(f"**Showing:** {selected_district} | **Active Alerts:** {map_data['Cases'].sum()}")

# --- MAP + STATS ---
col1, col2 = st.columns([3, 1.2])

with col1:
    st.subheader("🛰️ AP State Scam Hotspot Map - Satellite View")
    
    # NEW: SATELLITE MAP WITH LAYER CONTROL
    m = folium.Map(location=map_center, zoom_start=map_zoom, control_scale=True)
    
    # Layer 1: Satellite - Default
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='Satellite View',
        overlay=False,
        control=True
    ).add_to(m)
    
    # Layer 2: Street Map
    folium.TileLayer(
        tiles='OpenStreetMap',
        name='Street Map',
        overlay=False,
        control=True
    ).add_to(m)
    
    # Layer 3: Dark Mode - For Night Ops
    folium.TileLayer(
        tiles='CartoDB dark_matter',
        name='Dark Mode',
        overlay=False,
        control=True
    ).add_to(m)

    for idx, row in map_data.iterrows():
        color_map = {"Critical": "#FF0000", "High": "#FF6B00", "Medium": "#FFD700", "Low": "#90EE90"}
        color = color_map.get(row["Threat"], "blue")
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
            location=[row["Lat"], row["Lon"]], radius=max(8, row["Cases"]/2),
            popup=folium.Popup(popup_html, max_width=250), color=color, fill=True,
            fill_color=color, fill_opacity=0.8, weight=3
        ).add_to(m)
        folium.Marker(
            [row["Lat"], row["Lon"]],
            icon=folium.DivIcon(html=f"""<div style="font-size: 11pt; color: white;
            text-shadow: 2px 2px 4px black; font-weight: bold;">{row['District']}</div>""")
        ).add_to(m)

    # Add Layer Control - Right side lo icon vastundi
    folium.LayerControl(position='topright').add_to(m)
    
    st_data = st_folium(m, width=None, height=550, returned_objects=["last_object_clicked"])
    st.caption("👆 Map right-top corner lo 'Layers' icon nokki Satellite/Street/Dark maarchuko")

with col2:
    st.subheader("🔥 Live Statistics")
    total_cases = map_data["Cases"].sum()
    critical_districts = len(map_data[map_data["Threat"] == "Critical"])
    st.metric("Total Alerts", f"{total_cases}")
    st.metric("Critical Districts", f"{critical_districts}")
    st.metric("Top Scam", map_data.sort_values("Cases", ascending=False).iloc[0]["Crime"])
    
    st.markdown("---")
    st.markdown("#### 🚨 Hotspots")
    for idx, row in map_data.sort_values("Cases", ascending=False).head(5).iterrows():
        if row["Threat"] == "Critical": st.error(f"**{row['District']}**: {row['Cases']} cases")
        elif row["Threat"] == "High": st.warning(f"**{row['District']}**: {row['Cases']} cases")
        else: st.info(f"**{row['District']}**: {row['Cases']} cases")

st.markdown("---")

# --- FEATURE 2 & 3: AI CHAT BOT + PHISHIELD ---
tab1, tab2, tab3 = st.tabs(["🤖 Raksha AI Chat Bot", "🛡️ Phishield - Link Checker", "🧪 Demo: Add Alert"])

with tab1:
    st.subheader("Student ki Instant Help - AI Chat Bot")
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Aviator betting safe aa? Nude call vaste em cheyali?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        response = ""
        prompt_lower = prompt.lower()
        if "aviator" in prompt_lower or "betting" in prompt_lower:
            response = "🚨 **ALERT: Aviator 100% Scam!**\n\n1. Idhi gambling, not investment. Mee money motham potundi.\n2. Police ki report cheyandi: 1930 ki call cheyandi.\n3. App delete cheyandi, bank details share cheyoddu.\n\n**Mee district lo ippatike cases unnay.**"
        elif "nude call" in prompt_lower or "blackmail" in prompt_lower:
            response = "🛡️ **Nude Call Blackmail - Ventane Cheyalsina Pani:**\n\n1. **Bayapadakandi.** Veellu screenshots tho bendhistaru.\n2. **Money pampoddu.** Okasari pampithe aaparu.\n3. **Proofs Save Cheyandi:** Screenshots, numbers.\n4. **1930 / cybercrime.gov.in** lo complaint petandi.\n5. **Mee daggara PS lo Women Cell** ki vellandi."
        elif "kyc" in prompt_lower or "sbi" in prompt_lower or "otp" in prompt_lower:
            response = "⚠️ **SBI KYC / OTP Scam Alert!**\n\nBank eppudu Phone/Link meeda KYC adagadu.\n1. **Link click cheyoddu.**\n2. **OTP evariki cheppoddu.**\n3. Doubt unte, **direct Bank branch ki vellandi.**"
        elif "loan app" in prompt_lower:
            response = "💰 **Fake Loan App Danger!**\n\n1. Veellu contacts, gallery access adugutaru. Ivvakandi.\n2. High interest, harassment start chestaru.\n3. **RBI approved apps matrame** vadandi.\n4. Harass cheste 1930 ki complaint."
        else:
            response = "Nenu cyber crime expert ni. 'Aviator', 'KYC Scam', 'Nude Call', 'Loan App' lanti words tho adagandi. Ledha 'Phishield' tab lo link check cheskondi."
        
        with st.chat_message("assistant"): st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

with tab2:
    st.subheader("🛡️ Phishield - Scam Link Check Chey")
    url_to_check = st.text_input("Anumanam ga unna Link/URL ikkada paste chey:", placeholder="http://sbikyc-update-verify.com")
    if st.button("🔍 Scan Now", use_container_width=True):
        if url_to_check:
            suspicious_keywords = ['kyc', 'update', 'verify', 'bank', 'prize', 'lottery', 'free', 'gift', 'bit.ly', '.xyz', '.tk', 'login']
            is_suspicious = any(keyword in url_to_check.lower() for keyword in suspicious_keywords)
            
            st.markdown("---")
            if is_suspicious or not url_to_check.startswith("https"):
                st.error("🚨 **DANGER: Ee Link 99% Scam/Fake!**")
                st.markdown("""
                **Reasons:**
                1. Bank/Govt websites `https` tho start avuthai. Idi ledu.
                2. `kyc`, `update`, `verify` lanti words scam links lo untai.
                3. **Click cheyoddu. Mee details enter cheyoddu.**
                """)
            else:
                st.success("✅ **Safe ga undochu.** Kani 100% guarantee ledu.")
                st.info("Bank link ayina sare, direct ga Bank app/website lone login avvandi. SMS lo vache links nammakandi.")
        else:
            st.warning("Link enter chey mawa.")

with tab3:
    st.subheader("🧪 Demo: New Alert Add Chey")
    test_district = st.selectbox("Select District", st.session_state.crime_data["District"].tolist())
    test_crime = st.selectbox("Crime Type", ["Aviator Betting", "SBI KYC Scam", "Nude Call", "Loan App Harassment", "Job Scam"])
    if st.button("➕ Add Alert to Map"):
        idx = st.session_state.crime_data[st.session_state.crime_data["District"] == test_district].index[0]
        st.session_state.crime_data.loc[idx, "Cases"] += 1
        new_cases = st.session_state.crime_data.loc[idx, "Cases"]
        if new_cases > 50: st.session_state.crime_data.loc[idx, "Threat"] = "Critical"
        elif new_cases > 30: st.session_state.crime_data.loc[idx, "Threat"] = "High"
        st.success(f"Alert Added! {test_district} lo case count {new_cases} aindi. Map refresh aipothundi.")
        st.rerun()

# --- FOOTER ---
st.markdown("---")
col3, col4, col5 = st.columns(3)
with col3: st.success("✅ **100% Anonymous**")
with col4: st.info("📊 **Data Source**: Student Network")
with col5: st.warning("⚠️ **For Official Use** - AP Cyber Police")
