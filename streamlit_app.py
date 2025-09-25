import streamlit as st
import requests
import base64

# -------------------
# CONFIG
# -------------------
API_URL = "https://api.stability.ai/v2beta/stable-image/generate/core"
API_KEY = "YOUR_API_KEY"   # 🔑 Replace with your Stability AI key

# -------------------
# STREAMLIT SETTINGS
# -------------------
st.set_page_config(
    page_title="Malayali AI Image Generator",
    page_icon="🎨",
    layout="centered"
)

st.title("🎨 Malayali AI Image Generator")
st.caption("Crafted by **Hdx Jpg**")

# -------------------
# LOGIN
# -------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.subheader("🔐 Login Required")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if email == "hdxjpg@gmail.com" and password == "AMAN2014":
            st.session_state.logged_in = True
            st.success("✅ Logged in successfully!")
            st.experimental_rerun()
        else:
            st.error("❌ Invalid credentials")
    st.stop()

# -------------------
# IMAGE GENERATION
# -------------------
st.success("Welcome Admin! You can now generate images.")

prompt = st.text_area("Enter your prompt:", placeholder="Type in Malayalam, English, Math symbols...")

if st.button("Generate Image"):
    if not prompt:
        st.warning("⚠️ Please enter a prompt.")
    else:
        with st.spinner("🎨 Generating image..."):
            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Accept": "application/json"
            }
            data = {
                "prompt": prompt,
                "output_format": "png"
            }
            try:
                response = requests.post(API_URL, headers=headers, files={"none": ''}, data=data)

                if response.status_code == 200:
                    result = response.json()

                    if "image" in result:  # Base64 output
                        img_data = base64.b64decode(result["image"])
                        st.image(img_data, caption="Generated Image", use_container_width=True)

                    elif "image_url" in result:  # Direct URL output
                        st.image(result["image_url"], caption="Generated Image", use_container_width=True)

                    else:
                        st.error("⚠️ No image returned from API.")

                else:
                    st.error(f"API Error: {response.text}")

            except Exception as e:
                st.error(f"⚠️ Failed to connect: {e}")
