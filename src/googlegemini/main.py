# Tutorial source = https://cloud.google.com/vertex-ai/generative-ai/docs/start/quickstarts/quickstart-multimodal#python
import vertexai
from vertexai.generative_models import GenerativeModel
from dotenv import load_dotenv
import os

load_dotenv
PROJECT_ID = os.getenv("PROJECT_ID")

# init vertex AI
vertexai.init(project=PROJECT_ID, location="us-central1")

model = GenerativeModel("gemini-1.5-flash-002")

response = model.generate_content(
    "What's a good name for a flower shop that specializes in selling bouquets of dried flowers?"
)

print(response.text)
