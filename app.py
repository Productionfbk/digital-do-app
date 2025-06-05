import streamlit as st
import pandas as pd
from datetime import datetime
import os
 
st.set_page_config(page_title="Delivery/Requisition Form", layout="wide")
st.title("📦 FBK Delivery / Requisition Form")
 
# ---------- Auto-generate DO No ----------
def get_next_do_no():
    counter_file = "do_counter.txt"
    if not os.path.exists(counter_file):
        with open(counter_file, "w") as f:
            f.write("1001")
    with open(counter_file, "r") as f:
     last_number = int(f.read().strip())
     next_number = last_number + 1
    with open(counter_file, "w") as f:
        f.write(str(next_number))
    return f"DO{next_number:04d}"
 
# Initialize session state
if "do_no" not in st.session_state:
    st.session_state.do_no = get_next_do_no()
if "date" not in st.session_state:
    st.session_state.date = datetime.today()
if "from_to" not in st.session_state:
    st.session_state.from_to = "STORE → STORE"
if "prepared" not in st.session_state:
    st.session_state.prepared = ""
if "checked" not in st.session_state:
    st.session_state.checked = ""
if "approved" not in st.session_state:
    st.session_state.approved = ""
if "time" not in st.session_state:
    st.session_state.time = datetime.now().time()
for i in range(1, 21):
    for field in ["item", "ref", "cp", "set", "ctn", "qty", "remark"]:
        key = f"{field}_{i}"
        if key not in st.session_state:
            st.session_state[key] = ""
 
# ---------- Reset Function ----------
def reset_form():
    st.session_state.do_no = get_next_do_no()
    st.session_state.date = datetime.today()
    st.session_state.from_to = "STORE → STORE"
    st.session_state.prepared = ""
    st.session_state.checked = ""
    st.session_state.approved = ""
st.session_state.time = datetime.now().time()
for i in range(1, 21):
        for field in ["item", "ref", "cp", "set", "ctn", "qty", "remark"]:
            st.session_state[f"{field}_{i}"] = ""
st.rerun()
 
# ---------- Form Layout ----------
st.subheader("FBK MANUFACTURING MALAYSIA")
col1, col2, col3 = st.columns(3)
with col1:
    st.text_input("DO No", value=st.session_state.do_no, disabled=True)
with col2:
    st.date_input("Date", value=st.session_state.date, key="date")
with col3:
    st.selectbox("From → To", [
        "STORE → STORE",
        "BS PACKING → LOGISTIC",
        "DP PACKING → LOGISTIC",
        "OFFICE → TPM"
    ], key="from_to")
 
st.markdown("---")
st.subheader("Item Details (up to 20 rows)")
 
rows = []
for i in range(1, 21):
    with st.expander(f"Item Row {i}"):
        item = st.text_input(f"Scan or Enter Item (Barcode) {i}", key=f"item_{i}")
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
 
st.markdown("---")
st.subheader("Footer Information")
st.text_input("Prepared by", key="prepared")
st.text_input("Checked by", key="checked")
st.text_input("Approved by", key="approved")
st.time_input("Time", key="time")
 
# ---------- Submit ----------
if st.button("✅ Submit DO Form"):
    if not rows:
        st.error("Please fill at least one item.")
    else:
        df = pd.DataFrame(rows)
        df["DO No"] = st.session_state.do_no
        df["Date"] = st.session_state.date.strftime('%Y-%m-%d')
        df["From→To"] = st.session_state.from_to
        df["Prepared By"] = st.session_state.prepared
        df["Checked By"] = st.session_state.checked
        df["Approved By"] = st.session_state.approved
        df["Time"] = st.session_state.time.strftime('%H:%M:%S')
 
        filename = f"do_{st.session_state.do_no}.csv"
        df.to_csv(filename, index=False)
 
        st.success(f"DO saved as {filename} ✅")
        st.dataframe(df)
 
        reset_form()