<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Foodie Quiz</title>
    <link rel="stylesheet" href="https://pyscript.net/releases/2024.1.1/core.css">
    <script type="module" src="https://pyscript.net/releases/2024.1.1/core.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-orange-50 min-h-screen flex items-center justify-center p-6">

    <div id="main-card" class="bg-white p-8 rounded-3xl shadow-2xl max-w-md w-full text-center">
        <div id="game-ui">
            <span class="text-6xl">👨‍🍳</span>
            <h1 class="text-3xl font-bold text-slate-800 mt-4 mb-2">Foodie Quiz</h1>
            <p class="text-slate-500 mb-8">Loading Python Engine...</p>
            <div id="load-box" class="animate-pulse text-orange-500 font-bold">Please wait...</div>
        </div>
    </div>

    <script type="py">
from pyscript import document

def start_game(event):
    ui = document.querySelector("#game-ui")
    ui.innerHTML = """
        <h2 class="text-xl font-bold mb-4">Question 1: Which country invented Caesar Salad?</h2>
        <button py-click="check_correct" class="w-full bg-orange-500 text-white p-3 rounded-lg mb-2">Mexico</button>
        <button py-click="check_wrong" class="w-full bg-slate-200 p-3 rounded-lg">Italy</button>
    """

def check_correct(event):
    document.querySelector("#game-ui").innerHTML = "<h2 class='text-2xl font-bold text-green-500'>Correct! 🎉</h2><p class='mt-4'>You're a master chef!</p>"

def check_wrong(event):
    document.querySelector("#game-ui").innerHTML = "<h2 class='text-2xl font-bold text-red-500'>Oops! 😅</h2><p class='mt-4'>It was actually invented in Mexico!</p>"

# Ready to play
document.querySelector("#load-box").innerHTML = '<button py-click="start_game" class="bg-orange-600 text-white px-10 py-4 rounded-full text-xl font-bold shadow-lg hover:scale-105 transition-transform">PLAY NOW</button>'
    </script>
</body>
</html>
