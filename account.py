import streamlit as st
from supabase import create_client, Client
import pandas as pd

# 1. Koneksi Supabase
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Buku Besar MENWA KI LM", layout="centered")

st.markdown(
    """
    <style>
    /* 1. Sembunyikan elemen standar */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden !important;}
    header {visibility: hidden !important;}
    
    /* 2. Sembunyikan Toolbar Pojok Kanan Bawah */
    [data-testid="stStatusWidget"] {
        display: none !important;
    }

    /* 3. TRIK UTAMA: Menimpa Footer Streamlit */
    /* Kita buat kotak penutup di bagian paling bawah layar */
    .stApp::after {
        content: "";
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 50px; /* Sesuaikan tinggi untuk menutup bar sponsor */
        background-color: #0E1117; /* Ganti dengan warna background aplikasi kamu */
        z-index: 999999;
    }

    /* 4. Menyesuaikan layout agar konten tidak tertutup kotak penutup */
    .stApp {
        margin-bottom: 50px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Inisialisasi status aplikasi (Splash Screen & Navigasi)
if 'auth' not in st.session_state:
    st.session_state.auth = False
if 'menu' not in st.session_state:
    st.session_state.menu = "home"

# --- FUNGSI HELPER ---
def format_rupiah(nominal):
    return f"Rp {int(nominal):,}".replace(',', '.')

def get_accounts():
    try:
        response = supabase.table("accounts").select("id, account_name, account_type").execute()
        return response.data
    except Exception:
        return []

def upload_image(file):
    try:
        file_path = f"kuitansi/{file.name}"
        supabase.storage.from_("kuitansi_organisasi").upload(file_path, file.getvalue())
        return supabase.storage.from_("kuitansi_organisasi").get_public_url(file_path)
    except:
        return None

# --- LOGIKA TAMPILAN ---

# A. SPLASH SCREEN (Tampilan Pertama Kali Buka)
if not st.session_state.auth:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    col_logo1, col_logo2, col_logo3 = st.columns([1, 2, 1])
    
    with col_logo2:
        # GANTI URL INI dengan link logo MENWA KI LM kamu
        logo_url = "https://ygkqeydetmlsgwmdglyk.supabase.co/storage/v1/object/public/Logo%20Orgnisasi/MENWA_KI_LM__1__page-0001-removebg-preview%20(1).png" 
        st.image(logo_url, use_container_width=True)
        st.markdown("<h2 style='text-align: center;'>Buku Besar Digital</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Resimen Mahasiswa Kompi Latifah Mubarokiyah</p>", unsafe_allow_html=True)
        
        if st.button("Masuk ke Sistem", use_container_width=True):
            st.session_state.auth = True
            st.rerun()

# B. MAIN APP (Tampilan Setelah Klik Masuk)
else:
    # Header: Logo pindah ke pojok kiri atas
    head_1, head_2 = st.columns([1, 6])
    with head_1:
        st.image("https://ygkqeydetmlsgwmdglyk.supabase.co/storage/v1/object/public/Logo%20Orgnisasi/MENWA_KI_LM__1__page-0001-removebg-preview%20(1).png", width=80)
    with head_2:
        st.subheader("MENWA Mahawarman KI LM")

    st.divider()

    # PILIHAN MENU UTAMA
    st.write("### Pilih Menu Utama")
    m1, m2 = st.columns(2)
    
    with m1:
        if st.button("➕ Input Saldo Baru", use_container_width=True):
            st.session_state.menu = "input"
    with m2:
        if st.button("📊 Catatan Terakhir", use_container_width=True):
            st.session_state.menu = "laporan"

    st.divider()

    # --- KONTEN DINAMIS BERDASARKAN PILIHAN MENU ---
    
    accounts_data = get_accounts()
    account_options = {f"{a['account_name']} ({a['account_type']})": a['id'] for a in accounts_data}

    # HALAMAN INPUT
    if st.session_state.menu == "input":
        st.subheader("Form Input Transaksi Baru")
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
                account_id = account_options[selected_account_name]
                trans_type = "debit" if "Pemasukan" in selected_account_name else "kredit"
                image_url = upload_image(evidence_file) if evidence_file else None
                data = {"date": str(date), "description": description, "amount": amount, 
                        "account_id": account_id, "type": trans_type, "evidence_url": image_url}
                response = supabase.table("transactions").insert(data).execute()
                if response.data:
                    st.success("✅ Berhasil mencatat!")
        
        if st.button("⬅️ Kembali ke Home"):
            st.session_state.menu = "home"
            st.rerun()

    # HALAMAN LAPORAN
    elif st.session_state.menu == "laporan":
        st.subheader("Ringkasan Saldo & Riwayat")
        
        recent_logs = supabase.table("transactions").select("*, accounts(account_name)").order("created_at", desc=True).execute()

        if recent_logs.data:
            df_all = pd.DataFrame(recent_logs.data)
            # Metrik Saldo
            total_masuk = df_all[df_all['type'] == 'debit']['amount'].sum()
            total_keluar = df_all[df_all['type'] == 'kredit']['amount'].sum()
            
            s1, s2, s3 = st.columns(3)
            s1.metric("Pemasukan", format_rupiah(total_masuk))
            s2.metric("Pengeluaran", format_rupiah(total_keluar))
            s3.metric("Saldo Akhir", format_rupiah(total_masuk - total_keluar))
            
            st.write("#### 5 Transaksi Terakhir")
            df_display = df_all.head(5)
            df_display['Kategori'] = df_display['accounts'].apply(lambda x: x['account_name'])
            df_display['Nominal (Rp)'] = df_display['amount'].apply(format_rupiah)
            st.table(df_display[['date', 'Kategori', 'description', 'Nominal (Rp)', 'type']])
        
        if st.button("⬅️ Kembali ke Home"):
            st.session_state.menu = "home"
            st.rerun()
