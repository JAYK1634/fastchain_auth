import streamlit as st
from firebase_auth import signup_user, login_user, reset_password
from firestore_db import save_user_profile, get_user_profile

st.set_page_config(page_title="StudyPal", layout="centered")
st.title("📚 StudyPal - Student Auth")

menu = st.sidebar.radio("Menu", ["Register", "Login", "Reset Password"])

if menu == "Register":
    st.subheader("📝 Register New Student")
    name = st.text_input("Full Name")
    email = st.text_input("Student Email")
    branch = st.selectbox("Branch", ["CSE", "IT", "ECE", "ME", "CE"])
    semester = st.selectbox("Semester", [f"Sem {i}" for i in range(1, 9)])
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        res = signup_user(email, password)
        if "error" in res:
            st.error(res["error"]["message"])
        else:
            uid = res["localId"]
            token = res["idToken"]
            save_user_profile(uid, name, email, token, branch, semester)
            st.success("✅ Student account created successfully!")

elif menu == "Login":
    st.subheader("🔓 Student Login")
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
            st.success("🎉 Logged in successfully!")
            st.json(profile.get("fields", {}))

elif menu == "Reset Password":
    st.subheader("🔐 Reset Password")
    email = st.text_input("Enter your registered email")
    if st.button("Send Reset Link"):
        res = reset_password(email)
        if "error" in res:
            st.error(res["error"]["message"])
        else:
            st.success("📩 Password reset email sent!")
