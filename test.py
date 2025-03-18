from google import genai
from google.genai import types
import base64
import os

def generate():
  # Set up credentials
  os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "classroom-ai.json"
  
  client = genai.Client(
      vertexai=True,
      project="classroom-ai-454103",
      location="us-central1",
  )

  si_text1 = """You a classroom quiz generator for a particular lecture. Given a prompt, which will specify the content of the lecture, the questions asked by students during the lecture and the answer given, the number of quizzes to generate,  generate the question in JSON format in the following order for each quiz: Question, Options, Correct, Explanation"""

  model = "gemini-2.0-flash-lite-001"
  contents = [
    types.Content(
      role="user",
      parts=[
        types.Part.from_text(text="""digital trans""")
      ]
    )
  ]
  generate_content_config = types.GenerateContentConfig(
    temperature = 1,
    top_p = 0.95,
    max_output_tokens = 8192,
    response_modalities = ["TEXT"],
    safety_settings = [types.SafetySetting(
      category="HARM_CATEGORY_HATE_SPEECH",
      threshold="OFF"
    ),types.SafetySetting(
      category="HARM_CATEGORY_DANGEROUS_CONTENT",
      threshold="OFF"
    ),types.SafetySetting(
      category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
      threshold="OFF"
    ),types.SafetySetting(
      category="HARM_CATEGORY_HARASSMENT",
      threshold="OFF"
    )],
    response_mime_type = "application/json",
    response_schema = {"type":"ARRAY","minItems":1,"items":{"type":"OBJECT","properties":{"question":{"type":"STRING","description":"The quiz question"},"options":{"type":"OBJECT","properties":{"a":{"type":"STRING","description":"Option A"},"b":{"type":"STRING","description":"Option B"},"c":{"type":"STRING","description":"Option C"},"d":{"type":"STRING","description":"Option D"}},"required":["a","b","c","d"]},"correct":{"type":"STRING","enum":["a","b","c","d"],"description":"The correct option"},"explanation":{"type":"STRING","description":"Explanation for the correct answer"}},"required":["question","options","correct","explanation"]}},
    system_instruction=[types.Part.from_text(text=si_text1)],
  )
  response  = client.models.generate_content(
            model=model,
            contents=contents,
            config=generate_content_config
        )
  print(response)
generate()