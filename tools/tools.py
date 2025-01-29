from google import genai
from dotenv import load_dotenv
import os
import PIL.Image
import asyncio
from pdf2image import convert_from_path

load_dotenv()  # take environment variables from .env.
client = genai.Client(   api_key=os.environ["GEMINI_API_KEY"])

async def getOCR(path):

    image1  = PIL.Image.open(path)
    
    #response = client.models.generate_content(model='gemini-2.0-flash-exp', contents='How does AI work?')
    prompt= "get the content from the image"
    response = client.models.generate_content(
        model='gemini-2.0-flash-exp', contents=[prompt, image1],
    
    )

    return(response.text)


async def extractpdf(path) -> []:
    results = []

    # incase of Linux we don't have to provide the popper_path parameter
    images = convert_from_path(
       path)

    for i in range(len(images)):
        # Save pages as images in the pdf
        filename = f'{path}{i+1}.png'
        images[i].save(filename , 'PNG')
        results.append(filename)
    return results

 
