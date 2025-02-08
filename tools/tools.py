import PIL.Image
from pdf2image import convert_from_path
from config import gemini_client  # Import gemini_client from config.py


async def getOCR(path):
    image1 = PIL.Image.open(path)
    prompt = "you are an information extractor, you can extract all the data from the provide image in markdown format"
    response = gemini_client.models.generate_content(
        model='gemini-2.0-flash-exp', contents=[prompt, image1],
    )
    return response.text


async def extractpdf(path) -> list[str]:
    results = []
    images = convert_from_path(path)
    for i in range(len(images)):
        filename = f'cached/{path}{i+1}.png'
        images[i].save(filename, 'PNG')
        results.append(filename)
    return results

async def getUserInfo(userID: str) -> str:
    return f"Name: Asa Choi, Age: 40, Gender: M, UserID:{userID}"

