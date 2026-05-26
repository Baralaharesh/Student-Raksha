import streamlit as st
from datetime import datetime
import re

st.set_page_config(page_title="Raksha Intelligence V3.1", page_icon="🚔", layout="wide")

# --- Session State - Live Data Simulation ---
if "total_cases" not in st.session_state:
    st.session_state.total_cases = 247
if "today_cases" not in st.session_state:
    st.session_state.today_cases = 18
if "district_stats" not in st.session_state:
    st.session_state.district_stats = {"Kakinada": 52, "Vizag City": 81, "Vijayawada": 43, "Guntur": 28, "Tirupati": 19, "Rajahmundry": 24}
if "blacklist" not in st.session_state:
    st.session_state.blacklist = {
        "9876543210": {"count": 14, "crime": "Aviator Scam", "act": "66D IT Act"},
        "9123456789": {"count": 8, "crime": "SBI KYC Scam", "act": "66C IT Act"},
        "9988776655": {"count": 21, "crime": "Nude Video Blackmail", "act": "66E, 67A IT Act"}
    }

# --- Scam Databases ---
BETTING_DOMAINS = ["aviator", "1xbet", "parimatch", "betway", "teen patti", "rummy", "dafabet", "rajabets", "stake", "winbuzz", "lotus365"]
PHISHING_KEYWORDS = ["sbi kyc", "bank link", "otp", "ekyc update", "electricity bill", "customer care", "fedex", "courier", "loan app"]
BLACKMAIL_KEYWORDS = ["photo morph", "nude", "video call", "naked", "personal photo", "blackmail", "instagram id hack"]

# --- District Wise Cyber PS Data ---
DISTRICT_PSS = {
    "Kakinada": {"phone": "0884-2345100", "address": "Cyber Crime PS, SP Office Complex, Kakinada"},
    "Rajahmundry": {"phone": "0883-2444444", "address": "Cyber Crime PS, Rajahmundry Urban"},
    "Vizag City": {"phone": "0891-2565454", "address": "Cyber Crime PS, Police Commissioner Office, Vizag"},
    "Vijayawada": {"phone": "0866-2497100", "address": "Cyber Crime PS, Vijayawada City"},
    "Guntur": {"phone": "0863-2234000", "address": "Cyber Crime PS, Guntur Urban"},
    "Tirupati": {"phone": "0877-2265000", "address": "Cyber Crime PS, Tirupati Urban"},
    "Other": {"phone": "1930", "address": "National Cyber Crime Helpline"}
}

# MP3 URL - Nee GitHub username marchuko
AUDIO_URL = "https://raw.githubusercontent.com/Baralaharesh/Student-Raksha/main/assets/warning.mp3"

def get_legal_advice(user_input, district):
    user_lower = user_input.lower()
    ps_info = DISTRICT_PSS.get(district, DISTRICT_PSS["Other"])
    show_audio = False

    # Update Live Stats - Every query = 1 case flagged
    st.session_state.total_cases += 1
    st.session_state.today_cases += 1
    st.session_state.district_stats[district] = st.session_state.district_stats.get(district, 0) + 1

    if any(domain in user_lower for domain in BETTING_DOMAINS):
        show_audio = True
        reply = f"""
**🚨 ILLEGAL BETTING APP DETECTED - HIGH RISK 🚨**

**Mee tappu emi ledu. Bayapadakandi.** Aviator, 1xBet lanti apps `Public Gambling Act` prakaram **ILLEGAL**.

**Legal Protection**: Ee apps promote chese vaallu `Telangana Gaming Act` prakaram **7 Years jail** ki vellachu.
"""

    elif any(word in user_lower for word in PHISHING_KEYWORDS):
        reply = f"""
**⚠️ BANK / KYC PHISHING SCAM ALERT ⚠️**

**Gurthunchukondi**: SBI / Police / FedEx eppudu link pampi OTP adagaru. Idi `Digital Arrest` Scam.

**Legal Action**: Mosam chese vaallaki `IT Act 66C & 66D` prakaram **3 Years Jail + 1 Lakh Fine**.
"""

    elif any(word in user_lower for word in BLACKMAIL_KEYWORDS):
        reply = f"""
**🛑 CYBER BLACKMAIL - SERIOUS CRIME 🛑**

**Modata Oka Maata**: **Tappu 100% aa criminal didi. Meedi kaadu.** Siggu padakandi.

**Legal Shield**: `IT Act 66E`: **3 Years Jail**. `IT Act 67A`: **5 Years Jail**.
"""

    else:
        reply = "Mee samasya naaku artham ayyindi. Konchem vivaranga cheppagalara? Screenshot unte upload cheyandi."

    reply += f"\n\n**Mee Local Police Station:**\n📍 **{ps_info['address']}**\n📞 **Phone: {ps_info['phone']}** | **1930 Toll-Free**"
    return reply, show_audio

# --- UI START ---
st.title("🚔 Raksha Intelligence Dashboard V3.1")
st.caption("Telangana State Police - Student Cyber Crime Intelligence Network")

# --- Element 1: Live Stats Dashboard ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("✅ Total Cases Flagged", st.session_state.total_cases, "Live")
col2.metric("🔴 Cases Today", st.session_state.today_cases, f"+{1}")
col3.metric(f"📍 {district if 'district' in locals() else 'Kakinada'}", st.session_state.district_stats.get(district if 'district' in locals() else 'Kakinada', 0))
col4.metric("☠️ Blacklisted Numbers", len(st.session_state.blacklist))
st.markdown("---")

# --- Two Column Layout ---
left_col, right_col = st.columns([2, 1])

with right_col:
    # --- Element 2: Blacklist Checker ---
    st.subheader("☠️ Criminal Number Checker")
    st.caption("Scammer number ikkada vesi verify cheyandi")
    check_number = st.text_input("Phone Number", placeholder="9876543210", label_visibility="collapsed")
    if st.button("Check Blacklist", use_container_width=True):
        if check_number in st.session_state.blacklist:
            data = st.session_state.blacklist[check_number]
            st.error(f"**DANGER**: +91-{check_number}")
            st.write(f"**Reported**: {data['count']} times")
            st.write(f"**Crime**: {data['crime']}")
            st.write(f"**Act**: {data['act']}")
            st.warning("Ee number ki dabbulu pampavaddu. Block cheyandi.")
        elif check_number and len(check_number) == 10:
            st.success(f"✅ +91-{check_number} database lo ledu")
            st.info("Kotha number aithe, report cheyadaniki chat lo pampandi.")
            # Add to blacklist for demo
            st.session_state.blacklist[check_number] = {"count": 1, "crime": "New Report by Student", "act": "Under Verification"}
        elif check_number:
            st.warning("Sari aina 10-digit number ivvandi")

with left_col:
    # --- District Selector ---
    district = st.selectbox(
        "📍 Mee District Select Cheyandi",
        options=list(DISTRICT_PSS.keys()),
        index=0
    )

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": f"Namaste! Nenu {district} district kosam unna Raksha Sir ni. Betting app, fake SBI link, blackmail lanti vati gurinchi cheppandi."}]

    # --- Chat Display ---
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "image" in message:
                st.image(message["image"], width=300)

    # --- Photo Upload ---
    uploaded_file = st.file_uploader("🖼️ Screenshot / Photo Upload Cheyandi", type=["jpg", "jpeg", "png"])

    # --- Chat Input ---
    if user_input := st.chat_input("Mee samasya ikkada type cheyandi..."):
        user_msg = {"role": "user", "content": user_input}
        if uploaded_file:
            user_msg["image"] = uploaded_file

        st.session_state.messages.append(user_msg)

        reply, show_audio = get_legal_advice(user_input, district)
        case_id = f"RS{datetime.now().strftime('%d%m%H%M%S')}"

        if uploaded_file:
            reply += "\n\n✅ **Evidence Receive Ayindi.**"

        reply += f"\n\n---\n**Mee Raksha Case ID: {case_id}** | **District: {district}**"

        with st.chat_message("assistant"):
            st.markdown(reply)

            # Audio Player
            if show_audio:
                st.error("🚨 Hetchharika! Kinda Police Warning vinu")
                st.audio(AUDIO_URL, format="audio/mp3")

        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()

st.markdown("---")
st.caption("For emergencies, dial 100 or 1930. | This is an AI intelligence dashboard for student safety.")
