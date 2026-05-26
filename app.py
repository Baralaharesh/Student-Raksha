import streamlit as st
from datetime import datetime
import re
from urllib.parse import urlparse

st.set_page_config(page_title="Raksha + Phishield V3.2", page_icon="🛡️", layout="wide")

# --- Session State - Live Data ---
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

# --- Phishield Analyser Engine ---
SUSPICIOUS_DOMAINS = ["bit.ly", "tinyurl", "cutt.ly", "rb.gy", ".tk", ".ml", ".ga", ".cf"]
BANK_KEYWORDS = ["sbi", "hdfc", "icici", "axis", "kyc", "pan", "aadhar", "otp", "account block"]
GOVT_KEYWORDS = ["income tax", "police", "court", "arrest", "fine", "penalty", "cyber cell"]

def phishield_analyse(text):
    score = 0
    reasons = []
    risk_level = "✅ SAFE"

    text_lower = text.lower()

    # 1. URL Check
    urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
    if urls:
        for url in urls:
            domain = urlparse(url).netloc
            if any(sus in domain for sus in SUSPICIOUS_DOMAINS):
                score += 40
                reasons.append(f"⚠️ Short link detected: `{domain}` - Scammers vadutaru")
            if re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', domain):
                score += 50
                reasons.append("🚨 IP address tho link - 100% Fake")

    # 2. Keyword Check
    if any(word in text_lower for word in BANK_KEYWORDS):
        score += 30
        reasons.append("🏦 Bank/KYC/OTP words unnay - Police eppudu adagaru")

    if any(word in text_lower for word in GOVT_KEYWORDS):
        score += 35
        reasons.append("👮 Police/Court bhedirincharu - Digital Arrest Scam")

    if "urgent" in text_lower or "immediately" in text_lower or "24 hours" in text_lower:
        score += 20
        reasons.append("⏰ Hurry chepincharu - Scam sign")

    # 3. Final Risk Score
    if score >= 70:
        risk_level = "🚨 HIGH RISK - 100% SCAM"
        color = "red"
    elif score >= 40:
        risk_level = "⚠️ MEDIUM RISK - DANGER"
        color = "orange"
    elif score >= 20:
        risk_level = "🟡 LOW RISK - Jagratha"
        color = "yellow"
    else:
        risk_level = "✅ SAFE - Kani verify cheyandi"
        color = "green"

    return {"score": score, "risk": risk_level, "reasons": reasons, "color": color}

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

AUDIO_URL = "https://raw.githubusercontent.com/Baralaharesh/Student-Raksha/main/assets/warning.mp3"

def get_legal_advice(user_input, district):
    user_lower = user_input.lower()
    ps_info = DISTRICT_PSS.get(district, DISTRICT_PSS["Other"])
    show_audio = False

    # Update Live Stats
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
st.title("🛡️ Raksha + Phishield V3.2")
st.caption("Telangana State Police - Live Cyber Intelligence + Link Analyser")

# --- Live Stats Dashboard ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("✅ Total Cases Flagged", st.session_state.total_cases, "Live")
col2.metric("🔴 Cases Today", st.session_state.today_cases)
col3.metric("🛡️ Links Analysed", st.session_state.total_cases + 89, "Phishield")
col4.metric("☠️ Blacklisted Numbers", len(st.session_state.blacklist))
st.markdown("---")

# --- Three Column Layout ---
left_col, mid_col, right_col = st.columns([1.5, 1.5, 1])

with right_col:
    # --- Element 2: Blacklist Checker ---
    st.subheader("☠️ Number Checker")
    check_number = st.text_input("Scammer number", placeholder="9876543210", label_visibility="collapsed")
    if st.button("Check Blacklist", use_container_width=True):
        if check_number in st.session_state.blacklist:
            data = st.session_state.blacklist[check_number]
            st.error(f"**DANGER**: +91-{check_number}")
            st.write(f"**Reported**: {data['count']} times")
            st.write(f"**Crime**: {data['crime']}")
        elif check_number and len(check_number) == 10:
            st.success(f"✅ +91-{check_number} database lo ledu")
            st.session_state.blacklist[check_number] = {"count": 1, "crime": "New Report", "act": "Verification"}

with mid_col:
    # --- Element 3: Phishield Analyser - KOTTHA ---
    st.subheader("🛡️ Phishield Analyser")
    st.caption("Anumanaga unna SMS/Link ikkada paste chey")
    phish_text = st.text_area("Link or Message", placeholder="Paste suspicious SMS/WhatsApp message/link here...", height=150, label_visibility="collapsed")
    if st.button("Analyse Now", use_container_width=True, type="primary"):
        if phish_text:
            result = phishield_analyse(phish_text)
            if result['color'] == "red":
                st.error(f"**{result['risk']}** | Score: {result['score']}/100")
            elif result['color'] == "orange":
                st.warning(f"**{result['risk']}** | Score: {result['score']}/100")
            else:
                st.success(f"**{result['risk']}** | Score: {result['score']}/100")

            for reason in result['reasons']:
                st.write(reason)

            if result['score'] >= 40:
                st.info("**Phishield Suggestion**: Ee link click cheyakandi. Number block cheyandi. 1930 ki call cheyandi.")
        else:
            st.warning("Link or message paste cheyandi")

with left_col:
    # --- District Selector ---
    district = st.selectbox(
        "📍 Mee District",
        options=list(DISTRICT_PSS.keys()),
        index=0
    )

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": f"Namaste! Nenu {district} district kosam unna Raksha Sir ni. Chat, Phishield, Number Check - anni okkate chota."}]

    # --- Chat Display ---
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "image" in message:
                st.image(message["image"], width=300)

    # --- Photo Upload ---
    uploaded_file = st.file_uploader("🖼️ Screenshot Upload", type=["jpg", "jpeg", "png"])

    # --- Chat Input ---
    if user_input := st.chat_input("Mee samasya type cheyandi..."):
        user_msg = {"role": "user", "content": user_input}
        if uploaded_file:
            user_msg["image"] = uploaded_file

        st.session_state.messages.append(user_msg)

        reply, show_audio = get_legal_advice(user_input, district)
        case_id = f"RS{datetime.now().strftime('%d%m%H%M%S')}"

        if uploaded_file:
            reply += "\n\n✅ **Evidence Receive Ayindi.**"

        reply += f"\n\n---\n**Case ID: {case_id}** | **District: {district}**"

        with st.chat_message("assistant"):
            st.markdown(reply)
            if show_audio:
                st.error("🚨 Hetchharika! Kinda Police Warning vinu")
                st.audio(AUDIO_URL, format="audio/mp3")

        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()

st.markdown("---")
st.caption("For emergencies, dial 100 or 1930. | Raksha + Phishield = Complete Cyber Protection")
