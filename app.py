import streamlit as st
import pandas as pd
from datetime import datetime
import os
 
st.set_page_config(page_title="Delivery/Requisition Form", layout="wide")
st.title("📦 FBK Delivery / Requisition Form")
 
# Function untuk auto-generate DO number
def get_next_do_number():
    filename = "last_do.txt"
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            f.write("1")
        return "DO0001"
    else:
        with open(filename, "r") as f:
            content = f.read().strip()
            if content == "":
                current_no = 1
            else:
                current_no = int(content)
        next_no = current_no + 1
        with open(filename, "w") as f:
            f.write(str(next_no))
        return f"DO{next_no:04d}"
 
# Get DO number
do_no = get_next_do_number()
 
# Form Details
st.subheader("FBK MANUFACTURING MALAYSIA")
col1, col2, col3 = st.columns(3)
 
with col1:
    st.text_input("DO No (Auto)", value=do_no, disabled=True)
 
with col2:
    date = st.date_input("Date", value=datetime.today())
 
with col3:
    from_to = st.selectbox("From → To", ["STORE → STORE", "BS PACKING → LOGISTIC", "DP PACKING → LOGISTIC", "OFFICE → TPM"])
 
st.markdown("---")
st.subheader("Item Details (up to 20 rows)")
 
# Table Input
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
 
# Footer Section
st.markdown("---")
st.subheader("Footer Information")
 
prepared = st.text_input("Prepared by")
checked = st.text_input("Checked by")
approved = st.text_input("Approved by")
time_input = st.time_input("Time")
 
# Submit Button
if st.button("✅ Submit DO Form"):
    if not rows:
        st.error("Please fill in at least one item.")
    else:
        df = pd.DataFrame(rows)
        df["DO No"] = do_no
        df["Date"] = date.strftime('%Y-%m-%d')
        df["From→To"] = from_to
        df["Prepared By"] = prepared
        df["Checked By"] = checked
        df["Approved By"] = approved
        df["Time"] = time_input.strftime('%H:%M:%S')
 
        filename = f"do_{do_no}.csv"
        df.to_csv(filename, index=False)
 
        st.success(f"✅ DO saved successfully as {filename}")
        st.dataframe(df)
 
        # Reset form by rerunning app
        st.rerun()
 