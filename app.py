#1. i need to have field to put my job description
#2. upload pdf
#3. pdf ti image --> processsing --> ask gemini
#4. create prompt template (multiple prompts)

from dotenv import load_dotenv

load_dotenv()

import io
import base64

import streamlit as st
import os
from PIL import Image
import pdf2image
import google.generativeai as genai

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content([prompt, pdf_content[0], input])
    return response.text

def input_pdf_setup(uploaded_file):
    #converting the pdf to image
    if uploaded_file is not None:

        images = pdf2image.convert_from_bytes(uploaded_file.read())
        
        first_page = images[0]

        #converting the image into bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type" : "image/jpeg",
                "data" : base64.b64encode(img_byte_arr).decode() #encoding to base64
            }
        ]

        return pdf_parts
    
    else:
        raise FileNotFoundError("No file uploaded")

## Streamlit App

st.set_page_config(page_title="ATS - Job Description Analyzer")
st.header("ATS Tracking System")

#can use text area instead of text data as job desciptions are generally long
input_text = st.text_area("Enter your Job Description here:", key = "input")
uploaded_file = st.file_uploader("Upload your Resume (PDF format only)")

if uploaded_file is not None:
    st.write("Resume uploaded successfully!")

#Creating buttons in the streamlit app

submit1 = st.button("Tell me about my Resume")
submit2 = st.button("Percentage Match")

#we need to create input prompts so that the ai can ans accordingly when we click button

#basically write prompts inside!
input_prompts1 = """
You are an expert job recruiter. Analyze the resume provided and give a detailed summary
of the candidate's qualifications, skills, and experience in relation to the job description.
highlight strengths and weaknesses of applicant in relation to the Job description. 400 
words maximum.
"""

input_prompts2 = """
Your are a skilled ATS (APPLICATION TRACKING SYSTEM) specialist with 20 years of
experience and deep ATS functionality. Compare the 
resume provided with the job description AND OUTPUT the percentage match
between the resume and job description. Give the percentage on top (big and bolded)
and then a brief explanation of why you gave that percentage. Use bullet points
and maximum 50 words.
"""


if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompts1, pdf_content,input_text)
        st.subheader("The response is")
        st.write(response)
    else:
        st.write("Please upload your resume in pdf to proceed.")

elif submit2:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompts2, pdf_content,input_text)
        st.subheader("The response is")
        st.write(response)
    else:
        st.write("Please upload your resume in pdf to proceed.")

#see in the the submit2 button, only the prompt template is different
#we are suing input_prompt2 for submit2 button

