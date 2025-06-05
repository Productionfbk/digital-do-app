import streamlit as st
import pandas as pd
from datetime import datetime
import os
 
st.set_page_config(page_title="Delivery/Requisition Form", layout="wide")
st.title("📦 FBK Delivery / Requisition Form")
 
# Auto-generate DO number
def get_next_do_no():
    counter_file = "do_counter.txt"
    if not os.path.exists(counter_file):
        with open(counter_file, "w") as f:
            f.write("1000")
    with open(counter_file, "r") as f:
        last = int(f.read().strip())
    next_do = last + 1
    with open(counter_file, "w") as f:
        f.write(str(next_do))
    return f"DO{next_do:04d}"
 
# Initialize DO number if not already set
if "do_no" not in st.session_state:
    st.session_state.do_no = get_next_do_no()
 
# 🧹 Reset Form Function
def reset_form():
    # Reset item rows
    for i in range(1, 21):
        for key in ["item", "ref", "cp", "set", "ctn", "qty", "remark"]:
            session_key = f"{key}_{i}"
            if session_key in st.session_state:
                del st.session_state[session_key]
    
    # Reset footer
    for key in ["prepared", "checked", "approved", "time"]:
        if key in st.session_state:
            del st.session_state[key]
 
    # Reset DO number
    st.session_state.do_no = get_next_do_no()
 
    st.rerun()
 
# ──────────────────────────────
# Header Info
st.subheader("FBK MANUFACTURING MALAYSIA")
col1, col2, col3 = st.columns(3)
 
with col1:
    st.text_input("DO No", value=st.session_state.do_no, disabled=True)
 
with col2:
    date = st.date_input("Date", value=datetime.today())
 
with col3:
    from_to = st.selectbox("From → To", [
        "STORE → STORE",
        "BS PACKING → LOGISTIC",
        "DP PACKING → LOGISTIC",
        "OFFICE → TPM"
    ])
 
# ──────────────────────────────
# Item Input Section
st.markdown("---")
st.subheader("Item Details (up to 20 rows)")
rows = []
 
for i in range(1, 21):
    with st.expander(f"Item Row {i}"):
        item = st.text_input(f"Scan or Enter Item {i}", key=f"item_{i}")
        ref_no = st.text_input(f"Reference No {i}", key=f"ref_{i}")
        cp_no = st.text_input(f"C/P No {i}", key=f"cp_{i}")
        unit_set = st.text_input(f"Unit Packing (Set) {i}", key=f"set_{i}")
        unit_ctn = st.text_input(f"Unit Packing (CTN) {i}", key=f"ctn_{i}")
        quantity = st.text_input(f"Quantity {i}", key=f"qty_{i}")
        remarks = st.text_input(f"Remarks {i}", key=f"remark_{i}")
 
        if item:
            rows.append({
                "Item": item,
                "Reference No": ref_no,
                "C/P No": cp_no,
                "Unit Packing Set": unit_set,
                "Unit Packing CTN": unit_ctn,
                "Quantity": quantity,
                "Remarks": remarks
            })
 
# ──────────────────────────────
# Footer Info
st.markdown("---")
st.subheader("Footer Information")
prepared = st.text_input("Prepared by", key="prepared")
checked = st.text_input("Checked by", key="checked")
approved = st.text_input("Approved by", key="approved")
time_input = st.time_input("Time", key="time")
 
# ──────────────────────────────
# Buttons
col_submit, col_reset = st.columns([1, 1])
with col_submit:
    if st.button("✅ Submit DO Form", key="submit_do"):
        if not rows:
            st.error("Please fill at least one item.")
        else:
            df = pd.DataFrame(rows)
            df["DO No"] = st.session_state.do_no
            df["Date"] = date.strftime('%Y-%m-%d')
            df["From→To"] = from_to
            df["Prepared By"] = prepared
            df["Checked By"] = checked
            df["Approved By"] = approved
            df["Time"] = time_input.strftime('%H:%M:%S')
 
            filename = f"do_{st.session_state.do_no}.csv"
            df.to_csv(filename, index=False)
 
            st.success(f"DO saved as {filename} ✅")
            st.dataframe(df)
 
with col_reset:
    if st.button("🔄 Reset Form"):
        reset_form()