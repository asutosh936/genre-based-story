from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__, static_folder='static')
CORS(app)


def generate_story(api_key, genre):
    
    client = OpenAI(api_key=api_key)

    prompt = f"""Write a short story in the {genre} genre. 
    The story should be approximately 200 words long and have a clear 
    beginning, middle, and end."""
   
    try:
        response = client.chat.completions.create(
              model="gpt-3.5-turbo",
              messages=[
                {"role": "system",
                 "content": "You are a creative story writer."},
                {"role": "user", "content": prompt}
              ],
              max_tokens=500,
              temperature=0.7
         )
        return response.choices[0].message.content

    except Exception as e:
        return f"Error generating story: {str(e)}"


@app.route('/')
def serve_frontend():
    return send_from_directory('static', 'index.html')


@app.route('/api/generate-story', methods=['POST'])
def generate_story_api():
    data = request.get_json()
    genre = data.get('genre')
    api_key = data.get('api_key')

    story = generate_story(api_key, genre)

    return jsonify({'story': story}), 200


if __name__ == '__main__':
    os.makedirs('static', exist_ok=True)
    app.run(debug=True, port=5001)