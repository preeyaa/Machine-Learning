import streamlit as st
import os
import sys
import dotenv

# load environment variables
from dotenv import load_dotenv
load_dotenv()
# print(sys.executable)


import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Check if a file has been uploaded else give error
def image_uploader(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("File not uploaded")
    
    
# Based on input, image and prompt get gemini response
def get_gemini_response(input, image, prompt):
    model=genai.GenerativeModel('gemini-1.5-flash-002')
    #model=genai.GenerativeModel('gemini-1.5-vision')gemini-1.5-flash
    
    response=model.generate_content([input, image[0], prompt])
    return response.text

# Streamlit app
st.set_page_config(page_title="Food calorie calculator")

st.header("Food calorie calculator")

input=st.text_input("Input Prompt: ", key="input")

uploaded_file = st.file_uploader("Choose a image: ", type=["jpg", "jpeg", "png","jfif"])

image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Image uploaded", use_column_width=True)


submit=st.button("Calculate total calories")

input_prompt="""
You serve as an expert nutritionist where you see the food items from the given image
               and calculate the total calories, also provide the details of every food items with calories intake
               in below format

               1. Item 1 - no of calories
               2. Item 2 - no of calories
               ----
               ----
               
Not more than 20 lines.
"""

## If submit button is clicked
if submit:
    image_data=image_uploader(uploaded_file)
    response=get_gemini_response(input_prompt,image_data,input)
    st.subheader("The calorie calculator thinks as follows:")
    st.write(response)

