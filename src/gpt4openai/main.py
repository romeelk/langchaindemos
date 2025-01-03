import base64
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

deployment_name = 'gpt-4'
api_version = '2024-02-15-preview' # this might change in the future

client = AzureOpenAI(
    api_version=api_version
)

# create function to convert image to base64
def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

def convert_base64_to_data_url(base64_string):
    return f"data:image/png;base64,{base64_string}"

print("Gpt 4 turbo is ready to use")

response = client.chat.completions.create(
    model=deployment_name,
    messages=[
        { "role": "system", "content": "You are a helpful assistant." },
        { "role": "user", "content": [  
            { 
                "type": "text", 
                "text": "What is the capital of france:" 
            }
        ] } 
    ],
    max_tokens=2000 
)
print("Converting image timetable.png to base64")
base64image = image_to_base64("timetable.png")
print(base64image)
print(response.choices[0].message.content)

data_url = convert_base64_to_data_url(base64image)

response = client.chat.completions.create(
   model=deployment_name,
   messages=[
       { "role": "system", "content": "You are a helpful assistant." },
       { "role": "user", "content": [  
           { 
               "type": "text", 
              "text": "Describe this picture:" 
           },
           { 
               "type": "image_url",
               "image_url": {
                   "url": f"{data_url}"
               }
          }
       ] } 
  ],
   max_tokens=2000 
)
print(response.choices[0].message.content)