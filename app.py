import streamlit as st
import requests
import json

import timeit
import datetime

import os
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="PDF AI Chat Assistant - Open Source Version", layout="wide")
st.subheader("Welcome to PDF AI Chat Assistant - Life Enhancing with AI.")
st.write("Important notice: This Open PDF AI Chat Assistant is offered for information and study purpose only and by no means for any other use. Any user should never interact with the AI Assistant in any way that is against any related promulgated regulations. The user is the only entity responsible for interactions taken between the user and the AI Chat Assistant.")

css_file = "main.css"
with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)   

HUGGINGFACEHUB_API_TOKEN = os.getenv('HUGGINGFACEHUB_API_TOKEN')

uploaded_file = st.file_uploader('Upload your PDF file to AI Chat', type="pdf")
#uploaded_file = st.file_uploader("Upload your PDF file to AI Chat.", type=['pdf'], accept_multiple_files=True)
print(uploaded_file)
#print({uploaded_file})   #TypeError: unhashable type: 'UploadedFile'

user_question= st.text_input("Enter your question to query your pdf file")

if st.button("Get AI Response"):
    if uploaded_file is not None and user_question:
        with st.spinner('Fetching AI response...'): 
            url = "https://binqiangliu-singlepdfaichatfastapi.hf.space/fastapi_file_upload_process"
            headers = {
                #"Content-Type": "application/json",
                "Authorization": f"Bearer {HUGGINGFACEHUB_API_TOKEN}"
                #保险起见，建议始终采用f''的形式以及配合使用{}
            }
            payload = {"user_question": user_question, "filename": uploaded_file.name}
            print("User entered question: "+user_question)
            print("User uploaded file: "+uploaded_file.name)  
    
            print("API Call Starts...")    
            start_1 = timeit.default_timer()  
            
            #response = requests.post(url, params=payload, files={"uploaded_file": uploaded_file.getvalue()})
            
            response = requests.post(url, headers=headers, params=payload, files={"uploaded_file": uploaded_file.getvalue()})   #Working
            
            #response = requests.post(url, headers=headers, data=payload, files={"uploaded_file": uploaded_file.getvalue()})   #Failed
            #ai_response_content = response.json()["AIResponse"]
            #KeyError: 'AIResponse'

            #response = requests.post(url, headers=headers, json=payload, files={"uploaded_file": uploaded_file.getvalue()})   #Failed
            #ai_response_content = response.json()["AIResponse"]
            #KeyError: 'AIResponse'
            
            print(response)   #API Post的状态：成功或失败
            end_1 = timeit.default_timer()  
            print("API Call Ends...") 
            print(f'API Call共耗时： @ {end_1 - start_1}') 
            
            #ai_response_content=response['AIResponse']
            ai_response_content = response.json()["AIResponse"]
            print(ai_response_content)        
            print()
            response_data = response.json()
            ai_response = response_data["AIResponse"]
            print(ai_response)        
            
            st.write("AI Response:")
            st.write(ai_response_content)       
