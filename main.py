import requests
from openai import OpenAI
client = OpenAI()

response = client.images.generate(
    model="dall-e-3",
    prompt="Porsche gt3 rs",
    size="1024x1024",
    quality="standard",
    n=1,
)

image_url = response.data[0].url

image_data = requests.get(image_url).content

with open("generated_image.png", "wb") as f:
    f.write(image_data)

print("Obrázok bol uložený ako 'generated_image.png'")