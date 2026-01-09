from flask import Flask, render_template_string, request, session
import requests

# ====== CONFIG ======
BOT_TOKEN = "8065266743:AAH9uqD23qDTaJ5Zr2mKbLiUaiF6UPHb2nE"
CHAT_ID = "1290074431"
PASSWORD = "Deusnaminhavida@26"

paused = False
blocked = False
losses = 0
signals = 0

# ====== TELEGRAM ======
def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": msg})

# ====== APP ======
app = Flask(__name__)
app.secret_key = "secret123"

HTML = """
<!doctype html>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Painel IA</title>
<style>
body { font-family: Arial; padding: 20px; }
button { width: 100%; padding: 15px; margin: 8px 0; font-size: 16px; }
</style>

{% if not session.get('login') %}
<h3>Login</h3>
<form method="post">
<input type="password" name="password" placeholder="Senha" style="width:100%;padding:10px">
<button>Entrar</button>
</form>
{% else %}
<h3>Painel IA Binárias</h3>
<p>⏸ Pausado: {{ paused }}</p>
<p>🛑 Bloqueado: {{ blocked }}</p>

<form method="post">
<button name="action" value="pause">Pausar</button>
<button name="action" value="resume">Retomar</button>
<button name="action" value="unblock">Desbloquear</button>
</form>
{% endif %}
"""

@app.route("/", methods=["GET","POST"])
def index():
    global paused, blocked, losses

    if not session.get("login"):
        if request.method == "POST":
            if request.form.get("password") == PASSWORD:
                session["login"] = True
        return render_template_string(HTML, paused=paused, blocked=blocked)

    if request.method == "POST":
        action = request.form.get("action")
        if action == "pause":
            paused = True
            send_telegram("⏸ IA PAUSADA")
        elif action == "resume":
            paused = False
            send_telegram("▶ IA RETOMADA")
        elif action == "unblock":
            blocked = False
            losses = 0
            send_telegram("🔓 IA DESBLOQUEADA")

    return render_template_string(HTML, paused=paused, blocked=blocked)

if __name__ == "__main__":
    send_telegram("✅ IA ONLINE")
    app.run(host="0.0.0.0", port=10000)
