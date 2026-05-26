import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Cyber Kavacham AP",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
.main {background-color: #0E1117;}
.block-container {padding-top: 1rem;}
    h1 {color: #00D4FF; text-align: center; font-family: 'Arial Black';
        text-shadow: 0 0 10px #00D4FF, 2px 2px 4px #000000; margin-bottom: 0;}
    h3 {color: #FAFAFA; text-align: center; margin-top: 0;}
.stButton>button {
        background: linear-gradient(90deg, #00D4FF 0%, #0099CC 100%);
        color: white; border-radius: 10px; border: none;
        padding: 0.5rem 1rem; font-weight: bold;
        box-shadow: 0 4px 6px rgba(0, 212, 255, 0.3);
    }
    [data-testid="stMetricValue"] {color: #00D4FF; font-size: 28px;}
</style>
""", unsafe_allow_html=True)

# --- DATA: 26 AP DISTRICTS/CITIES ---
if 'crime_data' not in st.session_state:
    st.session_state.crime_data = pd.DataFrame({
        "District": [
            "Srikakulam", "Vizianagaram", "Visakhapatnam", "Alluri Sitharama Raju", "Anakapalli", 
            "Kakinada", "East Godavari", "Konaseema", "Eluru", "West Godavari", 
            "NTR", "Krishna", "Vijayawada", "Palnadu", "Guntur", 
            "Bapatla", "Prakasam", "Nellore", "Tirupati", "Chittoor", 
            "Annamayya", "Kadapa", "Anantapur", "Sri Sathya Sai", "Kurnool", "Nandyal"
        ],
        "Lat": [
            18.2969, 18.1067, 17.6869, 17.9339, 17.6910,
            16.9891, 17.0005, 16.5600, 16.7107, 16.8168,
            16.5734, 16.1750, 16.5062, 16.2393, 16.3067,
            15.8889, 15.5007, 14.4426, 13.6288, 13.2172,
            14.1000, 14.4673, 14.6819, 14.1617, 15.8281, 15.4788
        ],
        "Lon": [
            83.8968, 83.3956, 83.2185, 82.0230, 83.0037,
            82.2475, 81.8040, 82.1500, 81.0953, 81.5214,
            80.3580, 80.9900, 80.6480, 80.0500, 80.4365,
            80.4700, 80.0500, 79.9865, 79.4192, 79.1003,
            79.0500, 78.8242, 77.6006, 77.7475, 78.0373, 78.4836
        ],
        "Crime": [
            "UPI Scam", "OTP Fraud", "Loan App Harassment", "Job Scam", "Aviator Betting",
            "Aviator Betting", "KYC Scam", "FedEx Scam", "Job Scam", "UPI Scam",
            "Loan App", "SBI KYC Scam", "SBI KYC Scam", "Betting", "FedEx Scam",
            "Nude Call", "Loan App", "Aviator Betting", "Nude Call Blackmail", "Job Scam",
            "OTP Fraud", "Nude Call", "Betting", "UPI Scam", "Loan App", "KYC Scam"
        ],
        "Cases": [
            25, 14, 62, 18, 29, 47, 36, 21, 33, 19,
            28, 41, 55, 16, 43, 12, 24, 28, 31, 22,
            15, 17, 22, 11, 19, 13
        ],
        "Threat": [
            "High", "Medium", "Critical", "Medium", "High",
            "Critical", "High", "Medium", "High", "Medium",
            "High", "Critical", "Critical", "Medium", "Critical",
            "Medium", "High", "High", "High", "Medium",
            "Medium", "Medium", "Medium", "Medium", "Medium", "Medium"
        ]
    })

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Namaste! Nenu **Kavacham AI**. Meeku cyber crime nunchi rakshana kavali ante adagandi. Ex: 'Aviator safe aa?' or 'Phishing link check chey'"}]

# --- HEADER WITH LOGO - 100% SAFE ---
col_logo, col_title = st.columns([1, 6])
with col_logo:
    try:
        st.image("kavacham_logo.png", width=120)
    except:
        st.markdown("## 🛡️") # Logo file lekapothe emoji
with col_title:
    st.title("CYBER KAVACHAM AP")
    st.markdown("### Andhra Pradesh Digital Shield | Google Maps View + 26 Districts")
st.markdown("---")

# --- DISTRICT FILTER ---
col_filter1, col_filter2 = st.columns([2,3])
with col_filter1:
    district_list = ["All Districts - AP"] + sorted(st.session_state.crime_data["District"].tolist())
    selected_district = st.selectbox("📍 District/City Select Chey:", district_list)

if selected_district == "All Districts - AP":
    map_data = st.session_state.crime_data
    map_center = [15.9129, 79.7400]
    map_zoom = 7
else:
    map_data = st.session_state.crime_data[st.session_state.crime_data["District"] == selected_district]
    map_center = [map_data.iloc[0]["Lat"], map_data.iloc[0]["Lon"]]
    map_zoom = 11

with col_filter2:
    st.info(f"**Protected Area:** {selected_district} | **Active Threats:** {map_data['Cases'].sum()}")

# --- MAP + STATS ---
col1, col2 = st.columns([3, 1.2])

with col1:
    st.subheader("🗺️ Kavacham Google Map - Live Threats")
    
    m = folium.Map(location=map_center, zoom_start=map_zoom, control_scale=True)
    
    folium.TileLayer(
        tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
        attr='Google', name='Google Hybrid', overlay=False, control=True
    ).add_to(m)
    
    folium.TileLayer(
        tiles='https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
        attr='Google', name='Google Streets', overlay=False, control=True
    ).add_to(m)
    
    folium.TileLayer(tiles='CartoDB dark_matter', name='Dark Mode', overlay=False, control=True).add_to(m)

    for idx, row in map_data.iterrows():
        color_map = {"Critical": "#FF0000", "High": "#FF6B00", "Medium": "#FFD700", "Low": "#00D4FF"}
        color = color_map.get(row["Threat"], "blue")
        
        popup_html = f"""
        <div style="font-family: Arial; width: 220px;">
            <h4 style="color: #00D4FF; margin: 0;">🛡️ {row['District']}</h4>
            <hr style="margin: 5px 0;">
            <b>Top Threat:</b> {row['Crime']}<br>
            <b>Reports:</b> {row['Cases']} cases<br>
            <b>Risk Level:</b> <span style="color: {color}; font-weight: bold;">{row['Threat']}</span><br>
            <small>Kavacham Updated: {datetime.now().strftime('%d %b, %I:%M %p')}</small><br>
            <a href="tel:1930" style="color:#FF4B4B;">📞 Report: 1930</a>
        </div>
        """
        
        folium.CircleMarker(
            location=[row["Lat"], row["Lon"]], radius=max(10, row["Cases"]/1.5),
            popup=folium.Popup(popup_html, max_width=250),
            color=color, fill=True, fill_color=color, fill_opacity=0.7, weight=3
        ).add_to(m)

    folium.LayerControl(position='topright').add_to(m)
    st_folium(m, width=None, height=550, key="kavacham_map")
    st.caption("👆 Map lo red dot nokkite popup vastundi | Right-top lo Layers maarchuko")

with col2:
    st.subheader("🔥 Kavacham Stats")
    total_cases = map_data["Cases"].sum()
    critical_districts = len(map_data[map_data["Threat"] == "Critical"])
    st.metric("Total Threats", f"{total_cases}")
    st.metric("Critical Zones", f"{critical_districts}")
    st.metric("Top Threat", map_data.sort_values("Cases", ascending=False).iloc[0]["Crime"])
    
    st.markdown("---")
    st.markdown("#### 🚨 High Risk Districts")
    for idx, row in map_data.sort_values("Cases", ascending=False).head(8).iterrows():
        if row["Threat"] == "Critical": st.error(f"**{row['District']}**: {row['Cases']} cases")
        elif row["Threat"] == "High": st.warning(f"**{row['District']}**: {row['Cases']} cases")
        else: st.info(f"**{row['District']}**: {row['Cases']} cases")

st.markdown("---")

# --- AI CHAT + PHISHIELD ---
tab1, tab2, tab3 = st.tabs(["🤖 Kavacham AI Assistant", "🛡️ Phishield Scanner", "🧪 Demo: Add Threat"])

with tab1:
    st.subheader("Student ki Digital Rakshana")
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Aviator betting safe aa?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        response = ""
        prompt_lower = prompt.lower()
        if "aviator" in prompt_lower or "betting" in prompt_lower:
            response = "🚨 **KAVACHAM ALERT: Aviator 100% Scam!**\n\n1. Idhi gambling. Money pothundi.\n2. **1930** ki call cheyandi.\n3. App delete cheyandi. **Kavacham meeku shield.**"
        elif "nude call" in prompt_lower or "blackmail" in prompt_lower:
            response = "🛡️ **Kavacham Protection:**\n\n1. **Bayapadakandi.**\n2. **Money pampoddu.**\n3. **Proofs save cheyandi.**\n4. **1930 / cybercrime.gov.in** lo complaint petandi."
        elif "kyc" in prompt_lower or "sbi" in prompt_lower or "otp" in prompt_lower:
            response = "⚠️ **Kavacham Scan: KYC Scam!**\n\n1. Bank link meeda KYC adagadu.\n2. **OTP cheppoddu.**\n3. Direct Bank ki vellandi."
        elif "loan app" in prompt_lower:
            response = "💰 **Kavacham Warning: Fake Loan App!**\n\n1. Contacts access ivvakandi.\n2. **RBI approved apps matrame** vadandi.\n3. Harass cheste **1930** ki call."
        else:
            response = "Nenu **Kavacham AI** ni. 'Aviator', 'KYC Scam', 'Nude Call' adagandi. Ledha 'Phishield' lo link scan cheyandi."
        
        with st.chat_message("assistant"): st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

with tab2:
    st.subheader("🛡️ Phishield - Scam Link Scanner")
    url_to_check = st.text_input("Link paste chey:", placeholder="http://sbikyc-update.com")
    if st.button("🔍 Kavacham Scan", use_container_width=True):
        if url_to_check:
            suspicious_keywords = ['kyc', 'update', 'verify', 'bank', 'prize', 'lottery', 'free', 'bit.ly', '.xyz', '.tk']
            is_suspicious = any(keyword in url_to_check.lower() for keyword in suspicious_keywords)
            
            if is_suspicious or not url_to_check.startswith("https"):
                st.error("🚨 **KAVACHAM BLOCKED: Danger Scam Link!**\n\n**DO NOT CLICK.** Kavacham meeku shield vesindi.")
            else:
                st.success("✅ **Kavacham Verified: Safe ga undochu.**\n\nKani Bank app lone login avvandi.")
        else:
            st.warning("Link enter chey mawa.")

with tab3:
    st.subheader("🧪 Demo: New Threat Add Chey")
    test_district = st.selectbox("District", st.session_state.crime_data["District"].tolist())
    test_crime = st.selectbox("Crime Type", ["Aviator Betting", "SBI KYC Scam", "Nude Call", "Loan App Harassment", "Job Scam"])
    if st.button("➕ Add Threat"):
        idx = st.session_state.crime_data[st.session_state.crime_data["District"] == test_district].index[0]
        st.session_state.crime_data.loc[idx, "Cases"] += 1
        new_cases = st.session_state.crime_data.loc[idx, "Cases"]
        if new_cases > 50: st.session_state.crime_data.loc[idx, "Threat"] = "Critical"
        elif new_cases > 30: st.session_state.crime_data.loc[idx, "Threat"] = "High"
        st.success(f"Kavacham Updated! {test_district} lo threat penchindi.")
        st.rerun()

# --- FOOTER ---
st.markdown("---")
col3, col4, col5 = st.columns(3)
with col3: st.success("✅ **100% Anonymous Shield**")
with col4: st.info("📊 **Powered by Student Network**")
with col5: st.warning("⚠️ **Official Use** - AP Cyber Police")
