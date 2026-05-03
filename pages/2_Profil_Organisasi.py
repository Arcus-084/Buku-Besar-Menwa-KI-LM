import streamlit as st

st.set_page_config(page_title="Struktur Organisasi - KI LM", layout="wide")

# CSS Kustom: Mengambil vibes Hard File ke versi Online
st.markdown("""
    <style>
        .stApp { background-color: #000000; }
        .level-label {
            color: #ffd700;
            font-weight: bold;
            text-align: center;
            border-bottom: 1px solid #333;
            padding-bottom: 5px;
            margin-top: 30px;
            margin-bottom: 20px;
            letter-spacing: 2px;
        }
        .org-box {
            background-color: #d1d1d1;
            border-left: 5px solid #808080;
            padding: 15px;
            text-align: center;
            color: black;
            border-radius: 4px;
            margin-bottom: 15px;
        }
        .job-title {
            font-weight: 800;
            font-size: 14px;
            margin-bottom: 2px;
            font-family: 'Arial Black', sans-serif;
        }
        .member-name {
            font-size: 13px;
            color: #333;
        }
        .nbp-text {
            font-size: 11px;
            color: #555;
        }
    </style>
""", unsafe_allow_html=True)

# --- FUNGSI REUSABLE UNTUK KOTAK PERSONIL ---
def personil(jabatan, nama, nbp="-"):
    st.markdown(f"""
        <div class="org-box">
            <div class="job-title">{jabatan}</div>
            <div class="member-name">{nama}</div>
            <div class="nbp-text">NBP: {nbp}</div>
        </div>
    """, unsafe_allow_html=True)

# 1. HEADER LOGO & JUDUL
st.markdown(
    """
    <div style="display: flex; justify-content: center; align-items: center; gap: 20px;">
        <img src="https://ygkqeydetmlsgwmdglyk.supabase.co/storage/v1/object/public/Logo%20Orgnisasi/MENWA_KI_LM__1__page-0001-removebg-preview%20(1).png" width="80">
        <h2 style='color: white; margin: 0;'>STRUKTUR ORGANISASI ONLINE</h2>
    </div>
    """, unsafe_allow_html=True)

st.write("---")

# 2. TIER 1: UNSUR PEMBINA & PENASEHAT (Dosen & Senior)
st.markdown('<div class="level-label">UNSUR PEMBINA & PENASEHAT</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    personil("PEMBINA", "Nama Dosen Pembina", "NIDN. 0001XXX")
with col2:
    personil("PENASEHAT", "Nama Penasehat", "NBP. XX.XXX.XX")

# 3. TIER 2: PIMPINAN TERTINGGI (Kamatrik & Danmen)
st.markdown('<div class="level-label">PIMPINAN KOMANDO</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    personil("KAMATRIK", "Nama Kamatrik", "NBP. XX.XXX.XX")
with col2:
    personil("DANMEN", "Nama Danmen", "NBP. XX.XXX.XX")

# 4. TIER 3: STAF KOMANDO (Kasmatrik & Danki)
st.markdown('<div class="level-label">STAF & OPERASIONAL</div>', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    personil("KASMATRIK", "Nama Kasmatrik", "NBP. XX.XXX.XX")
with col2:
    personil("DANKI", "Nama Danki", "NBP. XX.XXX.XX")
with col3:
    personil("WADANKI", "Nama Wadanki", "NBP. XX.XXX.XX")

# 5. TIER 4: PELATIH & KORPS
col1, col2 = st.columns(2)
with col1:
    personil("PELATIH", "Nama Pelatih", "NBP. XX.XXX.XX")
with col2:
    personil("KORPS", "Nama Korps", "NBP. XX.XXX.XX")

# 6. TIER 5: ANGGOTA / SATUAN (Grid 4 Kolom)
st.markdown('<div class="level-label">ANGGOTA KESATUAN</div>', unsafe_allow_html=True)
cols = st.columns(4)
for i in range(8): # Contoh 8 anggota
    with cols[i % 4]:
        personil("ANGGOTA", f"Nama Anggota {i+1}", "XX.XXX.XX")

# FOOTER KEBANGGAAN KAMU
st.write("<br><br>", unsafe_allow_html=True)
st.caption("© 2026 Menwa Mahawarman KI LM")
st.caption("Developed by [Nama Kamu] | [Nama Grup]")
