import streamlit as st
import pandas as pd
import os
from datetime import date, datetime

# Konfigurasi halaman
st.set_page_config(page_title="Digital DO Form - FBKM", layout="wide")

# Tajuk utama
st.title("🚚 Digital Delivery Order (DO) FBKM")

# -------------------------------------------------------
# Fungsi jana DO number secara auto: DO-0001, DO-0002...
# -------------------------------------------------------
def generate_do_number():
    csv_path = "do_data.csv"
    if os.path.exists(csv_path):
        try:
            df_existing = pd.read_csv(csv_path)
            if not df_existing.empty and "DO Number" in df_existing.columns:
                last_do = df_existing["DO Number"].iloc[-1]
                try:
                    last_num = int(last_do.split("-")[1])
                    return f"DO-{last_num + 1:04d}"
                except:
                    return "DO-0001"
        except pd.errors.EmptyDataError:
            return "DO-0001"
        except Exception:
            return "DO-0001"
    return "DO-0001"

# Jana DO number
do_number = generate_do_number()

# -------------------------------------------------------
# Borang Utama
# -------------------------------------------------------
with st.form("do_form"):
    st.subheader("📄 Maklumat Delivery Order")

    col1, col2 = st.columns(2)
    with col1:
        st.text_input("DO Number", value=do_number, disabled=True)
    with col2:
        do_date = st.date_input("DO Date", value=date.today())

    customer_name = st.text_input("Customer Name")

    st.markdown("---")
    st.subheader("📦 Item Details (maksimum 20 baris)")

    # Sediakan template kosong untuk 20 item
    default_items = {
        "No.": list(range(1, 21)),
        "Item": [""] * 20,
        "MI Number": [""] * 20,
        "C/P No.": [""] * 20,
        "Set": [0] * 20,
        "Ctn": [0] * 20,
        "Quantity": [0] * 20
    }
    item_df = pd.DataFrame(default_items)

    # Papar borang table editable dengan index tersembunyi
    edited_df = st.data_editor(
        item_df,
        num_rows="fixed",
        use_container_width=True,
        hide_index=True
    )

    # Butang Submit & Clear
    col_submit, col_clear = st.columns(2)
    with col_submit:
        submitted = st.form_submit_button("🚀 Submit DO")
    with col_clear:
        reset = st.form_submit_button("🔄 Clear Form")

    # Reset form bila tekan Clear
    if reset:
        st.experimental_rerun()

    # Bila user tekan Submit
    if submitted:
        valid_rows = []
        for _, row in edited_df.iterrows():
            if row["Item"].strip() != "" and row["Quantity"] > 0:
                valid_rows.append(row)

        if not valid_rows:
            st.warning("⚠️ Sila isi sekurang-kurangnya satu item dengan kuantiti lebih daripada 0.")
        else:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
            csv_path = "do_data.csv"
            file_exists = os.path.exists(csv_path)
            df_to_save.to_csv(csv_path, mode="a", header=not file_exists, index=False)

            st.success("✅ DO submitted and saved successfully!")
            st.markdown("### 📄 DO Summary:")
            st.write(f"**DO Number:** {do_number}")
            st.write(f"**DO Date:** {do_date.strftime('%Y-%m-%d')}")
            st.write(f"**Customer Name:** {customer_name}")
            st.write("#### Items:")
            st.dataframe(df_to_save, use_container_width=True)

# -------------------------------------------------------
# Papar semua rekod yang pernah dihantar
# -------------------------------------------------------
st.markdown("---")
st.subheader("📋 Semua Rekod DO")

csv_path = "do_data.csv"
if os.path.exists(csv_path):
    try:
        df_all = pd.read_csv(csv_path)
        if not df_all.empty:
            st.dataframe(df_all, use_container_width=True)
        else:
            st.info("Tiada DO dihantar lagi.")
    except pd.errors.EmptyDataError:
        st.info("Tiada DO dihantar lagi.")
    except Exception as e:
        st.error(f"❌ Ralat membaca fail CSV: {e}")
else:
    st.info("Tiada DO dihantar lagi.")