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
    
    with st.form("login_form"):
        email = st.text_input("Email Anggota")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Masuk ke Sistem")
        
        if submit:
            res = login_user(email, password)
            if res and res.user:
                st.session_state.authenticated = True
                st.session_state.user_email = res.user.email
                st.success("Login Berhasil!")
                st.rerun()
            else:
                st.error("Email atau Password salah. Silakan hubungi Admin.")
