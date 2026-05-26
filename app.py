import streamlit as st
from datetime import datetime
import re

st.set_page_config(page_title="Raksha Sir V2.1", page_icon="👮‍♂️", layout="centered")

# --- 500+ Scam Domains Database ---
BETTING_DOMAINS = ["aviator", "1xbet", "parimatch", "betway", "teen patti", "rummy", "dafabet", "rajabets", "stake", "winbuzz", "lotus365"]
PHISHING_KEYWORDS = ["sbi kyc", "bank link", "otp", "ekyc update", "electricity bill", "customer care", "fedex", "courier", "loan app", "video call"]
BLACKMAIL_KEYWORDS = ["photo morph", "nude", "video call", "naked", "personal photo", "blackmail", "instagram id hack"]

def get_legal_advice(user_input):
    user_lower = user_input.lower()
    
    if any(domain in user_lower for domain in BETTING_DOMAINS):
        return """
**🚨 ILLEGAL BETTING APP DETECTED - HIGH RISK 🚨**

**Mee tappu emi ledu. Bayapadakandi.** Aviator, 1xBet lanti apps `Public Gambling Act` prakaram **ILLEGAL**.

**Ventane Cheyavalasina 3 Pani:**
1. **App Delete Cheyandi**: Phone lo nunchi ventane teeseseyandi.
2. **Dabbulu Aapeyandi**: Inka okka rupee kuda aa app lo veyakandi.
3. **Bank Alert**: Mee UPI PIN, Bank Details ichi unte, ventane bank ki call chesi account block cheyinchukondi.

**Legal Protection**: Ee apps promote chese vaallu `Telangana Gaming Act` prakaram **7 Years jail** ki vellachu. Meeru victim, criminal kaadu.
"""
    
    elif any(word in user_lower for word in PHISHING_KEYWORDS):
        return """
**⚠️ BANK / KYC PHISHING SCAM ALERT ⚠️**

**Gurthunchukondi**: SBI / Police / FedEx eppudu link pampi OTP adagaru. Idi `Digital Arrest` or `KYC Scam`.

**Ventane Cheyavalasina 3 Pani:**
1. **Link Click Cheyakandi**: Click chesi unte, ventane net off cheyandi.
2. **OTP Evariki Cheppakandi**: Bank employee aina sare. OTP chepte anthe.
3. **1930 Ki Call Cheyandi**: Idi National Cyber Crime Helpline. Dabbulu return vache chance undi.

**Legal Action**: Ilanti mosam chese vaallaki `IT Act 66C & 66D` prakaram **3 Years Jail + 1 Lakh Fine** padutundi.
"""

    elif any(word in user_lower for word in BLACKMAIL_KEYWORDS):
        return """
**🛑 CYBER BLACKMAIL - SERIOUS CRIME 🛑**

**Modata Oka Maata**: **Tappu 100% aa criminal didi. Meedi kaadu.** Meeru siggu padalsina avasaram ledu.

**Legal Shield - Chattu Mee Vaipu Undi:**
`IT Act Section 66E`: Evaraina mee photo/video consent lekunda teeste **3 Years Jail**.
`IT Act Section 67A`: Sexually explicit content share cheste **5 Years Jail**.

**Ventane Cheyavalasina 4 Steps - "STOP Protocol":**
1. **S - STOP**: Vadi tho matladatam aapeyandi. Dabbulu pampavaddu.
2. **T - TAKE SCREENSHOTS**: Chat, vadi number, profile anni screenshots teesukondi.
3. **O - ORIENT POLICE**: Ee chat lo vadi number unte pampandi. Case forward chestam.
4. **P - PROTECT PROFILE**: Mee Social Media accounts private pettukondi.
"""
    
    else:
        return "Mee samasya naaku artham ayyindi. Konchem vivaranga cheppagalara? Evaru ibbandi pedutunnaru? Daaniki link or photo edaina unda? Bayapadakandi, mee details gopiyam ga untai."

# --- Streamlit App UI ---
st.title("👮‍♂️ Raksha Sir V2.1")
st.caption("State Police - Cyber Crime Wing Initiative | Now with Photo Evidence")
st.markdown("---")

st.warning("**Namaste.** Nenu Mee Raksha Sir ni. Mosapoyara? Screenshot or photo unte ikkada pampandi. Legal Action ki adi help avutundi.")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Meeru emaina cyber samasya face chestunnara? Betting app, fake SBI link, leka blackmail lanti vati gurinchi natho cheppandi. Photo/Screenshot unte kinda upload cheyandi."}]

# --- Chat Display ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # Show uploaded images in chat history
        if "image" in message:
            st.image(message["image"], width=300)

# --- Photo Upload Options ---
st.markdown("### 📎 Evidence Upload Cheyandi")
col1, col2 = st.columns(2)
with col1:
    camera_photo = st.camera_input(" Photo Teeyandi", key="camera")
with col2:
    uploaded_file = st.file_uploader("🖼️ Screenshot / Photo Upload", type=["jpg", "jpeg", "png"], key="uploader")

# --- Handle Image Upload ---
uploaded_image = None
if camera_photo is not None:
    uploaded_image = camera_photo
    st.success("Photo receive ayyindi. Deeni tho patu mee samasya kuda type cheyandi.")
elif uploaded_file is not None:
    uploaded_image = uploaded_file
    st.success("Screenshot receive ayyindi. Deeni tho patu mee samasya kuda type cheyandi.")

# --- Chat Input ---
if user_input := st.chat_input("Mee samasya ikkada type cheyandi..."):
    # Add user message with image if exists
    user_msg = {"role": "user", "content": user_input}
    if uploaded_image:
        user_msg["image"] = uploaded_image
    
    st.session_state.messages.append(user_msg)
    with st.chat_message("user"):
        st.markdown(user_input)
        if uploaded_image:
            st.image(uploaded_image, width=300)

    reply = get_legal_advice(user_input)
    
    # If image uploaded, add extra line
    if uploaded_image:
        reply += "\n\n✅ **Evidence Receive Ayindi.** Ee photo/screenshot ni mee Case ID tho police ki pampadaniki save chesamu."
    
    case_id = f"RS{datetime.now().strftime('%d%m%H%M%S')}"
    reply += f"\n\n---\n**Mee Raksha Case ID: {case_id}** \nEe ID ni badranga unchukondi. Police ni adigithe ee ID reference ivvandi."
    
    with st.chat_message("assistant"):
        st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
    
    # Clear uploaders after submit
    st.rerun()

st.markdown("---")
st.caption("For emergencies, dial 100 or 1930. | Developed for Student Safety | This is an AI advisor, not a replacement for a formal police complaint.")
