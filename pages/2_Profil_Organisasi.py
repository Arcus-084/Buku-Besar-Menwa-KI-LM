import streamlit as st

# 1. PROTEKSI HALAMAN (Wajib paling atas)
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.warning("⚠️ Akses Terbatas! Silakan login di halaman utama menggunakan NBP.")
    if st.button("Kembali ke Login"):
        st.switch_page("main_base_apps.py")
    st.stop()

# 2. KONFIGURASI HALAMAN
st.set_page_config(
    page_title="Struktur Organisasi - KI LM",
    page_icon="🪖",
    layout="centered"
)

# 3. CSS CUSTOM (Tema Hard File Online & Sidebar Hider)
st.markdown("""
    <style>
        /* Menghilangkan navigasi default sidebar */
        [data-testid="stSidebarNav"] {display: none !important;}
        
        .stApp { background-color: #0e1117; }
        
        .tier-header {
            color: #ffd700;
            font-weight: bold;
            text-align: center;
            padding: 10px;
            margin-top: 40px;
            border-bottom: 2px solid #2e3b23;
            letter-spacing: 3px;
            font-family: 'Arial Black', sans-serif;
        }

        .member-card {
            background-color: #d1d1d1;
            border-left: 8px solid #2e3b23;
            padding: 20px;
            text-align: center;
            color: #000000;
            border-radius: 4px;
            margin-bottom: 20px;
            min-height: 180px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            box-shadow: 0px 4px 15px rgba(0,0,0,0.5);
        }

        .photo-container img {
            border-radius: 5px;
            border: 2px solid #808080;
            object-fit: cover;
            margin-bottom: 10px;
            height: 120px;
            width: 100px;
        }

        .role-title {
            font-weight: 900;
            font-size: 13px;
            text-transform: uppercase;
            border-bottom: 1px solid #808080;
            margin-bottom: 5px;
        }

        .name-title { font-size: 14px; font-weight: bold; color: #000 !important; }
        .nbp-sub { font-size: 11px; color: #444 !important; }
    </style>
""", unsafe_allow_html=True)

# 4. FUNGSI DISPLAY PERSONIL
DEFAULT_IMG = "https://ygkqeydetmlsgwmdglyk.supabase.co/storage/v1/object/public/Logo%20Orgnisasi/MENWA_KI_LM__1__page-0001-removebg-preview%20(1).png"

def display_member(jabatan, nama, nbp, foto_url=None):
    img_path = foto_url if foto_url else DEFAULT_IMG
    st.markdown(f"""
        <div class="member-card">
            <div class="photo-container">
                <img src="{img_path}">
            </div>
            <div class="role-title">{jabatan}</div>
            <div class="name-title">{nama}</div>
            <div class="nbp-sub">NBP: {nbp}</div>
        </div>
    """, unsafe_allow_html=True)

# 5. SIDEBAR DINAMIS
with st.sidebar:
    st.image(DEFAULT_IMG, width=100)
    st.markdown(f"### 🪖 Operator Aktif\n**{st.session_state.user_nama}**\n`NBP: {st.session_state.user_nbp}`")
    st.divider()
    st.page_link("main_base_apps.py", label="Kembali ke Beranda", icon="🏠")
    st.page_link("pages/1_Buku_Besar.py", label="Buku Besar Keuangan", icon="💰")
    if st.button("🚪 Keluar Sistem", use_container_width=True):
        st.session_state.authenticated = False
        st.switch_page("main_base_apps.py")

# 6. HEADER UTAMA
st.markdown(
    """
    <div style="display: flex; justify-content: center; align-items: center; gap: 25px; margin-bottom: 30px;">
        <img src="https://ygkqeydetmlsgwmdglyk.supabase.co/storage/v1/object/public/Logo%20Orgnisasi/MENWA_KI_LM__1__page-0001-removebg-preview%20(1).png" width="90">
        <div>
            <h1 style='color: white; margin: 0;'>STRUKTUR ORGANISASI</h1>
            <p style='color: #ffd700; margin: 0;'>KOMPI LATIFAH MUBAROKIYAH - TA 2025/2026</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 7. SUSUNAN HIERARKI

# TIER 1: PUNCAK KOMANDO
st.markdown('<div class="tier-header">KOMANDO TERTINGGI</div>', unsafe_allow_html=True)
_, t1_mid, _ = st.columns([1, 1.5, 1])
with t1_mid:
    display_member("DANMEN", "Nama Danmen", "NBP. XX.XXX.XX")

# TIER 2: PIMPINAN SATUAN (REKTOR & WAREK)
st.markdown('<div class="tier-header">PIMPINAN INSTITUSI (KAMATRIK & KASMATRIK)</div>', unsafe_allow_html=True)
t2_c1, t2_c2 = st.columns(2)
with t2_c1:
    display_member("KAMATRIK (REKTOR IAILM)", "Nama Rektor", "NBP. XX.XXX.XX")
with t2_c2:
    display_member("KASMATRIK (WAREK 3 STIELM)", "Nama Warek 3", "NBP. XX.XXX.XX")

# TIER 3: DEWAN PEMBINA (UNSUR DOSEN)
st.markdown('<div class="tier-header">STAF PEMBINA (UNSUR DOSEN)</div>', unsafe_allow_html=True)
p_col1, p_col2, p_col3 = st.columns(3)
with p_col1:
    display_member("PEMBINA I", "Dosen Pembina 1", "NIDN. XXXX")
with p_col2:
    display_member("PEMBINA II", "Dosen Pembina 2", "NIDN. XXXX")
with p_col3:
    display_member("PEMBINA III", "Dosen Pembina 3", "NIDN. XXXX")

# TIER 4: UNSUR PELAKSANA
st.markdown('<div class="tier-header">UNSUR PELAKSANA</div>', unsafe_allow_html=True)
t3_c1, t3_c2, t3_c3 = st.columns(3)
with t3_c1:
    display_member("DANKI", "Nama Danki", "NBP. XX.XXX.XX")
with t3_c2:
    display_member("WADANKI", "Nama Wadanki", "NBP. XX.XXX.XX")
with t3_c3:
    display_member("PELATIH", "Nama Pelatih", "NBP. XX.XXX.XX")

# TIER 5: ANGGOTA (Grid)
st.markdown('<div class="tier-header">KESATUAN ANGGOTA</div>', unsafe_allow_html=True)
m_cols = st.columns(4)
for i in range(4):
    with m_cols[i]:
        display_member("ANGGOTA", f"Nama Anggota {i+1}", "XX.XXX.XX")

# 8. FOOTER
st.write("<br><br>", unsafe_allow_html=True)
st.divider()
st.caption("Akses terverifikasi untuk: " + st.session_state.user_nama)
st.caption("© 2026 Resimen Mahasiswa Mahawarman - KI LM | Developed by Muhammad Dani Setiawan")
