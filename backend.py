from flask import Flask, jsonify, request
from google.cloud import aiplatform
import vertexai
from vertexai.generative_models import GenerativeModel
import json
from dotenv import load_dotenv
import os
from flask_cors import CORS
from google.oauth2 import service_account
from google import genai
from google.genai import types
# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


def generate(prompt, num_quizzes):
    try:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "classroom-ai.json"
        client = genai.Client(
        vertexai=True,
        project="classroom-ai-454103",
        location="us-central1"
        )
        
        # Initialize Gemini Pro Model
        model = "gemini-2.0-flash-lite-001"
        
        si_text1 = """You a classroom quiz generator for a particular lecture. Given a prompt, which will specify the content of the lecture, the questions asked by students during the lecture and the answer given, the number of quizzes to generate, generate the question in JSON format in the following order for each quiz: Question, Options, Correct, Explanation"""

        # Generate content using Vertex AI
        prompt_text = f"\nGenerate {num_quizzes} quizzes for the following lecture content: {prompt}"
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=prompt_text)
                ]
            )
        ]

        with open('format.JSON','r') as file:
            format = json.load(file)

        generate_content_config = types.GenerateContentConfig(
        temperature = 0.5,
        top_p = 0.95,
        max_output_tokens = 8192,
        response_modalities = ["TEXT"],
        response_mime_type = "application/json",
        response_schema = format,
        system_instruction=[types.Part.from_text(text=si_text1)],
        )
        
        response = client.models.generate_content(
            model=model,
            contents=prompt_text,
            config=generate_content_config
        )

        return response.text

    except Exception as e:
        raise Exception(f"Error in generate function: {str(e)}")

@app.route('/generate-quiz', methods=['POST'])
def generate_quiz():
    try:
        data = request.get_json()
        if not data or 'prompt' not in data or 'num_quizzes' not in data:
            return jsonify({'error': 'Missing prompt or num_quizzes in request'}), 400

        prompt = data['prompt']
        num_quizzes = int(data['num_quizzes'])
        
        return jsonify(json.loads(generate(prompt, num_quizzes)))
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
