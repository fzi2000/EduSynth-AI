from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

AI_API_KEY = os.getenv("AI_ML_API_KEY")  # Add in Render Dashboard

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/generate', methods=['POST'])
def generate():
    text = request.form.get("text")

    # Summary
    summary_payload = {
        "model": "gpt-4o-mini",
        "input": f"Summarize this text in simple points:\n\n{text}"
    }

    summary = requests.post(
        "https://api.aimlapi.com/v1/chat/completions",
        json=summary_payload,
        headers={"Authorization": f"Bearer {AI_API_KEY}"}
    ).json()["choices"][0]["message"]["content"]

    # Quiz Generator
    quiz_payload = {
        "model": "gpt-4o-mini",
        "input": f"Create 5 MCQ questions with answers based on:\n\n{text}"
    }

    quiz = requests.post(
        "https://api.aimlapi.com/v1/chat/completions",
        json=quiz_payload,
        headers={"Authorization": f"Bearer {AI_API_KEY}"}
    ).json()["choices"][0]["message"]["content"]

    # Flashcards
    flash_payload = {
        "model": "gpt-4o-mini",
        "input": f"Generate 6 flashcards (term + explanation) from this text:\n\n{text}"
    }

    flashcards = requests.post(
        "https://api.aimlapi.com/v1/chat/completions",
        json=flash_payload,
        headers={"Authorization": f"Bearer {AI_API_KEY}"}
    ).json()["choices"][0]["message"]["content"]

    return render_template(
        "result.html",
        original=text,
        summary=summary,
        quiz=quiz,
        flashcards=flashcards
    )


if __name__ == "__main__":
    app.run(debug=True)
