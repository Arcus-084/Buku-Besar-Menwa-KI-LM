import streamlit as st
from supabase import create_client, Client

# 1. KONFIGURASI HALAMAN (Wajib paling atas, sebelum markdown/CSS)
st.set_page_config(
    page_title="Portal MENWA KI LM", 
    page_icon="https://ygkqeydetmlsgwmdglyk.supabase.co/storage/v1/object/public/Logo%20Orgnisasi/MENWA_KI_LM__1__page-0001-removebg-preview%20(1).png", 
    layout="centered"
)

# --- KODE PAKSA HAPUS SIDEBAR ---
st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {display: none !important;}
        [data-testid="stSidebar"] {display: none !important;}
        .main .block-container {max-width: 800px; padding-top: 2rem;}
    </style>
""", unsafe_allow_html=True)
st.markdown("""
    <style>
        /* 1. Mengubah Background Utama */
        .stApp {
            background-color: #0e1117; /* Warna gelap navy-grey */
            background-image: radial-gradient(circle at 20% 30%, #1d2b1a 0%, #0e1117 100%); /* Ada sentuhan gradasi hijau army gelap */
        }

        /* 2. Mengubah Warna Teks agar Kontras */
        h1, h2, h3, p, span {
            color: #e0e0e0 !important;
            font-family: 'Inter', sans-serif;
        }

        /* 3. Mempercantik Card/Kontainer Login */
        [data-testid="stForm"] {
            background-color: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 30px;
        }

        /* 4. Mengubah Warna Tombol agar lebih 'Komando' */
        .stButton>button {
            background-color: #2e3b23 !important; /* Hijau Army */
            color: #f1f1f1 !important;
            border-radius: 8px !important;
            border: 1px solid #4a5d3a !important;
            transition: 0.3s;
        }
        
        .stButton>button:hover {
            background-color: #3d4f2f !important;
            border-color: #ffd700 !important; /* Glow kuning emas pas di-hover */
        }
    </style>
""", unsafe_allow_html=True)

# 2. INISIALISASI SESSION STATE
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_nbp" not in st.session_state:
    st.session_state.user_nbp = None
if "menu" not in st.session_state:
    st.session_state.menu = "home" # Tambahkan ini agar tidak error saat tombol ditekan

# 3. KONEKSI SUPABASE
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)
except Exception as e:
    st.error("Konfigurasi Database (Secrets) belum lengkap.")
    st.stop()

# 4. FUNGSI LOGIKA LOGIN
def login_user(nbp, password):
    email_internal = f"{nbp}@menwa.com"
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email_internal, 
            "password": password
        })
        return response
    except Exception:
        return None

# --- LOGIKA TAMPILAN ---

# A. JIKA BELUM LOGIN
if not st.session_state.authenticated:
    # Logo Center
    st.markdown(
        """
        <div style="display: flex; justify-content: center;">
            <img src="https://ygkqeydetmlsgwmdglyk.supabase.co/storage/v1/object/public/Logo%20Orgnisasi/MENWA_KI_LM__1__page-0001-removebg-preview%20(1).png" width="150">
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<h1 style='text-align: center; margin-bottom: 0;'>Portal Resmi MENWA KI LM</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; margin-top: 0; color: grey;'>Kompi Latifah Mubarokiyah</h3>", unsafe_allow_html=True)
    
    st.write("---")
    
    # Menu Navigasi Sebelum Login
    st.write("### Informasi Umum")
    if st.button("📜 Baca Sejarah Menwa", use_container_width=True):
        st.session_state.menu = "sejarah" if st.session_state.menu != "sejarah" else "home"
    
    if st.session_state.menu == "sejarah":
        with st.expander("Klik untuk menutup Sejarah", expanded=True):
            st.title("📜 Sejarah Menwa MAHAWARMAN")
            st.markdown("""
            **Resimen Mahasiswa** (disingkat Menwa) adalah salah satu kekuatan sipil yang dilatih dan dipersiapkan untuk mempertahankan NKRI sebagai perwujudan Sistem Pertahanan dan Keamanan Rakyat Semesta (Sishankamrata). 
            
            Menwa merupakan komponen cadangan pertahanan negara yang diberikan pelatihan ilmu militer seperti penggunaan senjata, taktik pertempuran, survival, terjun payung, dan navigasi.
            """)
    
    st.write("---")

    # Form Login
    with st.container():
        st.info("Silakan login dengan Nomor Badan Pokok (NBP) Anda.")
        with st.form("login_form"):
            nbp_input = st.text_input("Nomor Badan Pokok (NBP)", placeholder="Masukkan NBP Anda")
            pass_input = st.text_input("Password", type="password")
            btn_login = st.form_submit_button("Masuk ke Sistem", use_container_width=True)
            
            if btn_login:
                nbp_clean = nbp_input.strip()
                res = login_user(nbp_clean, pass_input)
                
                if res and res.user:
                    st.session_state.authenticated = True
                    st.session_state.user_nbp = nbp_clean
                    st.success(f"Selamat bertugas, NBP {nbp_clean}!")
                    st.rerun()
                else:
                    st.error("Gagal Login. Periksa kembali NBP dan Password Anda.")

    st.write("---")
    st.caption("© 2026 Resimen Mahasiswa Mahawarman - KI LM")

# B. JIKA SUDAH LOGIN (DASHBOARD)
else:
    st.title("🚀 Dashboard Operasional")
    st.subheader(f"Selamat bertugas, NBP {st.session_state.user_nbp}")
    st.write("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📊 Administrasi")
        st.write("Kelola Buku Besar & Keuangan.")
        if st.button("Buka Buku Besar", use_container_width=True, type="primary"):
            st.switch_page("pages/1_Buku_Besar.py")
            
    with col2:
        st.markdown("### 🪖 Personil")
        st.write("Data Anggota & Struktur.")
        if st.button("Buka Profil Anggota", use_container_width=True):
            st.switch_page("pages/2_Profil_Organisasi.py")
            
    st.write("---")
    
    if st.button("🚪 Logout / Keluar"):
        st.session_state.authenticated = False
        st.session_state.user_nbp = None
        st.session_state.menu = "home"
        st.rerun()
