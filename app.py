from flask import Flask, render_template, request, redirect
import csv
import os

app = Flask(__name__)

ARQUIVO = "contatos.csv"


def carregar_contatos():
    contatos = []

    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
            leitor = csv.DictReader(arquivo)

            for linha in leitor:
                contatos.append(linha)

    return contatos


@app.route("/")
def inicio():
    contatos = carregar_contatos()
    return render_template("index.html", contatos=contatos)


@app.route("/salvar", methods=["POST"])
def salvar():
    telefone = request.form.get("telefone", "").strip()
    nome = request.form.get("nome", "").strip()
    status = request.form.get("status", "Pendente")
    observacao = request.form.get("observacao", "").strip()

    arquivo_existe = os.path.exists(ARQUIVO)

    with open(ARQUIVO, "a", newline="", encoding="utf-8") as arquivo:
        campos = ["nome", "telefone", "status", "observacao"]
        escritor = csv.DictWriter(arquivo, fieldnames=campos)

        if not arquivo_existe:
            escritor.writeheader()

        escritor.writerow({
            "nome": nome,
            "telefone": telefone,
            "status": status,
            "observacao": observacao
        })

    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
