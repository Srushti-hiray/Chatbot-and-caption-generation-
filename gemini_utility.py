import os
import json


import google.generativeai as genai
working_directory=os.path.dirname(os.path.abspath(__file__))

config_file_path=f"{working_directory}/config.json"
config_data=json.load(open(config_file_path))

GOOGLE_API_KEY=config_data["GOOGLE_API_KEY"]
#print(GOOGLE_API_KEY)

#configuring google.generative ai with api key
genai.configure(api_key=GOOGLE_API_KEY)

# def list_available_models():
#     try:
#         models = genai.list_models()  # This might be the correct call to get models
#         return models
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return []

# models = list_available_models()
# print("Available models:")
# for model in models:
#     print(model)
#function to load gemini-pro for chatbot
def load_gemini_pro_model():
    gemini_pro_model=genai.GenerativeModel("gemini-pro")
    return gemini_pro_model

# function for image captioning

def gemini_pro_vision_response(prompt,image):
    gemini_pro_vision_model=genai.GenerativeModel("gemini-1.5-flash")
    response=gemini_pro_vision_model.generate_content([prompt,image])
    result=response.text
    return result

