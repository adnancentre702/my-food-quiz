<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Foodie Quiz Live</title>
    <link rel="stylesheet" href="https://pyscript.net/releases/2024.1.1/core.css">
    <script type="module" src="https://pyscript.net/releases/2024.1.1/core.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-orange-50 min-h-screen flex items-center justify-center p-4">

    <div id="app" class="bg-white shadow-2xl rounded-3xl p-8 max-w-lg w-full text-center">
        <div id="game-ui">
            <h1 class="text-4xl mb-4">🌍</h1>
            <h1 class="text-2xl font-bold text-slate-800">Foodie Quiz Live</h1>
            <p class="text-slate-500 my-6">Connecting to Global Question Bank...</p>
            <div id="loader" class="text-orange-500 font-bold">Loading Engine...</div>
        </div>
    </div>

    <script type="py">
from pyscript import document, window
import json
import pyodide_http
import random

# Enable internet requests
pyodide_http.patch_all()
import requests

class LiveQuiz:
    def __init__(self):
        self.score = 0
        self.questions = []
        self.current_pos = 0

    async def fetch_questions(self, event=None):
        document.querySelector("#loader").innerHTML = "Fetching New Questions..."
        # This API gives 10 random Food & Drink questions
        url = "https://opentdb.com/api.php?amount=10&category=11&type=multiple"
        
        try:
            response = requests.get(url)
            data = response.json()
            self.questions = data['results']
            self.current_pos = 0
            self.load_question()
        except Exception as e:
            document.querySelector("#game-ui").innerHTML = f"Offline Error: {e}"

    def load_question(self, event=None):
        if self.current_pos >= len(self.questions):
            self.end_screen()
            return

        q_data = self.questions[self.current_pos]
        
        # Prepare options (Correct + Incorrect)
        opts = q_data['incorrect_answers'] + [q_data['correct_answer']]
        random.shuffle(opts)

        options_html = ""
        for opt in opts:
            is_correct = "true" if opt == q_data['correct_answer'] else "false"
            options_html += f'<button py-click="check_answer" data-correct="{is_correct}" class="w-full bg-white border-2 border-slate-100 p-4 rounded-xl mb-3 hover:border-orange-500 hover:bg-orange-50 transition-all text-slate-700 shadow-sm font-medium">{opt}</button>'

        document.querySelector("#game-ui").innerHTML = f"""
            <div class="flex justify-between mb-4 text-sm font-bold text-orange-500 uppercase">
                <span>Score: {self.score}</span>
                <span>Question {self.current_pos + 1}/10</span>
            </div>
            <h2 class="text-xl font-bold text-slate-800 mb-8">{q_data['question']}</h2>
            <div class="grid gap-1">{options_html}</div>
        """

    def check_answer(self, event):
        is_correct = event.target.getAttribute("data-correct")
        if is_correct == "true":
            self.score += 100
        
        self.current_pos += 1
        self.load_question()

    def end_screen(self):
        document.querySelector("#game-ui").innerHTML = f"""
            <h1 class="text-5xl mb-4">✨</h1>
            <h2 class="text-3xl font-bold">Round Over!</h2>
            <p class="text-xl my-6 text-slate-600">You earned <span class="text-orange-600 font-black">{self.score}</span> points</p>
            <button py-click="fetch_questions" class="bg-orange-500 text-white px-10 py-4 rounded-full font-bold shadow-lg">Get New Questions</button>
        """

quiz = LiveQuiz()

# Initial Start Button
document.querySelector("#loader").innerHTML = '<button py-click="quiz.fetch_questions" class="bg-orange-600 text-white px-12 py-4 rounded-full text-xl font-bold shadow-xl">START LIVE QUIZ</button>'
    </script>
</body>
</html>
