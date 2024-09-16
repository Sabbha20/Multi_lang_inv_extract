from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# load model
model = genai.GenerativeModel("gemini-pro-vision")

def get_gemini_response(msg, img, user_prompt):
    res = model.generate_content(msg, img[0], user_prompt)
    return res

