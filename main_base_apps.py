import streamlit as st
from supabase import create_client, Client

# --- KONEKSI ---
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

def login_user(email, password):
    try:
        # Menghubungkan ke Supabase Auth
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        return response
    except Exception as e:
        return None

# --- UI LOGIN ---
if not st.session_state.get("authenticated"):
    st.title("🔑 Login Anggota MENWA")
    
    # --- UI LOGIN ---
with st.form("login_form"):
    # Kita ganti labelnya jadi Nomor Anggota
    nbp = st.text_input("Nomor Badan Pokok (NBP)") 
    password = st.text_input("Password", type="password")
    submit = st.form_submit_button("Masuk")

    if submit:
        # OTOMATIS TAMBAHKAN DOMAIN DI BELAKANGNYA SECARA SILENT
        email_otomatis = f"{nbp}@menwa.com" 
        
        res = login_user(email_otomatis, password)
        if res and res.user:
            st.session_state.authenticated = True
            st.session_state.user_email = nba # Simpan NRA-nya saja untuk identitas
            st.success(f"Selamat bertugas, {nbp}!")
            st.rerun()
        else:
            st.error("Email atau Password salah. Silakan hubungi Admin.")
