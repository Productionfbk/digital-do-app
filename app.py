import streamlit as st
import pandas as pd
import os
from datetime import datetime
import uuid
 
st.set_page_config(page_title="Delivery/Requisition Form", layout="wide")
st.title("📦 FBK Delivery / Requisition Form")
 
# === Auto-generate DO Number ===
def generate_do_number():
    today = datetime.today().strftime("%Y%m%d")
    folder = "do_data"
    os.makedirs(folder, exist_ok=True)
    existing = [f for f in os.listdir(folder) if f.startswith(f"do_{today}")]
    new_number = len(existing) + 1
    return f"{today}-{new_number:03d}"
 
if 'submitted' not in st.session_state:
    st.session_state.submitted = False
 
if not st.session_state.submitted:
    # === FORM DETAILS ===
    st.subheader("FBK MANUFACTURING MALAYSIA")
    col1, col2, col3 = st.columns(3)
    with col1:
        do_no = generate_do_number()
        st.text_input("DO No", value=do_no, disabled=True, key="do_no_display")
    with col2:
        date = st.date_input("Date", value=datetime.today())
    with col3:
        from_to = st.selectbox("From → To", ["STORE → STORE", "BS PACKING → LOGISTIC", "DP PACKING → LOGISTIC", "OFFICE → TPM"])
 
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
    prepared = st.text_input("Prepared by")
    checked = st.text_input("Checked by")
    approved = st.text_input("Approved by")
    time_input = st.time_input("Time")
 
    # === SUBMIT BUTTON ===
    if st.button("✅ Submit DO Form"):
        if not rows:
            st.error("Please scan at least one item.")
        else:
            df = pd.DataFrame(rows)
            df["DO No"] = do_no
            df["Date"] = date.strftime('%Y-%m-%d')
            df["From→To"] = from_to
            df["Prepared By"] = prepared
            df["Checked By"] = checked
            df["Approved By"] = approved
            df["Time"] = time_input.strftime('%H:%M:%S')
 
            filename = f"do_data/do_{do_no}.csv"
            df.to_csv(filename, index=False)
 
            st.success(f"✅ DO saved successfully as `{filename}`")
            st.dataframe(df)
 
            # Set submitted state to reset form
            st.session_state.submitted = True
            st.experimental_rerun()
 
else:
    st.success("🎉 DO Form has been submitted.")
    if st.button("➕ Create New DO Form"):
        st.session_state.submitted = False
        st.experimental_rerun()
