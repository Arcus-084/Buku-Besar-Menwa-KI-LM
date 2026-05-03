import streamlit as st
from supabase import create_client, Client
import pandas as pd

# 1. PROTEKSI HALAMAN (Wajib paling atas)
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.warning("⚠️ Akses Terbatas! Silakan login di halaman utama menggunakan NBP.")
    if st.button("Kembali ke Login"):
        st.switch_page("main_base_apps.py")
    st.stop()

# 2. KONFIGURASI HALAMAN
st.set_page_config(
    page_title="Buku Besar - KI LM",
    page_icon="💰",
    layout="centered"
)

# 3. KONEKSI SUPABASE
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)
except Exception as e:
    st.error("Konfigurasi Database (Secrets) belum lengkap.")
    st.stop()

# 4. CSS CUSTOM (Konsisten dengan Tema Utama)
st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {display: none !important;}
        .stApp {
            background-color: #0e1117;
            background-image: radial-gradient(circle at 20% 30%, #1d2b1a 0%, #0e1117 100%);
        }
        h1, h2, h3, p, span { color: #e0e0e0 !important; font-family: 'Inter', sans-serif; }
        
        /* Gaya Kartu Metrik */
        [data-testid="stMetricValue"] { color: #ffd700 !important; font-weight: bold; }
        
        /* Mempercantik Form */
        [data-testid="stForm"] {
            background-color: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 15px;
        }
    </style>
""", unsafe_allow_html=True)

# --- FUNGSI HELPER ---
def format_rupiah(nominal):
    return f"Rp {int(nominal):,}".replace(',', '.')

def get_accounts():
    try:
        response = supabase.table("accounts").select("id, account_name, account_type").execute()
        return response.data
    except:
        return []

def upload_image(file):
    try:
        file_path = f"kuitansi/{file.name}"
        supabase.storage.from_("kuitansi_organisasi").upload(file_path, file.getvalue())
        return supabase.storage.from_("kuitansi_organisasi").get_public_url(file_path)
    except:
        return None

# --- SIDEBAR NAVIGASI ---
with st.sidebar:
    st.image("https://ygkqeydetmlsgwmdglyk.supabase.co/storage/v1/object/public/Logo%20Orgnisasi/MENWA_KI_LM__1__page-0001-removebg-preview%20(1).png", width=100)
    st.markdown(f"### 🪖 Operator Aktif\n**{st.session_state.user_nama}**\n`NBP: {st.session_state.user_nbp}`")
    st.divider()
    st.page_link("main_base_apps.py", label="Beranda", icon="🏠")
    st.page_link("pages/2_Profil_Organisasi.py", label="Struktur Organisasi", icon="📜")
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.authenticated = False
        st.switch_page("main_base_apps.py")

# --- KONTEN UTAMA ---
st.markdown("<h2 style='text-align: center;'>💰 Buku Besar Keuangan</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Kompi Latifah Mubarokiyah</p>", unsafe_allow_html=True)
st.divider()

# INISIALISASI MENU
if 'menu_internal' not in st.session_state:
    st.session_state.menu_internal = "home"

# PILIHAN MENU (Gaya Tombol Besar)
m1, m2 = st.columns(2)
with m1:
    if st.button("➕ Input Transaksi", use_container_width=True, type="primary"):
        st.session_state.menu_internal = "input"
with m2:
    if st.button("📊 Laporan Kas", use_container_width=True):
        st.session_state.menu_internal = "laporan"

st.write("<br>", unsafe_allow_html=True)

# --- LOGIKA MENU DINAMIS ---
accounts_data = get_accounts()
account_options = {f"{a['account_name']} ({a['account_type']})": a['id'] for a in accounts_data}

if st.session_state.menu_internal == "input":
    st.subheader("📝 Form Input Transaksi")
    with st.form("transaction_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            date = st.date_input("Tanggal Transaksi")
            amount = st.number_input("Nominal (Rp)", min_value=0, step=1000)
            evidence_file = st.file_uploader("Upload Bukti (Kuitansi)", type=['png', 'jpg', 'jpeg'])
        with col2:
            selected_acc = st.selectbox("Kategori Akun", list(account_options.keys()) if account_options else ["Belum ada akun"])
            description = st.text_input("Keterangan")
            
        submitted = st.form_submit_button("Simpan ke Database", use_container_width=True)
        if submitted:
            if not account_options:
                st.error("Gagal menyimpan: Tabel akun kosong.")
            else:
                acc_id = account_options[selected_acc]
                trans_type = "debit" if "Pemasukan" in selected_acc else "kredit"
                img_url = upload_image(evidence_file) if evidence_file else None
                
                payload = {
                    "date": str(date), 
                    "description": description, 
                    "amount": amount, 
                    "account_id": acc_id, 
                    "type": trans_type, 
                    "evidence_url": img_url,
                    "operator_nbp": st.session_state.user_nbp # Mencatat siapa yang input
                }
                
                resp = supabase.table("transactions").insert(payload).execute()
                if resp.data:
                    st.success(f"✅ Transaksi berhasil dicatat oleh {st.session_state.user_nama}!")

elif st.session_state.menu_internal == "laporan":
    # --- DI DALAM BAGIAN elif st.session_state.menu_internal == "laporan": ---

st.subheader("📊 Ringkasan Saldo")

# Ambil data transaksi termasuk kolom operator_nbp dan created_at
recent_logs = supabase.table("transactions").select("*, accounts(account_name)").order("created_at", desc=True).execute()

if recent_logs.data:
    df_all = pd.DataFrame(recent_logs.data)
    
    # ... (bagian metrik Saldo tetap sama) ...

    st.write("#### 📝 Riwayat Transaksi Lengkap")
    df_display = df_all.copy()
    
    # Merapikan tampilan kolom
    df_display['Kategori'] = df_display['accounts'].apply(lambda x: x['account_name'] if x else "N/A")
    df_display['Nominal'] = df_display['amount'].apply(format_rupiah)
    
    # Mengubah created_at menjadi format waktu yang enak dibaca
    df_display['Waktu Input'] = pd.to_datetime(df_display['created_at']).dt.strftime('%d/%m/%Y %H:%M')
    
    # Menampilkan tabel dengan kolom 'operator_nbp'
    st.dataframe(
        df_display[['Waktu Input', 'Kategori', 'description', 'Nominal', 'type', 'operator_nbp']],
        column_config={
            "Waktu Input": "Tanggal & Jam",
            "operator_nbp": "ID Operator (NBP)",
            "description": "Keterangan"
        },
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("Belum ada data transaksi.")

# Footer Copyright
st.write("---")
st.caption(f"Akses terverifikasi untuk: {st.session_state.user_nama} | © 2026 Menwa Mahawarman KI LM")
