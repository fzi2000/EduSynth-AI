from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
AI_API_KEY = os.getenv("AI_ML_API_KEY")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    text = request.form.get("text")

    if not text:
        return render_template("index.html", message="⚠️ Please enter study notes!")

    headers = {
        "Authorization": f"Bearer {AI_API_KEY}",
        "Content-Type": "application/json"
    }

    def ask_ai(prompt):
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        r = requests.post(
            "https://api.aimlapi.com/v1/chat/completions",
            json=payload,
            headers=headers
        )
        data = r.json()

        # debug print
        print("API response:", data)

        if "choices" not in data:
            return f"API Error: {data}"

        return data["choices"][0]["message"]["content"]

    summary = ask_ai(f"Summarize this text in simple bullet points:\n{text}")
    quiz = ask_ai(f"Create 5 MCQs with answers based on:\n{text}")
    flashcards = ask_ai(f"Generate 5 flashcards (term + explanation) from:\n{text}")

    return render_template("result.html",
                           original=text,
                           summary=summary,
                           quiz=quiz,
                           flashcards=flashcards)

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )
