import streamlit as st
from firebase_auth import signup_user, login_user, reset_password
from firestore_db import save_user_profile, get_user_profile

st.set_page_config(page_title="FastChain Auth", layout="centered")
st.title("🍔 FastChain - User Auth")

menu = st.sidebar.radio("Menu", ["Sign Up", "Login", "Forgot Password"])

if menu == "Sign Up":
    st.subheader("Create Account")
    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Sign Up"):
        res = signup_user(email, password)
        if "error" in res:
            st.error(res["error"]["message"])
        else:
            uid = res["localId"]
            token = res["idToken"]
            save_user_profile(uid, name, email, token)
            st.success("Account created and profile saved!")

elif menu == "Login":
    st.subheader("Login to Account")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        res = login_user(email, password)
        if "error" in res:
            st.error(res["error"]["message"])
        else:
            uid = res["localId"]
            token = res["idToken"]
            profile = get_user_profile(uid, token)
            st.success("Login successful!")
            st.write("👤 Your Profile:")
            st.json(profile.get("fields", {}))

elif menu == "Forgot Password":
    st.subheader("Reset Password")
    email = st.text_input("Email")
    if st.button("Send Reset Link"):
        res = reset_password(email)
        if "error" in res:
            st.error(res["error"]["message"])
        else:
            st.success("Reset link sent! Check your email.")
