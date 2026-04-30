import streamlit as st
from supabase import create_client, Client
import pandas as pd

# 1. Koneksi Supabase
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

# --- FUNGSI HELPER BARU ---
def format_rupiah(nominal):
    """Mengubah angka menjadi format Rp 1.000.000"""
    return f"Rp {int(nominal):,}".replace(',', '.')

# --- DEFINISI FUNGSI ---
def get_accounts():
    try:
        response = supabase.table("accounts").select("id, account_name, account_type").execute()
        return response.data
    except Exception:
        return []

def upload_image(file):
    file_path = f"kuitansi/{file.name}"
    supabase.storage.from_("kuitansi_organisasi").upload(file_path, file.getvalue())
    return supabase.storage.from_("kuitansi_organisasi").get_public_url(file_path)

# --- TAMPILAN APLIKASI ---
st.title("Sistem Buku Besar Organisasi")

accounts_data = get_accounts()
if not accounts_data:
    st.error("Gagal mengambil data akun.")
    st.stop()

account_options = {f"{a['account_name']} ({a['account_type']})": a['id'] for a in accounts_data}

# --- BAGIAN RINGKASAN SALDO (Optional tapi Bagus) ---
recent_logs = supabase.table("transactions").select("*, accounts(account_name)").order("created_at", desc=True).execute()

if recent_logs.data:
    df_all = pd.DataFrame(recent_logs.data)
    total_masuk = df_all[df_all['type'] == 'debit']['amount'].sum()
    total_keluar = df_all[df_all['type'] == 'kredit']['amount'].sum()
    saldo_total = total_masuk - total_keluar
    
    col_s1, col_s2, col_s3 = st.columns(3)
    col_s1.metric("Total Pemasukan", format_rupiah(total_masuk))
    col_s2.metric("Total Pengeluaran", format_rupiah(total_keluar))
    col_s3.metric("Saldo Kas", format_rupiah(saldo_total))

st.divider()

# 3. Form Input Transaksi (Tetap sama)
st.subheader("Input Transaksi Baru")
with st.form("transaction_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        date = st.date_input("Tanggal Transaksi")
        amount = st.number_input("Nominal (Rp)", min_value=0, step=1000)
        evidence_file = st.file_uploader("Upload Bukti", type=['png', 'jpg', 'jpeg'])
    with col2:
        selected_account_name = st.selectbox("Pilih Kategori Akun", list(account_options.keys()))
        description = st.text_input("Keterangan/Deskripsi")
    
    submitted = st.form_submit_button("Simpan Transaksi")
    if submitted:
        # ... (Logika simpan tetap sama seperti kode kamu)
        account_id = account_options[selected_account_name]
        trans_type = "debit" if "Pemasukan" in selected_account_name else "kredit"
        image_url = upload_image(evidence_file) if evidence_file else None
        data = {"date": str(date), "description": description, "amount": amount, 
                "account_id": account_id, "type": trans_type, "evidence_url": image_url}
        response = supabase.table("transactions").insert(data).execute()
        if response.data:
            st.success(f"Berhasil mencatat!")
            st.rerun()

# 4. Tampilkan Transaksi dengan Format Rupiah
st.subheader("Catatan Terakhir")
if recent_logs.data:
    # Ambil 5 data terbaru dari DataFrame yang sudah ada
    df_display = pd.DataFrame(recent_logs.data).head(5)
    
    # Merapikan tampilan tabel
    df_display['Kategori'] = df_display['accounts'].apply(lambda x: x['account_name'])
    
    # BAGIAN PENTING: Format Kolom Amount
    df_display['Nominal (Rp)'] = df_display['amount'].apply(format_rupiah)
    
    # Menampilkan tabel dengan kolom baru
    st.table(df_display[['date', 'Kategori', 'description', 'Nominal (Rp)', 'type']])
else:
    st.info("Belum ada transaksi.")
