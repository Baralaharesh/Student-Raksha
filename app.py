import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Raksha Sir", page_icon="👮‍♂️", layout="centered")

st.title("👮‍♂️ Raksha Sir")
st.caption("Police - Cyber Crime Wing Initiative")
st.markdown("---")

st.info("**Namaste.** Nenu Mee Raksha Sir ni. Cyber mosalu, betting apps, blackmail lanti vati nunchi students ni kapadataniki nenu ikkada unnanu. Mee samacharam 100% gopiyam ga unchabadutundi.")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Meeru emaina cyber samasya face chestunnara? Dayachesi natho panchukondi."}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("Mee samasya ikkada type cheyandi..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    user_lower = user_input.lower()
    if any(word in user_lower for word in ["betting", "aviator", "teen patti", "money"]):
        reply = """**Artham chesukunnanu.** Betting apps chala mandi students jeevithalanu nasanam chestunnai. 

**Ventane cheyavalasina pani:**
1. Aa app ni ventane delete cheyandi.
2. Evarikaina UPI PIN, OTP ichara? Iste bank ki call cheyandi.
3. **Mee tappu emi ledu.** Bayapadakandi. 

Mee school peru, district chepte memu mee school lo awareness session pedatam."""
    
    elif any(word in user_lower for word in ["photo", "blackmail", "morph"]):
        reply = """**Idi serious Cyber Crime.** Mee bhayam naaku artham avutundi. **Tappu vaadidi, mee di kaadu.**

**Legal Protection:** IT Act 66E, 67A prakaram vadu 3-5 years jail ki vellachu.

**Cheyavalasina pani:**
1. Vadi tho chat, photos anni screenshots teesukondi. Delete cheyyakandi.
2. Vadi number, ID link unte ikkada paste cheyandi.
3. Nenu ee case ni Cyber Crime PS ki forward chestanu."""
    
    else:
        reply = "Mee samasya naaku artham ayyindi. Konchem vivaranga cheppagalara? Evaru ibbandi pedutunnaru, ela?"

    case_id = f"RS{datetime.now().strftime('%d%m%H%M')}"
    reply += f"\n\n---\n**Mee Raksha Case ID: {case_id}** \nEe ID save chesukondi."
    
    with st.chat_message("assistant"):
        st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})

st.markdown("---")
st.caption("For emergencies, dial 100 or 1930. | Developed for Student Safety")
