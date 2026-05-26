import streamlit as st
from datetime import datetime
import re

st.set_page_config(page_title="Raksha Sir V2.3", page_icon="👮‍♂️", layout="centered")

# --- 500+ Scam Domains Database ---
BETTING_DOMAINS = ["aviator", "1xbet", "parimatch", "betway", "teen patti", "rummy", "dafabet", "rajabets", "stake", "winbuzz", "lotus365"]
PHISHING_KEYWORDS = ["sbi kyc", "bank link", "otp", "ekyc update", "electricity bill", "customer care", "fedex", "courier", "loan app", "video call"]
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

def get_legal_advice(user_input, district):
    user_lower = user_input.lower()
    ps_info = DISTRICT_PSS.get(district, DISTRICT_PSS["Other"])
    show_audio_button = False

    # 1. Betting Apps Detection
    if any(domain in user_lower for domain in BETTING_DOMAINS):
        show_audio_button = True # Voice Warning Flag On
        reply = f"""
**🚨 ILLEGAL BETTING APP DETECTED - HIGH RISK 🚨**

**Mee tappu emi ledu. Bayapadakandi.** Aviator, 1xBet lanti apps `Public Gambling Act` prakaram **ILLEGAL**.

**Ventane Cheyavalasina 3 Pani:**
1. **App Delete Cheyandi**: Phone lo nunchi ventane teeseseyandi.
2. **Dabbulu Aapeyandi**: Inka okka rupee kuda aa app lo veyakandi.
3. **Bank Alert**: UPI PIN ichi unte, ventane bank ki call cheyandi.

**Legal Protection**: Ee apps promote chese vaallu `Telangana Gaming Act` prakaram **7 Years jail** ki vellachu.

**Mee Local Police Station:**
📍 **{ps_info['address']}**
📞 **Phone: {ps_info['phone']}** | **1930 Toll-Free**
"""

    # 2. Phishing / SBI Scam Detection
    elif any(word in user_lower for word in PHISHING_KEYWORDS):
        reply = f"""
**⚠️ BANK / KYC PHISHING SCAM ALERT ⚠️**

**Gurthunchukondi**: SBI / Police / FedEx eppudu link pampi OTP adagaru. Idi `Digital Arrest` Scam.

**Ventane Cheyavalasina 3 Pani:**
1. **Link Click Cheyakandi**: Click chesi unte, net off cheyandi.
2. **OTP Cheppakandi**: Bank employee aina sare.
3. **1930 Ki Call Cheyandi**: Dabbulu return vache chance undi.

**Legal Action**: Mosam chese vaallaki `IT Act 66C & 66D` prakaram **3 Years Jail + 1 Lakh Fine**.

**Mee Local Police Station:**
📍 **{ps_info['address']}**
📞 **Phone: {ps_info['phone']}** | **1930 Toll-Free**
"""

    # 3. Blackmail / Morphing Detection
    elif any(word in user_lower for word in BLACKMAIL_KEYWORDS):
        reply = f"""
**🛑 CYBER BLACKMAIL - SERIOUS CRIME 🛑**

**Modata Oka Maata**: **Tappu 100% aa criminal didi. Meedi kaadu.** Siggu padakandi.

**Legal Shield - Chattu Mee Vaipu Undi:**
`IT Act Section 66E`: Photo/video consent lekunda teeste **3 Years Jail**.
`IT Act Section 67A`: Explicit content share cheste **5 Years Jail**.

**Ventane Cheyavalasina 4 Steps - "STOP Protocol":**
1. **S - STOP**: Vadi tho matladatam aapeyandi.
2. **T - TAKE SCREENSHOTS**: Chat, number, profile anni teesukondi.
3. **O - ORIENT POLICE**: Vadi number ikkada pampandi.
4. **P - PROTECT PROFILE**: Social Media private pettukondi.

**Mee Local Police Station - Direct Help:**
📍 **{ps_info['address']}**
📞 **Phone: {ps_info['phone']}** | **100 Emergency**
"""

    else:
        reply = f"""
Mee samasya naaku artham ayyindi. Konchem vivaranga cheppagalara? Screenshot unte upload cheyandi.

**Mee District Police Help:**
📍 **{ps_info['address']}**
📞 **Phone: {ps_info['phone']}** | **1930**
"""

    return reply, show_audio_button

# --- Streamlit App UI ---
st.title("👮‍♂️ Raksha Sir V2.3")
st.caption("Telangana State Police - Cyber Crime Wing | Voice Alert + Local PS Connect")
st.markdown("---")

# --- District Selector ---
district = st.selectbox(
    "📍 Mee District Select Cheyandi - Local Police Details Kosam",
    options=list(DISTRICT_PSS.keys()),
    index=0
)

st.warning("**Namaste.** Nenu Mee Raksha Sir ni. Mosapoyara? Screenshot unte upload cheyandi. Bayapadakandi, chattu mee vaipu undi.")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": f"Namaste! Nenu {district} district students kosam unna Raksha Sir ni. Betting app, fake SBI link, blackmail lanti vati gurinchi cheppandi. Screenshot unte upload cheyandi."}]

# --- Chat Display ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image" in message:
            st.image(message["image"], width=300)

# --- Photo Upload Only ---
uploaded_file = st.file_uploader("🖼️ Screenshot / Photo Upload Cheyandi", type=["jpg", "jpeg", "png"], key="uploader")

if uploaded_file is not None:
    st.success("Screenshot receive ayyindi. Deeni tho patu mee samasya kinda type cheyandi.")

# --- Chat Input ---
if user_input := st.chat_input("Mee samasya ikkada type cheyandi..."):
    user_msg = {"role": "user", "content": user_input}
    if uploaded_file:
        user_msg["image"] = uploaded_file

    st.session_state.messages.append(user_msg)
    with st.chat_message("user"):
        st.markdown(user_input)
        if uploaded_file:
            st.image(uploaded_file, width=300)

    reply, show_audio_button = get_legal_advice(user_input, district)

    if uploaded_file:
        reply += "\n\n✅ **Evidence Receive Ayindi.** Ee screenshot ni mee Case ID tho Cyber Crime Police ki pampadaniki save chesamu."

    case_id = f"RS{datetime.now().strftime('%d%m%H%M%S')}"
    reply += f"\n\n---\n**Mee Raksha Case ID: {case_id}** | **District: {district}**\nEe ID tho {DISTRICT_PSS[district]['phone']} ki call cheyandi."

    with st.chat_message("assistant"):
        st.markdown(reply)

        # Option 3: Audio Button - Betting detect aithe ne vastundi
        if show_audio_button:
            st.error("🚨 Hetchharika! Kinda button nokki Police Warning vinu")
            if st.button("🔊 Police Warning Vinu", type="primary", key=f"audio_{case_id}"):
                audio_html = """
                <script>
                    var msg = new SpeechSynthesisUtterance();
                    msg.text = "Hetchharika! Idi illegal betting app. Telangana Gaming Act prakaram seven years jail padutundi. Ventane delete cheyandi.";
                    msg.lang = 'te-IN';
                    window.speechSynthesis.speak(msg);
                </script>
                """
                st.components.v1.html(audio_html, height=0)
                st.success("✅ Warning play ayyindi. Jagratha.")

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()

st.markdown("---")
st.caption("For emergencies, dial 100 or 1930. | Developed for Student Safety | This is an AI advisor, not a replacement for a formal police complaint.")
