from dotenv import load_dotenv
load_dotenv() ## to load all env variables

import streamlit as st
from PIL import Image

import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


st.set_page_config(page_title="Dr. Santosh Taware's Q&A")
st.header("Dr. Santosh's LLM Application")


# Approximate conversion: Assuming a DPI of around 96 (common on many screens)
cm_to_pixels = 96 / 2.54  # pixels per cm
desired_height_cm = 10
desired_height_pixels = int(desired_height_cm * cm_to_pixels)

# Load the image
try:
    image = Image.open(r"DrST.jpg")  # Use your corrected path
    # Resize the image to the desired height while maintaining aspect ratio
    original_width, original_height = image.size
    width = int(original_width * (desired_height_pixels / original_height))
    resized_image = image.resize((width, desired_height_pixels))
except FileNotFoundError:
    st.error("Image file not found. Please check the path.")
    resized_image = None

# Create columns for layout
col1, col2 = st.columns([1, 3])  # Adjust the ratios as needed

with col1:
    if resized_image:
        st.image(resized_image, use_container_width=False)  # Changed parameter name

with col2:
    st.title("About Dr. Santosh Taware")
    llm_description = """
    Dr. Santosh Taware is a distinguished expert in plant nursery management and technology. His profound knowledge spans critical areas, including advanced propagation techniques (like seeding, cuttings, and grafting), formulation of optimal growing media, and integrated pest and disease management. Dr. Taware provides valuable guidance on efficient nursery design, resource utilization (water, fertilizers), and implementing modern technologies for enhanced productivity. His expertise is instrumental in establishing and running successful nurseries, ensuring the consistent production of healthy, high-quality, and vigorous plants essential for agriculture, horticulture, and forestry. He is recognized for his practical approach and contributions to sustainable nursery practices.
    """
    st.write(llm_description)

## function load Gemini Pro model and get response
model=genai.GenerativeModel("gemini-2.0-pro-exp-02-05")
def get_gemini_response(input, image):
    if input!="":
        response=model.generate_content([input,image])
    else:
        response=model.generate_content(image)
    return response.text

input=st.text_input("Input: ", key="input")

uploaded_file = st.file_uploader("Choose an image...", type=["jgp", "jpeg", "png"])
image="" 
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image. ", use_container_width =True)
submit=st.button("Ask question to Dr. Santosh")

## When submit is clicked

if submit:
    response=get_gemini_response(input, image)
    st.write(response)
