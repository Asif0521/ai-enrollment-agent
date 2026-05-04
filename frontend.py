import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="TechU Admin Dashboard", page_icon="📊", layout="wide")

st.title("📊 TechU AI Enrollment - Admin Dashboard")
st.write("Internal team dashboard for monitoring AI enrollments and lead metrics.")

# Security simple mock
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    st.subheader("Admin Login")
    password = st.text_input("Enter password", type="password")
    if st.button("Login"):
        if password == "admin123":
            st.session_state['authenticated'] = True
            st.rerun()
        else:
            st.error("Incorrect password")
else:
    st.sidebar.button("Logout", on_click=lambda: st.session_state.update({'authenticated': False}))
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Leads", "142", "+12")
    col2.metric("Enrolled", "86", "+5")
    col3.metric("Conversion Rate", "60.5%", "+2.1%")
    col4.metric("Avg Fit Score", "88", "+1")

    st.subheader("Recent Applications (Mock Data / CSV)")
    
    csv_path = "raw_enrollment_data.csv"
    if os.path.exists(csv_path):
        try:
            df = pd.read_csv(csv_path)
            st.dataframe(df.tail(10))
            
            st.subheader("Course Distribution")
            if 'Recommendation Course' in df.columns:
                st.bar_chart(df['Recommendation Course'].value_counts())
        except:
            st.warning("Could not read CSV data.")
    else:
        st.info("No raw_enrollment_data.csv found yet. Start sending webhooks!")
        
    st.subheader("Trigger Manual Sync")
    if st.button("Refresh Power BI Dataset"):
        with st.spinner("Calling Power BI API..."):
            # Mock sync
            import time; time.sleep(1)
            st.success("Power BI Dataset Refresh Triggered Successfully!")
