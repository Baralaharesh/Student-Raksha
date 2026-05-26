import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

st.set_page_config(
    page_title="Cyber Kavacham AP",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- SIMPLE CSS - NO ANIMATION ---
st.markdown("""
<style>
.stApp { background-color: #0E1117; }
.block-container {padding: 1rem 0.5rem;}
h1 {color: #00D4FF; text-align: center; font-weight: 900; margin-bottom: 0;}
h3 {color: #FAFAFA; text-align: center; margin-top: 0;}
.stButton>button {
    background-color: #00D4FF;
    color: #0E1117;
    border-radius: 8px;
    border: none;
    padding: 0.5rem 1rem;
    font-weight: bold;
    width: 100%;
}
[data-testid="stMetricValue"] {color: #00FF88; font-size: 28px;}
.stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
    background-color: #00D4FF;
    color: #0E1117;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# --- EMAIL FUNCTION ---
def send_mail_alert(subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = st.secrets["email"]["sender"]
        msg['To'] = st.secrets["email"]["receiver"]
        msg['Subject'] = f"🚨 KAVACHAM ALERT: {subject}"
        msg.attach(MIMEText(body, 'html'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(st.secrets["email"]["sender"], st.secrets["email"]["password"])
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        st.error(f"Mail Error: {e}")
        return False

# --- DATA: 26 AP DISTRICTS ---
if 'crime_data' not in st.session_state:
    st.session_state.crime_data = pd.DataFrame({
        "District": ["Srikakulam", "Vizianagaram", "Visakhapatnam", "Alluri Sitharama Raju", "Anakapalli", "Kakinada", "East Godavari", "Konaseema", "Eluru", "West Godavari", "NTR", "Krishna", "Vijayawada", "Palnadu", "Guntur", "Bapatla", "Prakasam", "Nellore", "Tirupati", "Chittoor", "Annamayya", "Kadapa", "Anantapur", "Sri Sathya Sai", "Kurnool", "Nandyal"],
        "Lat": [18.2969, 18.1067, 17.6869, 17.9339, 17.6910, 16.9891, 17.0005, 16.5600, 16.7107, 16.8168, 16.5734, 16.1750, 16.5062, 16.2393, 16.3067, 15.8889, 15.5007, 14.4426, 13.6288, 13.2172, 14.1000, 14.4673, 14.6819, 14.1617, 15.8281, 15.4788],
        "Lon": [83.8968, 83.3956, 83.2185, 82.0230, 83.0037, 82.2475, 81.8040, 82.1500, 81.0953, 81.5214, 80.3580, 80.9900, 80.6480, 80.0500, 80.4365, 80.4700, 80.0500, 79.9865, 79.4192, 79.1003, 79.0500, 78.8242, 77.6006, 77.7475, 78.0373, 78.4836],
        "Crime": ["UPI Scam", "OTP Fraud", "Loan App Harassment", "Job Scam", "Aviator Betting", "Aviator Betting", "KYC Scam", "FedEx Scam", "Job Scam", "UPI Scam", "Loan App", "SBI KYC Scam", "SBI KYC Scam", "Betting", "FedEx Scam", "Nude Call", "Loan App", "Aviator Betting", "Nude Call Blackmail", "Job Scam", "OTP Fraud", "Nude Call", "Betting", "UPI Scam", "Loan App", "KYC Scam"],
        "Cases": [25, 14, 62, 18, 29, 47, 36, 21, 33, 19, 28, 41, 55, 16, 43, 12, 24, 28, 31, 22, 15, 17, 22, 11, 19, 13],
        "Threat": ["High", "Medium", "Critical", "Medium", "High", "Critical", "High", "Medium", "High", "Medium", "High", "Critical", "Critical", "Medium", "Critical", "Medium", "High", "High", "High", "Medium", "Medium", "Medium", "Medium", "Medium", "Medium", "Medium"]
    })

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Namaste! Nenu **Kavacham AI**. Meeku cyber crime nunchi rakshana kavali ante adagandi."}]

# --- HEADER ---
col_logo, col_title = st.columns([1, 6])
with col_logo:
    try:
        st.image("kavacham_logo.png", width=100)
    except:
        st.markdown("## 🛡️")
with col_title:
    st.title("CYBER KAVACHAM AP")
    st.markdown("### Andhra Pradesh Digital Shield | Live Threat Intelligence")
st.markdown("---")

# --- DISTRICT FILTER ---
col_filter1, col_filter2 = st.columns([2,3])
with col_filter1:
    district_list = ["All Districts - AP"] + sorted(st.session_state.crime_data["District"].tolist())
    selected_district = st.selectbox("📍 District:", district_list)

if selected_district == "All Districts - AP":
    map_data = st.session_state.crime_data
    map_center = [15.9129, 79.7400]
    map_zoom = 6
else:
    map_data = st.session_state.crime_data[st.session_state.crime_data["District"] == selected_district]
    map_center = [map_data.iloc[0]["Lat"], map_data.iloc[0]["Lon"]]
    map_zoom = 10

with col_filter2:
    st.info(f"**Area:** {selected_district} | **Threats:** {map_data['Cases'].sum()}")

# --- MAP + STATS ---
col1, col2 = st.columns([3, 1.2])

with col1:
    st.subheader("🗺️ Kavacham Map")
    m = folium.Map(location=map_center, zoom_start=map_zoom, control_scale=True)

    folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google', name='Hybrid').add_to(m)
    folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}', attr='Google', name='Streets').add_to(m)
    folium.TileLayer(tiles='CartoDB dark_matter', name='Dark').add_to(m)

    for idx, row in map_data.iterrows():
        color_map = {"Critical": "#FF0066", "High": "#FF6B00", "Medium": "#FFD700", "Low": "#00D4FF"}
        color = color_map.get(row["Threat"], "blue")
        popup_html = f"""<div style="font-family: Arial; width: 200px; background: #0E1117; color: white; padding: 8px; border-radius: 8px;"><h4 style="color: #00D4FF; margin: 0;">🛡️ {row['District']}</h4><hr style="margin: 5px 0; border-color: #00D4FF;"><b>Threat:</b> {row['Crime']}<br><b>Cases:</b> {row['Cases']}<br><b>Risk:</b> <span style="color: {color}; font-weight: bold;">{row['Threat']}</span><br><a href="tel:1930" style="color:#FF4B4B;">📞 1930</a></div>"""
        folium.CircleMarker(location=[row["Lat"], row["Lon"]], radius=max(8, row["Cases"]/2), popup=folium.Popup(popup_html, max_width=200), color=color, fill=True, fill_color=color, fill_opacity=0.7, weight=2).add_to(m)

    folium.LayerControl(position='topright').add_to(m)
    st_folium(m, width=None, height=400, key="kavacham_map")

with col2:
    st.subheader("🔥 Stats")
    st.metric("Total Threats", f"{map_data['Cases'].sum()}")
    st.metric("Critical Zones", f"{len(map_data[map_data['Threat'] == 'Critical'])}")
    st.metric("Top Threat", map_data.sort_values("Cases", ascending=False).iloc[0]["Crime"])

st.markdown("---")

# --- TABS ---
tab1, tab2, tab3 = st.tabs(["🤖 AI Assistant", "🛡️ Phishield", "🧪 Demo + Mail"])

with tab1:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Aviator safe aa?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        prompt_lower = prompt.lower()
        if "aviator" in prompt_lower: response = "🚨 **KAVACHAM ALERT: Aviator 100% Scam!** Money pothundi. **1930** ki call cheyandi."
        elif "nude call" in prompt_lower: response = "🛡️ **Protection:** 1.Bayapadakandi 2.Money pampoddu 3.**1930** lo complaint"
        elif "kyc" in prompt_lower or "otp" in prompt_lower: response = "⚠️ **KYC Scam!** Bank link adagadu. **OTP cheppoddu.**"
        elif "loan app" in prompt_lower: response = "💰 **Fake Loan App!** Contacts ivvakandi. **RBI approved** matrame."
        else: response = "Nenu **Kavacham AI** ni. 'Aviator', 'KYC Scam' adagandi."
        with st.chat_message("assistant"): st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

with tab2:
    st.subheader("🛡️ Scam Link Scanner")
    url_to_check = st.text_input("Link:", placeholder="http://sbikyc-update.com")
    if st.button("🔍 Scan", use_container_width=True):
        if url_to_check:
            suspicious = ['kyc', 'update', 'verify', 'bank', 'prize', 'bit.ly', '.xyz']
            is_suspicious = any(k in url_to_check.lower() for k in suspicious)
            if is_suspicious or not url_to_check.startswith("https"):
                st.error("🚨 **DANGER! Scam Link! DO NOT CLICK.**")
                mail_body = f"<h3>Phishield Alert</h3><p><b>Scam Link Detected:</b> {url_to_check}</p><p><b>Time:</b> {datetime.now().strftime('%d-%m-%Y %I:%M %p')}</p>"
                if send_mail_alert("Scam Link Detected", mail_body):
                    st.success("Backend ki mail vellindi ✅")
            else:
                st.success("✅ Safe ga undochu.")
        else:
            st.warning("Link enter chey.")

with tab3:
    st.subheader("🧪 Demo: Add Threat + Mail Alert")
    test_district = st.selectbox("District", st.session_state.crime_data["District"].tolist())
    test_crime = st.selectbox("Crime", ["Aviator Betting", "SBI KYC Scam", "Nude Call", "Loan App Harassment"])
    if st.button("➕ Add Threat & Send Mail", use_container_width=True):
        idx = st.session_state.crime_data[st.session_state.crime_data["District"] == test_district].index[0]
        st.session_state.crime_data.loc[idx, "Cases"] += 1
        new_cases = st.session_state.crime_data.loc[idx, "Cases"]
        if new_cases > 50: st.session_state.crime_data.loc[idx, "Threat"] = "Critical"
        elif new_cases > 30: st.session_state.crime_data.loc[idx, "Threat"] = "High"

        mail_body = f"""<h3>New Threat Added - Kavacham</h3><p><b>District:</b> {test_district}</p><p><b>Crime:</b> {test_crime}</p><p><b>Total Cases:</b> {new_cases}</p><p><b>Time:</b> {datetime.now().strftime('%d-%m-%Y %I:%M %p')}</p><p><b>Action:</b> Check dashboard immediately</p>"""
        if send_mail_alert(f"New Threat: {test_district}", mail_body):
            st.success(f"Kavacham Updated! Mail sent to hareeshbarla2@gmail.com ✅")
        st.rerun()

# --- FOOTER ---
st.markdown("---")
col3, col4, col5 = st.columns(3)
with col3: st.success("✅ Anonymous")
with col4: st.info("📊 Student Network")
with col5: st.warning("⚠️ AP Police")
