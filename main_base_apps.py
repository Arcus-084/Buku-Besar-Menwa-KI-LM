import streamlit as st
from supabase import create_client, Client

# 1. KONFIGURASI HALAMAN
st.set_page_config(
    page_title="Portal Resmi MENWA KI LM", 
    page_icon="https://ygkqeydetmlsgwmdglyk.supabase.co/storage/v1/object/public/Logo%20Orgnisasi/MENWA_KI_LM__1__page-0001-removebg-preview%20(1).png", 
    layout="centered"
)

# 2. INISIALISASI SESSION STATE
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_nbp" not in st.session_state:
    st.session_state.user_nbp = None
if "user_nama" not in st.session_state:
    st.session_state.user_nama = None
if "show_login" not in st.session_state:
    st.session_state.show_login = False

# 3. KONEKSI SUPABASE
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)
except Exception as e:
    st.error("Konfigurasi Database belum lengkap di Secrets.")
    st.stop()

# 4. CSS CUSTOM (Gabungan Tema Gelap & Marquee)
st.markdown("""
    <style>
        /* Sembunyikan Sidebar Default untuk Publik */
        [data-testid="stSidebarNav"] {display: none !important;}
        
        .stApp {
            background-color: #0e1117;
            background-image: radial-gradient(circle at 20% 30%, #1d2b1a 0%, #0e1117 100%);
        }
        
        h1, h2, h3, p, span { color: #e0e0e0 !important; font-family: 'Inter', sans-serif; }

        /* Marquee Style */
        .marquee-box {
            background-color: rgba(46, 59, 35, 0.5); 
            padding: 10px; 
            border-radius: 5px; 
            border-left: 5px solid #ffd700;
            margin: 20px 0;
        }

        /* Card Login */
        [data-testid="stForm"] {
            background-color: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 15px;
        }

        /* Tombol Komando */
        .stButton>button {
            background-color: #2e3b23 !important;
            color: #f1f1f1 !important;
            border-radius: 8px !important;
            transition: 0.3s;
        }
        .stButton>button:hover {
            border-color: #ffd700 !important;
            color: #ffd700 !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR (DINAMIS) ---
with st.sidebar:
    st.markdown("### 🪖 Menu Navigasi")
    st.page_link("main_base_apps.py", label="Beranda", icon="🏠")
    st.page_link("pages/2_Profil_Organisasi.py", label="Struktur Organisasi", icon="📜")
    
    if st.session_state.authenticated:
        st.write("---")
        st.markdown("### 🔐 Internal Komando")
        st.page_link("pages/1_Buku_Besar.py", label="Buku Besar Keuangan", icon="💰")
        if st.button("🚪 Keluar Sistem", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()

# --- TAMPILAN UTAMA ---

# A. Header Logo (Tiga Logo)
st.markdown(
    """
    <div style="display: flex; justify-content: center; align-items: center; gap: 20px; margin-bottom: 20px;">
        <img src="https://ygkqeydetmlsgwmdglyk.supabase.co/storage/v1/object/public/Logo%20Orgnisasi/Institut%20Agama%20Islam%20Latifah%20Mubarokiyah,%20Pondok%20Pesantren%20Suryalaya%20Tasikmalaya.png" width="65">
        <img src="https://ygkqeydetmlsgwmdglyk.supabase.co/storage/v1/object/public/Logo%20Orgnisasi/MENWA_KI_LM__1__page-0001-removebg-preview%20(1).png" width="100">
        <img src="https://ygkqeydetmlsgwmdglyk.supabase.co/storage/v1/object/public/Logo%20Orgnisasi/Sekolah%20Tinggi%20Ilmu%20Ekonomi%20Latifah%20Mubarokiyah.png" width="65">
    </div>
    """, unsafe_allow_html=True)

# B. Marquee
st.markdown("""
    <div class="marquee-box">
        <marquee scrollamount="7" style="color: #ffd700; font-weight: bold;">
            WIDYA CASTRENA DHARMA SIDDHA — SELAMAT DATANG DI PORTAL RESMI MENWA MAHAWARMAN KOMPI LATIFAH MUBAROKIYAH — BERSAMA KITA KUAT, MENGABDI UNTUK NEGERI!
        </marquee>
    </div>
""", unsafe_allow_html=True)
st.markdown("""
    <div style="background-color: #000000; padding: 10px; border-radius: 5px; border-top: 3px solid #ffd700; border-bottom: 3px solid #ffd700; margin-bottom: 25px;">
        <marquee scrollamount="8" style="color: #ffd700; font-weight: bold; font-family: 'Courier New', Courier, monospace; letter-spacing: 1px;">
            [ BREAKING NEWS ] >>> PENERIMAAN ANGGOTA BARU MENWA KI LM TA 2026/2027 >>> WIDYA CASTRENA DHARMA SIDDHA >>> TUNJUKKAN BAKTIMU PADA NUSA DAN BANGSA SEKARANG JUGA! <<< [ BREAKING NEWS ]
        </marquee>
    </div>
""", unsafe_allow_html=True)
# C. Judul
st.markdown("<h1 style='text-align: center;'>Portal Resmi MENWA KI LM</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: grey;'>Batalyon VIII/Tarumanagara</h3>", unsafe_allow_html=True)
st.write("---")

# D. Konten Berdasarkan Status Login
if not st.session_state.authenticated:
    # --- BAGIAN INFORMASI PUBLIK (Tambahkan di app.py / main_base_apps.py) ---

    st.write("### 📚 Informasi Publik")
    
    # 1. Sejarah Menwa
    with st.expander("📜 Sejarah Menwa Mahawarman"):
        st.markdown("""
        **Resimen Mahasiswa** (disingkat Menwa) adalah salah satu kekuatan sipil yang dilatih dan dipersiapkan untuk mempertahankan NKRI sebagai perwujudan Sistem Pertahanan dan Keamanan Rakyat Semesta (Sishankamrata). 
        Menwa juga merupakan salah satu komponen warga negara yang mendapat pelatihan militer (unsur mahasiswa). Markas komando satuan Menwa bertempat di perguruan tinggi di kesatuan masing-masing yang anggotanya adalah mahasiswa yang berkedudukan di kampus tersebut. 
        Anggota Menwa sendiri akan diberikan dan dibekali pelatihan ilmu militer seperti penggunaan senjata, taktik pertempuran, survival, terjun payung, bela diri militer, senam militer, penyamaran, navigasi dan sebagainya.
        """)

    # Penerimaan CAMEN
    with st.expander("📢 DETAIL PENDAFTARAN ANGGOTA BARU"):
        st.markdown("""
        ### 🛡️ Open Recruitment 2026
        Jadilah bagian dari Resimen Mahasiswa Mahawarman Kompi Latifah Mubarokiyah!
        
        **Persyaratan Umum:**
        1. Sukarela
        2. Merupakan Mahasiswa/i aktif kampus STIE & IAI Latifah Mubarokiyah
        3. Sehat Jasmani dan Rohani
        4. Beriman dan Bertaqwa Kepada Tuhan Yang Maha Esa
        
        **Cara Mendaftar:**
        * Silakan ambil formulir di Mako Menwa KI LM.
        * Atau hubungi kontak person: **[Nomor WA/Kontak]**
        
        *Penyempurnaan Pengabdian dengan Ilmu Pengetahuan dan Ilmu Keprajuritan!*
        """)
        # Jika ada link Google Form, bisa tambahkan tombol:
        st.link_button("Daftar Online Sekarang", "https://link-gform-kamu.com")
    
    # 2. Panca Dharma Satya & Mars
    col_info1, col_info2 = st.columns(2)
    with col_info1:
        with st.expander("🛡️ Panca Dharma Satya"):
            st.info("""
            1. Kami adalah Mahasiswa warga negara Negara Kesatuan Republik Indonesia yang berdasarkan Pancasila
            2. Kami adalah Mahasiswa yang sadar akan tanggung jawab serta kehormatan akan pembelaan negara dan tidak mengenal menyerah
            3. Kami putra Indonesia yang berjiwa kesatria dan bertaqwa kepa Tuhan Yang Maha Esa serta membela kejujuran, kebenaran dan keadilan
            4. Kami adalah Mahasiswa yang menjunjung tinggi nama kehormatan Garba Ilmiah dan sadar akan hari depan Bangsa dan Negara
            5. Kami adalah Mahasiswa yang memegang teguh disiplin lahir dan bathin, percaya pada diri sendiri dan mengutamakan kepentingan nasional diatas kepentingan pribadi maupun golongan
            """)
    
    with col_info2:
        with st.expander("🎶 Mars Mahawarman"):
            st.markdown("""
            **Lirik Mars Mahawarman:**
            
            *Hai Satukanlah, padukanlah
            Senantiasa Langkah Kita
            Menuju Cita, Membangun Bangsa
            Tanpa Pamrih Berbakti 'Tuk Negara*
            
            *Hai Tunjukanlah Pengabdian
            dan Kembangkanlah Citra
            di Masyarakat, Setiap Saat
            Amalkanlah Ilmu yang Bermanfaat*
            
            *Panca Dharma Satyalah Tekad Kita
            dalam Mahawarman Kita di Bina
            dengan Berlandaskan Jiwa Pancasila
            Siap Menunjang Pola Hankamrata*
            
            *Hai Kobarkanlah, Kerahkanlah
            Semangat K'Satria
            Mari Berjuang, Terus Berjuang
            Jayalah Mahawarman Sepanjang Masa*
            
            *Panca Dharma Satyalah Tekad Kita
            dalam Mahawarman Kita di Bina
            dengan Berlandaskan Jiwa Pancasila
            Siap Menunjang Pola Hankamrata*
            
            *Hai Kobarkanlah, Kerahkanlah
            Semangat K'Satria
            Mari Berjuang, Terus Berjuang
            Jayalah Mahawarman Sepanjang Masa*
            """)
            audio_link = "https://ygkqeydetmlsgwmdglyk.supabase.co/storage/v1/object/public/Logo%20Orgnisasi/MARS%20MAHAWARMAN%202022%20-%20Hendrik%20Hapu%20Hinggiranja.mp3" 
            st.audio(audio_link, format="audio/mp3")
    
    # 3. Tugas dan Jabatan
    with st.expander("🪖 Tugas & Tanggung Jawab Jabatan"):
        st.markdown("""
        | Jabatan | Tugas Pokok |
        | :--- | :--- |
        | **DANMEN** | Pemimpin tertinggi operasi dan koordinasi resimen. |
        | **KAMATRIK** | Pembina teknis dan administratif di tingkat institusi. |
        | **DANKI** | Pemimpin operasional di tingkat Kompi. |
        | **STAF** | Pendukung administrasi, logistik, dan personel. |
        """)
    
    # E. FOOTER & PINTU LOGIN RAHASIA
    st.write("<br><br><br>", unsafe_allow_html=True)
    st.write("---")
    _, col_login, _ = st.columns([1, 2, 1])
    
    with col_login:
        if st.button("Sistem Manajemen Internal", type="secondary", use_container_width=True):
            st.session_state.show_login = not st.session_state.show_login

    if st.session_state.show_login:
        with st.form("form_login"):
            st.info("Otentikasi Personil (Gunakan NBP)")
            nbp_in = st.text_input("NBP", placeholder="Contoh: 2026.XX.XXX")
            pass_in = st.text_input("Password", type="password")
            if st.form_submit_button("Masuk", use_container_width=True):
                # Logika cek ke tabel data_anggota
                try:
                    res = supabase.table("data_anggota").select("*").eq("nbp", nbp_in).execute()
                    if res.data and res.data[0]['password'] == pass_in:
                        st.session_state.authenticated = True
                        st.session_state.user_nbp = nbp_in
                        st.session_state.user_nama = res.data[0]['nama']
                        st.session_state.show_login = False
                        st.success(f"Selamat bertugas, {res.data[0]['nama']}!")
                        st.rerun()
                    else:
                        st.error("Kredensial salah atau tidak terdaftar.")
                except:
                    st.error("Terdapat gangguan koneksi, harap tekan tombol masuk 1 kali lagi")

else:
    # --- TAMPILAN DASHBOARD (SETELAH LOGIN) ---
    st.success(f"✅ Terkoneksi sebagai: {st.session_state.user_nama} ({st.session_state.user_nbp})")
    
    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.markdown("#### 💰 Keuangan")
            st.write("Akses Buku Besar Kompi.")
            if st.button("Buka Buku Besar", use_container_width=True):
                st.switch_page("pages/1_Buku_Besar.py")
                
    with col2:
        with st.container(border=True):
            st.markdown("#### 🪖 Personil")
            st.write("Lihat Struktur Organisasi.")
            if st.button("Lihat Struktur", use_container_width=True):
                st.switch_page("pages/2_Profil_Organisasi.py")

st.write("<br>", unsafe_allow_html=True)
st.caption("© 2026 Resimen Mahasiswa Mahawarman - KI LM")
st.caption("Developed by M. Dani. Setiawan | Cordevia Familia")
