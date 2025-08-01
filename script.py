from flask import Flask, render_template_string, request, redirect
import random
import time

app = Flask(__name__)

# Liste de 50 phrases inspirantes
phrases = [
    # 🌞 Joie
    "Le bonheur est contagieux, partage-le sans modération.",
    "Un sourire peut illuminer une journée entière.",
    "La joie se cache dans les petites choses du quotidien.",
    "Danse comme si personne ne te regardait.",
    "Aujourd’hui est un cadeau, savoure-le pleinement.",
    "Rire est le langage universel du bonheur.",
    "La vie est belle quand on la regarde avec le cœur.",
    "Cueille chaque instant comme une fleur rare.",
    "Le soleil brille toujours quelque part, même après la pluie.",
    "Ton rire est une mélodie qui rend le monde plus doux.",
    # 🧠 Réflexion
    "Ce n’est pas la destination qui compte, mais le chemin parcouru.",
    "Chaque erreur est une leçon déguisée.",
    "Le silence est parfois la réponse la plus sage.",
    "On ne voit bien qu’avec le cœur.",
    "La vie est un miroir : elle te renvoie ce que tu lui offres.",
    "Le changement commence toujours par une pensée.",
    "Ce que tu cherches à l’extérieur se trouve souvent en toi.",
    "La patience est une forme de sagesse.",
    "Les plus grandes découvertes naissent de l’inconfort.",
    "Réfléchir, c’est semer les graines du progrès.",
    # 🙏 Remerciement
    "Merci d’être une lumière dans ce monde.",
    "Ta présence est un cadeau précieux.",
    "Merci pour ton écoute, elle apaise les cœurs.",
    "Chaque geste de gentillesse compte, merci pour le tien.",
    "Merci pour ton sourire, il réchauffe les âmes.",
    "Ta générosité inspire ceux qui t’entourent.",
    "Merci pour ta patience et ta bienveillance.",
    "Tu fais une différence, merci d’être là.",
    "Merci pour ton soutien, il m’a porté plus loin.",
    "Gratitude infinie pour tout ce que tu es.",
    # 💪 Courage
    "Le courage ne crie pas, il murmure : essaie encore demain.",
    "Tu es plus fort que tu ne le crois.",
    "Chaque pas, même petit, est une victoire.",
    "Le vrai courage, c’est d’avancer malgré la peur.",
    "Les tempêtes forgent les âmes les plus solides.",
    "N’abandonne pas, ton histoire ne fait que commencer.",
    "Le doute est humain, mais ta force est réelle.",
    "Tu as déjà surmonté tant de choses, continue.",
    "Le courage, c’est de se relever encore une fois de plus.",
    "Ta résilience est une source d’inspiration.",
    # 🤝 Soutien
    "Je suis là, même dans le silence.",
    "Tu n’es pas seul, jamais.",
    "Un jour à la fois, je marche avec toi.",
    "Je crois en toi, même quand tu doutes.",
    "Tu peux toujours compter sur moi.",
    "Je t’envoie toute ma force et mon affection.",
    "Je te soutiens, peu importe la distance.",
    "Tu as le droit de flancher, je suis là pour te relever.",
    "Je t’écoute, sans jugement, avec tout mon cœur.",
    "Ton combat est le mien, ensemble on avance."
]

# Liste des messages avec timestamp
messages = []

# HTML avec fond visible, flou, logo, titre, formulaire, et messages
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Générateur de Joie</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: 'Arial', sans-serif;
            background-image: url('/static/background.jpg');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            display: flex;
        }

        .main {
            flex: 1;
            text-align: center;
            padding: 100px 50px;
            position: relative;
            z-index: 1;
        }

        .overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            backdrop-filter: blur(6px);
            background-color: rgba(255, 255, 255, 0.4);
            z-index: 0;
        }

        .logo {
            position: absolute;
            top: 20px;
            left: 20px;
            z-index: 2;
        }

        .logo img {
            width: 180px;
            height: auto;
        }

        .page-title {
            font-size: 48px;
            color: #001858;
            margin-bottom: 40px;
            position: relative;
            z-index: 2;
        }

        .phrase {
            font-size: 24px;
            margin-bottom: 30px;
            color: #001858;
            position: relative;
            z-index: 2;
        }

        button {
            padding: 10px 20px;
            font-size: 18px;
            background-color: #f582ae;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            color: white;
            z-index: 2;
            position: relative;
        }

        button:hover {
            background-color: #ff8fab;
        }

        .form-section {
            margin-top: 50px;
            position: relative;
            z-index: 2;
        }

        input, textarea {
            padding: 10px;
            margin: 5px;
            font-size: 16px;
            width: 80%;
            border-radius: 5px;
            border: 1px solid #ccc;
        }

        .sidebar {
            width: 300px;
            background-color: rgba(243, 210, 193, 0.9);
            padding: 20px;
            overflow-y: auto;
            height: 100vh;
            box-shadow: -2px 0 5px rgba(0,0,0,0.1);
            z-index: 1;
        }

        .message {
            margin-bottom: 15px;
            background-color: #fff;
            padding: 10px;
            border-radius: 5px;
            font-size: 14px;
        }

        .pseudo {
            font-weight: bold;
            color: #001858;
        }
    </style>
</head>
<body>
    <div class="main">
        <div class="overlay"></div>

        <div class="logo">
            <img src="/static/logo.png" alt="Logo">
        </div>

        <h1 class="page-title">Tu n'es pas seul</h1>

        <div class="phrase">{{ phrase }}</div>
        <form method="get">
            <button type="submit">Générer une nouvelle phrase</button>
        </form>

        <div class="form-section">
            <h3>Laisse un message 💬</h3>
            <form method="post">
                <input type="text" name="pseudo" placeholder="Ton pseudo" required><br>
                <textarea name="message" placeholder="Ton message" rows="3" required></textarea><br>
                <button type="submit">Envoyer</button>
            </form>
        </div>
    </div>

    <div class="sidebar">
        <h3>🌟 Messages</h3>
        {% for msg in messages %}
            <div class="message">
                <div class="pseudo">{{ msg.pseudo }}</div>
                <div>{{ msg.message }}</div>
            </div>
        {% endfor %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    current_time = time.time()
    valid_messages = [msg for msg in messages if current_time - msg["timestamp"] < 120]

    if request.method == "POST":
        pseudo = request.form.get("pseudo")
        message = request.form.get("message")
        if pseudo and message:
            messages.append({
                "pseudo": pseudo,
                "message": message,
                "timestamp": current_time
            })
        return redirect("/")

    phrase = random.choice(phrases)
    return render_template_string(HTML_TEMPLATE, phrase=phrase, messages=valid_messages)

if __name__ == "__main__":
    app.run(debug=True)
