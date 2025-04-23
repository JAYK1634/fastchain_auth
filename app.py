import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth, firestore

# Initialize Firebase with service account key
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase-key.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()

# Streamlit app layout
st.title("🍔 FastChain Restaurant - User Auth")

menu = ["Sign Up", "Login"]
choice = st.sidebar.selectbox("Menu", menu)

email = st.text_input("Email")
password = st.text_input("Password", type="password")

if choice == "Sign Up":
    name = st.text_input("Full Name")
    if st.button("Sign Up"):
        try:
            # Create user in Firebase Authentication
            user = auth.create_user(email=email, password=password, display_name=name)
            
            # Store user info in Firestore
            db.collection('users').document(user.uid).set({
                'email': email,
                'name': name
            })
            st.success("Account created! Now login to continue.")
        except Exception as e:
            st.error(f"Error: {e}")

elif choice == "Login":
    if st.button("Login"):
        try:
            # Check for user login (this is simplified for now)
            users = auth.list_users().users
            found = False
            for user in users:
                if user.email == email:
                    st.session_state['uid'] = user.uid
                    st.session_state['name'] = user.display_name
                    found = True
                    break

            if found:
                st.success(f"Welcome back {st.session_state['name']}!")

                # Edit Profile Section
                new_name = st.text_input("New Name", value=st.session_state['name'])
                new_email = st.text_input("New Email", value=email)

                if st.button("Update Info"):
                    # Update Firebase Authentication and Firestore
                    auth.update_user(st.session_state['uid'], email=new_email, display_name=new_name)
                    db.collection('users').document(st.session_state['uid']).update({
                        'name': new_name,
                        'email': new_email
                    })
                    st.success("Profile updated!")
                    st.session_state['name'] = new_name
                    st.session_state['email'] = new_email
            else:
                st.warning("User not found!")
        except Exception as e:
            st.error(f"Error: {e}")
