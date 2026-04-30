import streamlit as st

st.set_page_config(page_title="Dashboard MENWA KI LM", layout="centered")

# --- CSS UNTUK TAMPILAN BERSIH ---
st.markdown("""
    <style>
    [data-testid="stStatusWidget"] {display: none !important;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

st.title("Pusat Kendali Organisasi")
st.write("Selamat datang, silakan pilih modul di bawah:")

# Membuat Grid Tombol Besar
col1, col2 = st.columns(2)

with col1:
    st.info("### Administrasi")
    if st.button("📊 Buka Buku Besar", use_container_width=True):
        st.switch_page("pages/1_Buku_Besar.py")

with col2:
    st.success("### Personil")
    if st.button("🪖 Profil & Struktur", use_container_width=True):
        st.switch_page("pages/2_Profil_Organisasi.py")

st.divider()
st.caption("Resimen Mahasiswa Kompi Latifah Mubarokiyah")
