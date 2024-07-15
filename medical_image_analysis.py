import os
from dotenv import load_dotenv
import google.generativeai as genai
import streamlit as st
load_dotenv()

api_key = os.getenv('GOOGLE_API_KEY')

#configure genai key
genai.configure(api_key=api_key)
# Set up the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 0,
  "max_output_tokens": 8192,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]



model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

system_prompts = [
  "Your Prompt here"]

st.title('Medical Image Analysis')

#file upload

upload_file = st.file_uploader("Please upload your medical image", type=['png', 'jpg', 'jpeg'])

if upload_file:
    st.image(upload_file, width=200, caption="Uploaded Image")


submit=st.button("Generate Analysis")

if submit:
     image_data = upload_file.getvalue()

     image_parts = [
        {
            "mime_type" : "image/jpg",
            "data" : image_data
        }
    ]
    
#     making our prompt ready
     prompt_parts = [
        image_parts[0],
        system_prompts[0],
    ]
     
     response = model.generate_content(prompt_parts)
     if response:
        st.title('Detailed analysis based on the uploaded image')
        st.write(response.text)
