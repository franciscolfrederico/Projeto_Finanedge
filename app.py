from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import timedelta


app = Flask(__name__)
app.secret_key = "troque-por-uma-chave-segura"
app.permanent_session_lifetime = timedelta(hours=8)

# “banco” de teste em memória
USERS = {
    "ict_user": {"password": "1234", "nome": "Usuário ICT"},
    "empresa_user": {"password": "abcd", "nome": "Usuário Empresa"}
}

@app.route("/", methods=["GET"])
def index():
    if "user" in session:
        return redirect(url_for("dashboard"))
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    role = request.form.get("role")         # "Equipe" ou "Empresa"
    email = request.form.get("email", "").strip()
    senha = request.form.get("password", "")

    if not role:
        flash("Selecione o tipo de acesso: Equipe ou Empresa.", "error")
        return redirect(url_for("index"))

    if not email or not senha:
        flash("Preencha email e senha.", "error")
        return redirect(url_for("index"))

    user = USERS.get(email)
    if not user or user["password"] != senha:
        flash("Credenciais inválidas.", "error")
        return redirect(url_for("index"))

    session.permanent = True
    session["user"] = {"email": email, "nome": user["nome"], "role": role}
    flash(f"Bem-vindo(a), {user['nome']}!", "success")
    return redirect(url_for("dashboard"))

@app.route("/dashboard", methods=["GET"])
def dashboard():
    if "user" not in session:
        flash("Faça login para continuar.", "error")
        return redirect(url_for("index"))
    return render_template("dashboard.html", u=session["user"])

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("Sessão encerrada.", "success")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
