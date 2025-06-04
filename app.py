import streamlit as st
import pandas as pd
from datetime import datetime
 
st.set_page_config(page_title="Digital DO App", layout="centered")
 
st.title("📦 Delivery Order (DO) Form")
st.markdown("Isi maklumat DO untuk proses digitalisasi dan posting ke sistem.")
 
# Form input
with st.form("do_form"):
    do_number = st.text_input("No DO")
    customer = st.text_input("Customer Name")
    item = st.text_input("Product Name / Description")
    quantity = st.number_input("Quantity", min_value=1)
date = st.date_input("Delivery Date", value=datetime.today())
 
submitted = st.form_submit_button("Submit")
 
# Bila user tekan submit
if submitted:
    data = {
        "DO Number": do_number,
        "Customer": customer,
        "Item": item,
        "Quantity": quantity,
        "Delivery Date": date.strftime("%Y-%m-%d")
    }
 
    df = pd.DataFrame([data])
 
    # Simpan data ke Excel/CSV buat sementara
df.to_csv("do_log.csv", mode="a", header=not pd.read_csv("do_log.csv").empty if pd.io.common.file_exists("do_log.csv") else True, index=False)
 
st.success("Maklumat DO berjaya dihantar! ✅")
st.write("**Ringkasan:**")
st.json(data)
 