import streamlit as st
from supabase import create_client, Client

# 1. KONFIGURASI HALAMAN (Wajib di baris pertama)
st.set_page_config(
    page_title="Portal MENWA KI LM", 
    page_icon="🪖", 
    layout="centered"
)

# 2. INISIALISASI SESSION STATE
# Agar status login tetap terjaga saat pindah halaman
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_nra" not in st.session_state:
    st.session_state.user_nra = None

# 3. KONEKSI SUPABASE
# Pastikan sudah setting di Streamlit Cloud Secrets
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)
except Exception as e:
    st.error("Konfigurasi Database (Secrets) belum lengkap.")
    st.stop()

# 4. FUNGSI LOGIKA LOGIN
def login_user(nra, password):
    # Mengonversi NRA menjadi format email internal Supabase secara otomatis
    email_internal = f"{nra}@menwa.com"
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email_internal, 
            "password": password
        })
        return response
    except Exception:
        return None

# --- TAMPILAN UI ---

# JIKA BELUM LOGIN (Halaman Depan / Public Area)
if not st.session_state.authenticated:
    st.title("🪖 Portal Resmi MENWA KI LM")
    st.subheader("Kompi Latifah Mubarokiyah - Resimen Mahasiswa")
    
    st.write("---")
    
    # Form Login di Sidebar atau Tengah
    with st.container():
        st.info("Silakan login dengan Nomor Anggota untuk mengakses administrasi.")
        with st.form("login_form"):
            nra_input = st.text_input("Nomor Registrasi Anggota (NRA)", placeholder="Contoh: 2024.001")
            pass_input = st.text_input("Password", type="password")
            btn_login = st.form_submit_button("Masuk ke Sistem", use_container_width=True)
            
            if btn_login:
                res = login_user(nra_input, pass_input)
                if res and res.user:
                    st.session_state.authenticated = True
                    st.session_state.user_nra = nra_input
                    st.success(f"Selamat bertugas, {nra_input}!")
                    st.rerun()
                else:
                    st.error("Akses ditolak. NRA atau Password salah.")

    st.write("")
    st.caption("© 2026 Resimen Mahasiswa Mahawarman - KI LM")

# JIKA SUDAH LOGIN (Dashboard Utama)
else:
    st.title("🚀 Dashboard Utama")
    st.write(f"Selamat datang kembali, **{st.session_state.user_nra}**")
    st.write("---")

    # Layout Tombol Navigasi Besar
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📊 Keuangan")
        st.write("Input dan pantau saldo Buku Besar.")
        if st.button("Buka Buku Besar", use_container_width=True, type="primary"):
            st.switch_page("pages/1_Buku_Besar.py")

    with col2:
        st.markdown("### 🪖 Personil")
        st.write("Lihat struktur organisasi & profil.")
        if st.button("Buka Profil", use_container_width=True):
            st.switch_page("pages/2_Profil_Organisasi.py")

    st.write("---")
    
    # Tombol Logout
    if st.button("Keluar dari Sistem"):
        st.session_state.authenticated = False
        st.session_state.user_nra = None
        st.rerun()
