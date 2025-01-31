import os
from google import genai
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.models.openai import OpenAIModel
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

ollama_model = OllamaModel(
    model_name='deepseek-r1:1.5b',
    base_url='http://localhost:11434/v1',
)

ds_model = OpenAIModel(
    'deepseek-chat',
    base_url='https://api.deepseek.com',
    api_key=os.environ["DEEPSEEK_API_KEY"],
)

mm_model = OpenAIModel(
    "MiniMax-Text-01",
    base_url="https://api.minimaxi.chat/v1",
    api_key=os.environ["MINIMAX_API_KEY"]
)

# Gemini API setup
# genai.configure(api_key=os.environ["GEMINI_API_KEY"]) # Removed configure line
gemini_client = genai.Client(api_key=os.environ["GEMINI_API_KEY"]) # Explicitly pass API key

question = """
    Condition: Itchy and painful keloid
    Please confirm the exact date of onset of keloid.
    Please advise where did the keloid come from e.g. accident/injury details, date of accident/injury
    Please confirm the exact date of keloid starting to get itchy and painful
    Please advise if you have ever seen any other medical practitioner for keloid condition.
    Please confirm if Dr Lam is the first practitioner you have seen for keloid condition.
    Please confirm if any previous treatment has been done to treat keloid.
    Condition: Viral warts
    Please confirm if this is the first time you have had warts. If not please provide date for previous condition.
    Please confirm the exact date of onset of symptoms (dd/mm/yyyy)?
    Please advise if you have ever seen any other medical practitioner for warts condition.
    Please confirm if Dr Lam is the first practitioner you have seen for warts condition.
    Please confirm if any previous treatment has been done to treat warts e.g. Co2 or other cauterization.
"""
