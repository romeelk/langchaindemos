import vertexai
from vertexai.generative_models import GenerativeModel, Part

PROJECT_ID = "contini-5aa3a3d90477d2d3"

# init vertex AI
vertexai.init(project=PROJECT_ID, location="us-central1")

model = GenerativeModel("gemini-1.5-flash-002")

prompt = """
Provide a description of the image.
The description should also contain anything important which people say in the video.
"""


response = model.generate_content(
    [
        Part.from_uri(
            "gs://sandboxrk/timetable.png",
            mime_type="image/png",
        ),
        "What is shown in this image?",
    ]
)
print(response.text)