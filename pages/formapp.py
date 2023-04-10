

import time
import streamlit as st
import pandas as pd
st.markdown("<h1 style= 'text-align:center';> Data input </h1>",unsafe_allow_html=True)
st.markdown("---")
with st.form("Data input form : ", clear_on_submit=True):
    # divides form into 2 cols
    # col1, col2 = st.columns(2)
    data_prep = st.text_input("Data preparation and integration approach  ")
    mod_name = st.text_input("Model name ")
    methodology = st.text_input("Model methodology  ")
    notes = st.text_input("Any extra notes  ")
    # st.text_input("Confirm Password : ")
    # day, month, year = st.columns(3)
    # day.text_input("Day")
    # month.text_input("Month")
    # year.text_input("Year")
    s_state = st.form_submit_button("Submit")
    if s_state:
        if data_prep == "" or mod_name == "" or methodology == "" or notes == "":
            st.warning("Please fill the above fields")
        if data_prep != "" and mod_name != "" and methodology != "" or notes != "":
            st.success("Submitted Successfully")
