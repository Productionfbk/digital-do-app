import streamlit as st
import pandas as pd
import os
from datetime import date, datetime
 
# Konfigurasi halaman
st.set_page_config(page_title="Digital DO Form", layout="wide")
 
# Tajuk utama
st.title("🚚 Digital Delivery Order (DO) Form - The Fixers")
 
# Fungsi auto-generate DO No
def generate_do_number():
    # Jika do_data.csv wujud dan tidak kosong, ambil DO Number terakhir
    if os.path.exists("do_data.csv"):
        df_existing = pd.read_csv("do_data.csv")
        if not df_existing.empty:
            last_do = df_existing["DO Number"].iloc[-1]
            try:
                last_num = int(last_do.split("-")[1])
                return f"DO-{last_num + 1:04d}"
            except:
                # Kalau format lain, reset ke 0001
                return "DO-0001"
    # Jika fail belum wujud atau kosong, mula dari 0001
    return "DO-0001"
 
# Jana nombor DO
do_number = generate_do_number()
 
# ---------------------------------------------------
# Form untuk isi DO
# ---------------------------------------------------
with st.form("do_form"):
    st.subheader("📄 Delivery Order Information")
 
    # Dua column: DO No & DO Date
    col1, col2 = st.columns([1, 1])
    with col1:
        st.text_input("DO Number", value=do_number, disabled=True)
    with col2:
do_date = st.date_input("DO Date", value=date.today())
 
    # Customer Name
    customer_name = st.text_input("Customer Name")
 
    st.markdown("---")
    st.subheader("📦 Item Details (maksimum 5 baris)")
 
    # Sediakan data kosong untuk 5 baris
    default_items = {
        "No.": [1, 2, 3, 4, 5],
        "Item": ["", "", "", "", ""],
        "MI Number": ["", "", "", "", ""],
        "C/P No.": ["", "", "", "", ""],
        "Set": [0, 0, 0, 0, 0],
        "Ctn": [0, 0, 0, 0, 0],
        "Quantity": [0, 0, 0, 0, 0]
    }
    item_df = pd.DataFrame(default_items)
 
    # Papar table editable (boleh tambah/murangi baris jika perlu)
    edited_df = st.data_editor(
        item_df,
        num_rows="fixed",             # "fixed" bermaksud 5 baris, boleh ubah jika mahu "dynamic"
        use_container_width=True
    )
 
    # Butang Submit dan Clear Form
    col_submit, col_clear = st.columns([1, 1])
    with col_submit:
        submitted = st.form_submit_button("🚀 Submit DO")
    with col_clear:
        reset = st.form_submit_button("🔄 Clear Form")
 
    # Jika tekan Clear, kita reload halaman (kosongkan input)
    if reset:
        st.experimental_rerun()
 
    # Proses bila Submit
    if submitted:
        # Semak sekurang-kurangnya satu baris item diisi (field Item dan Quantity > 0)
        valid_rows = []
        for _, row in edited_df.iterrows():
            if row["Item"].strip() != "" and row["Quantity"] > 0:
                valid_rows.append(row)
 
        if not valid_rows:
            st.warning("⚠️ Sila isi sekurang-kurangnya satu item dengan kuantiti lebih daripada 0.")
        else:
            # Tarikh dan masa simpan
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
 
            # Simpan setiap baris ke CSV
            rows_to_save = []
            for row in valid_rows:
                record = {
                    "Timestamp": timestamp,
                    "DO Number": do_number,
                    "DO Date": do_date.strftime("%Y-%m-%d"),
                    "Customer Name": customer_name,
                    "No.": int(row["No."]),
                    "Item": row["Item"],
                    "MI Number": row["MI Number"],
                    "C/P No.": row["C/P No."],
                    "Set": int(row["Set"]),
                    "Ctn": int(row["Ctn"]),
                    "Quantity": int(row["Quantity"])
                }
                rows_to_save.append(record)
 
            df_to_save = pd.DataFrame(rows_to_save)
            file_exists = os.path.exists("do_data.csv")
            df_to_save.to_csv("do_data.csv", mode="a", header=not file_exists, index=False)
 
            st.success("✅ DO submitted and saved successfully!")
 
            st.markdown("### 📄 DO Summary:")
            st.write(f"**DO Number:** {do_number}")
            st.write(f"**DO Date:** {do_date.strftime('%Y-%m-%d')}")
            st.write(f"**Customer Name:** {customer_name}")
            st.write("#### Items:")
            st.dataframe(df_to_save, use_container_width=True)
 
# ---------------------------------------------------
# Bahagian Paparan Semua Rekod DO
# ---------------------------------------------------
st.markdown("---")
st.subheader("📋 All Submitted DO Records")
 
if os.path.exists("do_data.csv"):
    df_all = pd.read_csv("do_data.csv")
    st.dataframe(df_all, use_container_width=True)
else:
st.info("Tiada DO dihantar lagi.")