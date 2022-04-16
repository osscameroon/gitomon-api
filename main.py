import requests
import json

from flask import Flask, request, render_template
from flask_cors import CORS, cross_origin


app = Flask(__name__)
CORS(app, support_credentials=True)

app.config['secret'] = "Secret"


@app.route('/', methods=['GET'])
@cross_origin(support_credentials=True)
def index():
    return render_template("index.html")


@app.route('/generate', methods=['POST'])
@cross_origin(support_credentials=True)
def generate():
    content = request.get_json()

    author = content.get("author")
    repo = content.get("repo")

    url = f"https://api.github.com/repos/{author}/{repo}"

    github_api_content = requests.get(url).json()
    languages = requests.get(f"{url}/languages").json()

    github_api_content["languages"] = languages

    # extract the username from owner object or organisation object
    github_api_content["username"] = (
        github_api_content["owner"]["login"]
        if "owner" in github_api_content
        else github_api_content["organization"]["login"]
    )
    del github_api_content["owner"]
    del github_api_content["license"]

    payload = {
      "items": [
        {
            **github_api_content,
            **{
              "share": {}
            }
        }
      ],
      "api_calls": 0,
      "api_calls_time": []
    }

    return payload, 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=2589)

