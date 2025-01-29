from google import genai
from dotenv import load_dotenv
import os
import PIL.Image


load_dotenv()  # take environment variables from .env.
client = genai.Client(   api_key=os.environ["GEMINI_API_KEY"])

def getOCR(path):

    image1  = PIL.Image.open(path)
    
    #response = client.models.generate_content(model='gemini-2.0-flash-exp', contents='How does AI work?')
    prompt= "get the content from the image"
    response = client.models.generate_content(
        model='gemini-2.0-flash-exp', contents=[prompt, image1],
    
    )

    return(response.text)

print(getOCR("dr3.jpg"))