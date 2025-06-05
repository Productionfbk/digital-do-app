import streamlit as st
import pandas as pd
from datetime import datetime
import os

# SET PAGE CONFIG MESTI PALING AWAL
st.set_page_config(page_title="Delivery/Requisition Form", layout="wide")

# --- User Credentials ---
USER_CREDENTIALS = {
    "firdaus": "D0499",
    "vijaya": "D0228",
    "asrin": "D0489",
    "sazli": "D0039",
    "Eddy": "D0290"
}

# --- Login function ---
def login():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.subheader("🔐 Leader Login Required")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"✅ Welcome, {username}!")
                st.experimental_rerun()
            else:
                st.error("❌ Invalid username or password.")
        st.stop()  # Stop further execution if not logged in
    else:
        # Show logout and user info
        st.sidebar.write(f"👤 Logged in as: **{st.session_state.username}**")
        if st.sidebar.button("Logout"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.experimental_rerun()

# --- Delivery Order Number Generator ---
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

# --- Reset form ---
def reset_form():
    for i in range(1, 21):
        for key in ["item", "ref", "cp", "set", "ctn", "qty", "remark"]:
            st.session_state.pop(f"{key}_{i}", None)
    for key in ["prepared", "checked", "approved", "time"]:
        st.session_state.pop(key, None)
    st.session_state.do_no = get_next_do_no()
    st.experimental_rerun()

# --- MAIN ---
login()  # call login first, stops if not logged in

# Initialize DO number
if "do_no" not in st.session_state:
    st.session_state.do_no = get_next_do_no()

st.title("📦 FBK Delivery / Requisition Form")

# Header input
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

st.markdown("---")
st.subheader("Footer Information")
prepared = st.text_input("Prepared by", key="prepared")
checked = st.text_input("Checked by", key="checked")
approved = st.text_input("Approved by", key="approved")
time_input = st.time_input("Time", key="time")

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

            output_folder = "do_output"
            os.makedirs(output_folder, exist_ok=True)
            filename = os.path.join(output_folder, f"do_{st.session_state.do_no}.csv")
            df.to_csv(filename, index=False)

            st.success(f"✅ Delivery Order {st.session_state.do_no} submitted successfully.")
            st.info(f"Saved to `{filename}`")
            st.dataframe(df)

            reset_form()

with col_reset:
    if st.button("🔄 Reset Form"):
        reset_form()
