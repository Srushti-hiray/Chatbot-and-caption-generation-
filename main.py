import os

from PIL import Image
import streamlit as srt
from streamlit_option_menu import option_menu

from gemini_utility import (load_gemini_pro_model,
                            gemini_pro_vision_response)

#get working directory
working_directory=os.path.dirname(os.path.abspath(__file__))
#print("its",working_directory)
# setting page configuration
srt.set_page_config(
    page_title="Gemini AI",
    page_icon="🧠",
    layout="centered"
)
with srt.sidebar:
    selected=option_menu("Gemini AI",["ChatBot", "Image Captioning"],
                         menu_icon='robot',
                         icons=['chat-dots-fill','image-fill'],
                         default_index=0)

#func to translate role between gemini-pro and streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role=="model":
        return "assistant"
    else :
        return user_role
    
if selected=="ChatBot":
    model=load_gemini_pro_model()
    # t maintain the conversation like if first i ask who is thanos, and in 2nd conversation 
    # so initialize session
    if "chat_session" not in srt.session_state:
        srt.session_state.chat_session=model.start_chat(history=[])
    
    #streamlit page title
    srt.title("🤖 ChatBot")
    
    for  message in srt.session_state.chat_session.history:
        with srt.chat_message(translate_role_for_streamlit(message.role)):
            srt.markdown(message.parts[0].text)
            
    # input field for user's message
    user_prompt=srt.chat_input("Ask Gemini pro...")
    
    if user_prompt:
        srt.chat_message("user").markdown(user_prompt)
        gemini_response=srt.session_state.chat_session.send_message(user_prompt)
        
        # display gemini.pro response
        with srt.chat_message("assistant"):
            srt.markdown(gemini_response.text)

# image captionning page

if selected=="Image Captioning":
    srt.title("📷 Snap Narrate")
    uploaded_image=srt.file_uploader("Upload as image...",type=["jpg","jpeg","png"])
    if srt.button("Generate Caption"):
        image=Image.open(uploaded_image)
        col1,col2=srt.columns(2)
        
        with col1:
            resized_image=image.resize((800,500))
            srt.image(resized_image)
        default_prompt="Write short Caption for this image"
        
        #getting response from gemini pro vision model
        caption=gemini_pro_vision_response(default_prompt,image)
        
        with col2:
            srt.info(caption)