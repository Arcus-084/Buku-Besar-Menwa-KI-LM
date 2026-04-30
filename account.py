import streamlit as st
from supabase import create_client, Client
import pandas as pd

# 1. Koneksi Supabase
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

# --- DEFINISI FUNGSI (Harus di atas sebelum dipanggil) ---

def get_accounts():
    """Mengambil daftar kategori dari tabel accounts"""
    try:
        response = supabase.table("accounts").select("id, account_name, account_type").execute()
        return response.data
    except Exception:
        return []

def upload_image(file):
    """Upload kuitansi ke Supabase Storage"""
    file_path = f"kuitansi/{file.name}"
    # Pastikan bucket 'kuitansi_organisasi' sudah kamu buat di dashboard Supabase
    supabase.storage.from_("kuitansi_organisasi").upload(file_path, file.getvalue())
    return supabase.storage.from_("kuitansi_organisasi").get_public_url(file_path)

# --- TAMPILAN APLIKASI ---

st.title("Sistem Buku Besar Organisasi")

# Cek koneksi dan ambil data akun
accounts_data = get_accounts()

if not accounts_data:
    st.error("Gagal mengambil data akun atau tabel 'accounts' masih kosong.")
    st.stop()

# Buat mapping untuk dropdown: "Nama Akun (Tipe)"
account_options = {f"{a['account_name']} ({a['account_type']})": a['id'] for a in accounts_data}

# 3. Form Input Transaksi
st.subheader("Input Transaksi Baru")
with st.form("transaction_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    
    with col1:
        date = st.date_input("Tanggal Transaksi")
        amount = st.number_input("Nominal (Rp)", min_value=0, step=1000)
        # Tambahan: Input untuk Upload Bukti
        evidence_file = st.file_uploader("Upload Bukti Kuitansi", type=['png', 'jpg', 'jpeg'])
    
    with col2:
        selected_account_name = st.selectbox("Pilih Kategori Akun", list(account_options.keys()))
        description = st.text_input("Keterangan/Deskripsi")
    
    submitted = st.form_submit_button("Simpan Transaksi")

    if submitted:
        account_id = account_options[selected_account_name]
        trans_type = "debit" if "Pemasukan" in selected_account_name else "kredit"
        
        # Proses upload jika ada file
        image_url = None
        if evidence_file:
            image_url = upload_image(evidence_file)

        data = {
            "date": str(date),
            "description": description,
            "amount": amount,
            "account_id": account_id,
            "type": trans_type,
            "evidence_url": image_url
        }
        
        response = supabase.table("transactions").insert(data).execute()
        
        if response.data:
            st.success(f"Berhasil mencatat: {description}")
            st.rerun() # Refresh untuk melihat data terbaru
        else:
            st.error("Gagal menyimpan data.")

# 4. Tampilkan 5 Transaksi Terakhir
st.divider()
st.subheader("Catatan Terakhir")
recent_logs = supabase.table("transactions").select("*, accounts(account_name)").order("created_at", desc=True).limit(5).execute()

if recent_logs.data:
    df = pd.DataFrame(recent_logs.data)
    # Merapikan tampilan tabel
    df['Kategori'] = df['accounts'].apply(lambda x: x['account_name'])
    
    # Menampilkan tabel (hanya kolom tertentu)
    st.dataframe(
        df[['date', 'description', 'amount', 'type', 'Kategori']],
        use_container_width=True
    )