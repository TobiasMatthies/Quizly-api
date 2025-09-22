import json

import whisper
from google import genai

client = genai.Client()

filename = None
prompt = """Based on the following transcript, generate a quiz in valid JSON format.

The quiz must follow this exact structure:

{{

  "title": "Create a concise quiz title based on the topic of the transcript.",

  "description": "Summarize the transcript in no more than 150 characters. Do not include any quiz questions or answers.",

  "questions_data": [

    {{

      "question_title": "The question goes here.",

      "question_options": ["Option A", "Option B", "Option C", "Option D"],

      "answer": "The correct answer from the above options"

    }},

    ...

    (exactly 10 questions)

  ]

}}

Requirements:

- Each question must have exactly 4 distinct answer options.

- Only one correct answer is allowed per question, and it must be present in 'question_options'.

- The output must be valid JSON and parsable as-is (e.g., using Python's json.loads).

- The answer field should have the exact same content as the right option

- Do not include explanations, comments, or any text outside the JSON."""


def audio_download_hook(d):
    if d["status"] == "finished":
        global filename
        filename = d["filename"]


def generate_transcribtion():
    model = whisper.load_model("turbo")
    global filename
    transcribtion = model.transcribe(filename)
    return transcribtion


def generate_quiz(transcribtion, url):
  global prompt

  response = client.models.generate_content(
      model="gemini-2.5-flash",
      contents=[
          json.dumps(transcribtion), json.dumps(prompt)
      ],
      config={
          "response_mime_type": "application/json"
      }
  )

  json_string = response.candidates[0].content.parts[0].text
  quiz_data = json.loads(json_string)
  quiz_data["video_url"] = url

  return quiz_data
