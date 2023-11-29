from flask import Flask, render_template, jsonify, request
import base64
import tempfile
import os
import re
import json
import requests

app = Flask(__name__)


# Creating simple Routes
@app.route("/test")
def test():
    return "Home Page"


@app.route("/test/help/")
def about_test():
    return "About Page"


# Routes to Render Something
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/help", strict_slashes=False)
def help():
    return render_template("help.html")


@app.route("/process_image", methods=["POST"])
def process_image():
    data = request.json.get("image_data")
    img_data = base64.b64decode(data)
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(img_data)
    temp_file.close()
    return jsonify({"tempFilePath": temp_file.name})


@app.route("/gen_seo", methods=["POST"])
def gen_seo_endpoint():
    image_path = request.json.get("image_path")
    result = gen_seo(image_path)
    return jsonify(result)


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def gen_seo(image_path):
    base64_image = encode_image(image_path)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer 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",
    }
    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "generate seo for this image, title and description for pinterest. respond in json format {title: 'title', description: 'description'}",
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
        "max_tokens": 300,
    }
    response = requests.post(
        "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
    )
    result = response.json()["choices"][0]["message"]["content"]
    os.remove(image_path)
    json_match = re.search(r"{.*}", result, re.DOTALL)
    if json_match:
        json_string = json_match.group(0)
        try:
            # Parse the JSON string into a Python dictionary
            json_data = json.loads(json_string)
            return json_data
        except json.JSONDecodeError:
            print("Error decoding JSON")
    else:
        print("No JSON found in the string")


# Make sure this we are executing this file
if __name__ == "__main__":
    app.run(debug=True)
