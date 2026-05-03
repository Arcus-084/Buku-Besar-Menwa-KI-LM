import streamlit as st
from supabase import create_client, Client

# --- KODE PAKSA HAPUS SIDEBAR ---
st.markdown("""
    <style>
        /* Menghilangkan navigasi di sidebar */
        [data-testid="stSidebarNav"] {display: none !important;}
        
        /* Menghilangkan garis pembatas sidebar (opsional) */
        [data-testid="stSidebar"] {display: none !important;}
        
        /* Menyesuaikan lebar halaman agar tetap di tengah */
        .main .block-container {max-width: 800px; padding-top: 2rem;}
    </style>
""", unsafe_allow_html=True)

# 1. KONFIGURASI HALAMAN
st.set_page_config(
    page_title="Portal MENWA KI LM", 
    page_icon="https://ygkqeydetmlsgwmdglyk.supabase.co/storage/v1/object/public/Logo%20Orgnisasi/MENWA_KI_LM__1__page-0001-removebg-preview%20(1).png", 
    layout="centered"
)

# 2. INISIALISASI SESSION STATE
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_nbp" not in st.session_state:
    st.session_state.user_nbp = None

# 3. KONEKSI SUPABASE
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)
except Exception as e:
    st.error("Konfigurasi Database (Secrets) belum lengkap.")
    st.stop()

# 4. FUNGSI LOGIKA LOGIN BERBASIS NBP
def login_user(nbp, password):
    # Mengonversi NBP menjadi format email internal secara otomatis
    email_internal = f"{nbp}@menwa.com"
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email_internal, 
            "password": password
        })
        return response
    except Exception:
        return None

# --- TAMPILAN UI ---

if not st.session_state.authenticated:
    st.markdown(
        """
        <div style="display: flex; justify-content: center;">
            <img src="https://ygkqeydetmlsgwmdglyk.supabase.co/storage/v1/object/public/Logo%20Orgnisasi/MENWA_KI_LM__1__page-0001-removebg-preview%20(1).png" width="150">
        </div>
        """,
        unsafe_allow_html=True
    )

    # Judul dan Subtitle juga dibuat center lewat CSS
    st.markdown("<h1 style='text-align: center; margin-bottom: 0;'>Portal Resmi MENWA KI LM</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; margin-top: 0; color: grey;'>Kompi Latifah Mubarokiyah</h3>", unsafe_allow_html=True)
    
    st.write("---")
    st.write("### Pilih Menu Utama")
    m1,  = st.columns(1)
    
    with m1:
        if st.button("Sejarah Menwa", use_container_width=True):
            st.session_state.menu = "sejarah"     
 
    # --- UI TAMPILAN SEJARAH ---
    if st.session_state.menu == "sejarah":
        st.title("📜 Sejarah Menwa MAHAWARMAN")
        st.markdown("""**Resimen Mahasiswa** (disingkat Menwa) adalah salah satu kekuatan sipil yang dilatih dan dipersiapkan untuk mempertahankan NKRI sebagai perwujudan Sistem Pertahanan dan Keamanan Rakyat Semesta (Sishankamrata). 
        Menwa juga merupakan salah satu komponen warga negara yang mendapat pelatihan militer (unsur mahasiswa). Markas komando satuan Menwa bertempat di perguruan tinggi di kesatuan masing-masing yang anggotanya adalah mahasiswa yang berkedudukan di kampus tersebut. 
        Menwa merupakan komponen cadangan pertahanan negara yang diberikan pelatihan ilmu militer seperti penggunaan senjata, taktik pertempuran, survival, terjun payung, bela diri militer, senam militer, penyamaran, navigasi dan sebagainya.""")
    st.write("---")
   
with st.container():
        st.info("Silakan login dengan Nomor Badan Pokok (NBP) Anda.")
        with st.form("login_form"):
            nbp_input = st.text_input("Nomor Badan Pokok (NBP)", placeholder="Masukkan NBP Anda")
            pass_input = st.text_input("Password", type="password")
            btn_login = st.form_submit_button("Masuk ke Sistem", use_container_width=True)
            
            if btn_login:
                # Menghapus spasi jika user tidak sengaja mengetiknya
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
            else:
                    # TAMPILAN DASHBOARD SETELAH LOGIN
                st.title("🚀 Dashboard Operasional")
                st.write(f"Selamat bertugas, **NBP {st.session_state.user_nbp}**")
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
                
                if st.button("Logout / Keluar"):
                    st.session_state.authenticated = False
                    st.session_state.user_nbp = None
                    st.rerun()
