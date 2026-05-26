import streamlit as st
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
import urllib.parse

# Streamlit Secrets lo pettuko
TWILIO_SID = st.secrets["TWILIO_ACCOUNT_SID"]
TWILIO_TOKEN = st.secrets["TWILIO_AUTH_TOKEN"] 
TWILIO_NUMBER = st.secrets["TWILIO_PHONE_NUMBER"] # +1XXXXXXXXXX

def send_police_warning_call(scammer_number, report_count):
    try:
        client = Client(TWILIO_SID, TWILIO_TOKEN)
        
        # Voice message Telugu lo
        voice_msg = f"Alert from Kakinada Cyber Crime Police. Your mobile number {scammer_number} has been reported {report_count} times for online fraud. An FIR is under process under IPC 420 and IT Act 66 D. To avoid arrest, call 1930 immediately. This call is being recorded."
        
        # Twilio ki URL encode chesi pampali
        encoded_msg = urllib.parse.quote(voice_msg)
        
        call = client.calls.create(
            twiml=f'<Response><Say voice="Polly.Aditi" language="en-IN">{voice_msg}</Say></Response>',
            to=f"+91{scammer_number}", # India numbers ki +91 add
            from_=TWILIO_NUMBER
        )
        return True, call.sid
    except Exception as e:
        return False, str(e)

# Blacklist Checker function lo ila marchu
def blacklist_checker(number):
    report_count = st.session_state.blacklist_db.get(number, 0)
    
    if report_count > 0:
        st.error(f"🚨 DANGER: {number} is reported {report_count} times for fraud.")
        
        # NEW V4.0 BUTTON
        if st.button(f"🔴 Send Police Warning Call to {number}", type="primary"):
            with st.spinner("Connecting to Cyber Crime Voice Server..."):
                success, result = send_police_warning_call(number, report_count)
                
            if success:
                st.success(f"✅ Warning Call Sent to Scammer! Call ID: {result[:8]}")
                st.balloons()
                st.info("Scammer ki ippudu police warning vellindi. Recorded call proof meeku WhatsApp lo pampistam - V4.1 lo.")
                st.audio("warning.mp3") # Nee 7 years jail audio
            else:
                st.error(f"Call Failed. Reason: {result}. Free tier lo verified numbers ke ne call veltundi.")
    else:
        st.success(f"✅ {number} is not in our blacklist yet. Still, be careful.")
