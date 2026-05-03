import streamlit as st

# 1. KONFIGURASI HALAMAN (Wajib paling atas)
st.set_page_config(
    page_title="Struktur Organisasi - KI LM",
    page_icon="🪖",
    layout="centered"
)

# 2. LOGIKA STATUS LOGIN (Tanpa Proteksi Gembok)
is_authenticated = st.session_state.get("authenticated", False)
user_nama = st.session_state.get("user_nama", "Tamu Publik")
user_nbp = st.session_state.get("user_nbp", "N/A")

# 3. CSS CUSTOM
st.markdown("""
    <style>
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
        .name-title { font-size: 14px; font-weight: bold; color: #000 !important; }
        .nbp-sub { font-size: 11px; color: #444 !important; }
    </style>
""", unsafe_allow_html=True)

# 4. FUNGSI DISPLAY PERSONIL
DEFAULT_IMG = "https://ygkqeydetmlsgwmdglyk.supabase.co/storage/v1/object/public/Logo%20Orgnisasi/MENWA_KI_LM__1__page-0001-removebg-preview%20(1).png"

def display_member(jabatan, nama, nbp, foto_url=None):
    img_path = foto_url if foto_url else DEFAULT_IMG
    # Sembunyikan NBP jika bukan anggota yang login (Opsional untuk privasi)
    display_nbp = nbp if is_authenticated else "Terproteksi"
    
    st.markdown(f"""
        <div class="member-card">
            <div style="display: flex; justify-content: center; margin-bottom: 10px;">
                <img src="{img_path}" style="border-radius: 5px; border: 2px solid #808080; height: 120px; width: 100px; object-fit: cover;">
            </div>
            <div style="font-weight: 900; font-size: 13px; text-transform: uppercase; border-bottom: 1px solid #808080; margin-bottom: 5px;">{jabatan}</div>
            <div class="name-title">{nama}</div>
            <div class="nbp-sub">NBP: {display_nbp}</div>
        </div>
    """, unsafe_allow_html=True)

# 5. SIDEBAR DINAMIS
with st.sidebar:
    st.image(DEFAULT_IMG, width=100)
    if is_authenticated:
        st.markdown(f"### 🪖 Operator: \n**{user_nama}**")
        st.markdown(\n`NBP: {user_nbp}`)
        st.page_link("pages/1_Buku_Besar.py", label="Buku Besar Keuangan", icon="💰")
    else:
        st.info("Mode Publik: Akses terbatas pada informasi umum.")
    
    st.divider()
    st.page_link("main_base_apps.py", label="Kembali ke Beranda", icon="🏠")
    
    if is_authenticated:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()

# 6. KONTEN STRUKTUR (Dapat Dilihat Semua Orang)
st.markdown(
    """
    <div style="text-align: center; margin-bottom: 30px;">
        <img src="https://ygkqeydetmlsgwmdglyk.supabase.co/storage/v1/object/public/Logo%20Orgnisasi/MENWA_KI_LM__1__page-0001-removebg-preview%20(1).png" width="90">
        <h1 style='color: white; margin: 10px 0 0 0;'>STRUKTUR ORGANISASI</h1>
        <p style='color: #ffd700;'>KOMPI LATIFAH MUBAROKIYAH - TA 2025/2026</p>
    </div>
    """, unsafe_allow_html=True)

# TIER 1: DANMEN
st.markdown('<div class="tier-header">KOMANDO TERTINGGI</div>', unsafe_allow_html=True)
_, t1, _ = st.columns([1, 1.5, 1])
with t1: display_member("DANMEN", "Nama Danmen", "XX.XXX.XX")

# TIER 2: REKTOR & WAREK (KAMATRIK & KASMATRIK)
st.markdown('<div class="tier-header">PIMPINAN INSTITUSI</div>', unsafe_allow_html=True)
t2_1, t2_2 = st.columns(2)
with t2_1: display_member("KAMATRIK", "Nama Kamatrik", "XX.XXX.XX")
with t2_2: display_member("KASMATRIK", "Nama Kasmatrik", "XX.XXX.XX")

# TIER 3: PEMBINA
st.markdown('<div class="tier-header">DEWAN PEMBINA DOSEN</div>', unsafe_allow_html=True)
p1, p2, p3 = st.columns(3)
with p1: display_member("PEMBINA I", "Dosen 1", "XXXX")
with p2: display_member("PEMBINA II", "Dosen 2", "XXXX")
with p3: display_member("PEMBINA III", "Dosen 3", "XXXX")

# TIER 4: PELAKSANA
st.markdown('<div class="tier-header">UNSUR PELAKSANA</div>', unsafe_allow_html=True)
t3_1, t3_2, t3_3 = st.columns(3)
with t3_1: display_member("DANKI", "Nama Danki", "XX.XXX.XX")
with t3_2: display_member("WADANKI", "Nama Wadanki", "XX.XXX.XX")
with t3_3: display_member("PELATIH", "Nama Pelatih", "XX.XXX.XX")

# TIER 5: ANGGOTA
st.markdown('<div class="tier-header">KESATUAN ANGGOTA</div>', unsafe_allow_html=True)
m_cols = st.columns(4)
for i in range(4):
    with m_cols[i]: display_member("ANGGOTA", f"Anggota {i+1}", "XX.XXX.XX")

st.divider()
st.caption("© 2026 Menwa Mahawarman KI LM")
