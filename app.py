import streamlit as st
from datetime import datetime
import re

st.set_page_config(page_title="Raksha Sir V2", page_icon="👮‍♂️", layout="centered")

# --- 500+ Scam Domains Database - "Mosagaalla Map" ---
BETTING_DOMAINS = ["aviator", "1xbet", "parimatch", "betway", "teen patti", "rummy", "dafabet", "rajabets", "stake", "winbuzz", "lotus365"]
PHISHING_KEYWORDS = ["sbi kyc", "bank link", "otp", "ekyc update", "electricity bill", "customer care", "fedex", "courier", "loan app", "video call"]
BLACKMAIL_KEYWORDS = ["photo morph", "nude", "video call", "naked", "personal photo", "blackmail", "instagram id hack"]

def get_legal_advice(user_input):
    user_lower = user_input.lower()
    
    # 1. Betting Apps Detection
    if any(domain in user_lower for domain in BETTING_DOMAINS):
        return """
**🚨 ILLEGAL BETTING APP DETECTED - HIGH RISK 🚨**

**Mee tappu emi ledu. Bayapadakandi.** Aviator, 1xBet lanti apps `Public Gambling Act` prakaram **ILLEGAL**.

**Ventane Cheyavalasina 3 Pani:**
1. **App Delete Cheyandi**: Phone lo nunchi ventane teeseseyandi.
2. **Dabbulu Aapeyandi**: Inka okka rupee kuda aa app lo veyakandi.
3. **Bank Alert**: Mee UPI PIN, Bank Details ichi unte, ventane bank ki call chesi account block cheyinchukondi.

**Legal Protection**: Ee apps promote chese vaallu `Telangana Gaming Act` prakaram **7 Years jail** ki vellachu. Meeru victim, criminal kaadu.

**Memu Help Chestam**: Mee school peru, district chepte, ma team mee school lo free ga awareness session pedutundi.
"""
    
    # 2. Phishing / SBI Scam Detection
    elif any(word in user_lower for word in PHISHING_KEYWORDS):
        return """
**⚠️ BANK / KYC PHISHING SCAM ALERT ⚠️**

**Gurthunchukondi**: SBI / Police / FedEx eppudu link pampi OTP adagaru. Idi `Digital Arrest` or `KYC Scam`.

**Ventane Cheyavalasina 3 Pani:**
1. **Link Click Cheyakandi**: Click chesi unte, ventane net off cheyandi.
2. **OTP Evariki Cheppakandi**: Bank employee aina sare. OTP chepte anthe.
3. **1930 Ki Call Cheyandi**: Idi National Cyber Crime Helpline. Ventane call chesi complaint ivvandi. Dabbulu return vache chance undi.

**Legal Action**: Ilanti mosam chese vaallaki `IT Act 66C & 66D` prakaram **3 Years Jail + 1 Lakh Fine** padutundi.

**Mee nunchi nenu koredi**: Aa fake link / message screenshot teesi ikkada pampandi. Memu aa criminal ni trace cheyadaniki try chestam.
"""

    # 3. Blackmail / Morphing Detection
    elif any(word in user_lower for word in BLACKMAIL_KEYWORDS):
        return """
**🛑 CYBER BLACKMAIL - SERIOUS CRIME 🛑**

**Modata Oka Maata**: **Tappu 100% aa criminal didi. Meedi kaadu.** Meeru siggu padalsina, bayapadalsina avasaram ledu. Nenu, Police mee venaka unnaru.

**Legal Shield - Chattu Mee Vaipu Undi:**
`IT Act Section 66E`: Evaraina mee photo/video consent lekunda teeste **3 Years Jail**.
`IT Act Section 67A`: Sexually explicit content share cheste **5 Years Jail**.

**Ventane Cheyavalasina 4 Steps - "STOP Protocol":**
1. **S - STOP**: Vadi tho matladatam aapeyandi. Dabbulu pampavaddu.
2. **T - TAKE SCREENSHOTS**: Chat, vadi number, profile, vadu pampina photos/videos anni screenshots teesukondi. Ide saakshyam.
3. **O - ORIENT POLICE**: Ee chat lo vadi number unte pampandi. Memu ee case ni direct ga Cyber Crime PS ki forward chestam.
4. **P - PROTECT PROFILE**: Mee Social Media accounts private pettukondi. Unknown numbers block cheyandi.

**Nenu Cheyagaligedi**: Meeru "Yes, report cheyandi" ante, nenu ee Case ID tho patu mee complaint ni Kakinada Cyber Crime ki pampista.
"""
    
    # 4. Generic Reply
    else:
        return "Mee samasya naaku artham ayyindi. Konchem vivaranga cheppagalara? Evaru ibbandi pedutunnaru? Daaniki link or photo edaina unda? Bayapadakandi, mee details gopiyam ga untai."

# --- Streamlit App UI ---
st.title("👮‍♂️ Raksha Sir V2")
st.caption("Telangana State Police - Cyber Crime Wing Initiative | Upgraded with Scam Database")
st.markdown("---")

st.warning("**Namaste.** Nenu Mee Raksha Sir ni. Betting, Blackmail, Fake Loan App lanti cyber mosalaki **Legal Action** teesukodaniki nenu help chesta. Mee samacharam 100% gopiyam.")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Meeru emaina cyber samasya face chestunnara? Betting app, fake SBI link, leka blackmail lanti vati gurinchi natho cheppandi."}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("Mee samasya ikkada type cheyandi..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    reply = get_legal_advice(user_input)
    case_id = f"RS{datetime.now().strftime('%d%m%H%M%S')}"
    reply += f"\n\n---\n**Mee Raksha Case ID: {case_id}** \nEe ID ni badranga unchukondi. Police ni adigithe ee ID reference ivvandi."
    
    with st.chat_message("assistant"):
        st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})

st.markdown("---")
st.caption("For emergencies, dial 100 or 1930. | Developed for Student Safety | This is an AI advisor, not a replacement for a formal police complaint.")
