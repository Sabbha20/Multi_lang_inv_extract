from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai
import io


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# load model
model = genai.GenerativeModel("gemini-1.5-flash")

def get_gemini_response(msg, img, user_prompt):
    prompt = f"{msg}\n\nUser Query: {user_prompt}"
    return model.generate_content([prompt, img[0]]).text
    

def img_details(img):
    if img is not None:
        # Convert PIL Image to bytes
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format=img.format)
        byte_data = img_byte_arr.getvalue()
        
        img_parts = [
            { 
             "mime_type": f"image/{img.format.lower()}", 
             "data": byte_data
             }
        ]
        return img_parts
    else:
        raise FileNotFoundError("File not uploaded...")


# App structure
st.set_page_config("Multilanguage Invoice Extractor")

st.header("Multilanguage Invoice Extractor")

user_input = st.text_input("Extract information...", key="msg")
uploaded_file = st.file_uploader("Choose your invoice file...", type=["jpg", "jpeg", "png"])

image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption=image.filename, use_column_width=True)

submit = st.button("Enter...")

msg = """
You are an expert in understanding invoices. We will upload a invoice image 
and you will answer the question based on the uploaded invoice
"""

if submit:
    img_data = img_details(image)
    response = get_gemini_response(msg, img_data, user_input)
    st.subheader("Output:")
    st.write(response)


