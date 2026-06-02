# -*- coding: utf-8 -*-
import sys
import os

# INJEÇÃO AUTOMÁTICA DE CAMINHO (Garante que o Python ache a pasta 'db' e o 'config')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from flask import Flask, jsonify, request
from functools import wraps
import jwt
import datetime
import bcrypt

# Import direto da pasta local 'db' (Agora vai funcionar sem erros)
from db.connection import get_db

app = Flask(__name__)
SECRET_KEY = "chave_super_secreta_demo"  # em produção, use variável de ambiente

# ------------------ Autenticação ------------------

@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    usuario = data.get("usuario")
    senha = data.get("senha")

    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE login=%s", (usuario,))
    user = cursor.fetchone()

    if user and bcrypt.checkpw(senha.encode("utf-8"), user["senha_hash"].encode("utf-8")):
        token = jwt.encode(
            {
                "usuario": user["login"],
                "permissao": user["permissao"],
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            },
            SECRET_KEY,
            algorithm="HS256"
        )
        return jsonify({"status": "ok", "token": token})
    else:
        return jsonify({"status": "erro", "mensagem": "Credenciais inválidas"}), 401

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"mensagem": "Token ausente"}), 403
        try:
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except:
            return jsonify({"mensagem": "Token inválido ou expirado"}), 403
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"mensagem": "Token ausente"}), 403
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            if payload.get("permissao") != "ADMIN":
                return jsonify({"mensagem": "Acesso negado: apenas ADMIN"}), 403
        except:
            return jsonify({"mensagem": "Token inválido ou expirado"}), 403
        return f(*args, **kwargs)
    return decorated

# ------------------ Produtos ------------------

@app.route("/api/produtos", methods=["GET"])
@token_required
def listar_produtos():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM produtos")
    rows = cursor.fetchall()
    return jsonify(rows)

@app.route("/api/produtos", methods=["POST"])
@admin_required
def adicionar_produto():
    data = request.json
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO produtos (nome, sku, quantidade, estoque_minimo, estoque_maximo) VALUES (%s, %s, %s, %s, %s)",
        (data["nome"], data["sku"], data["quantidade"], data["estoqueMinimo"], data["estoqueMaximo"])
    )
    db.commit()
    return jsonify({"status": "ok"})

@app.route("/api/produtos/<int:id>", methods=["PUT"])
@admin_required
def editar_produto(id):
    data = request.json
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "UPDATE produtos SET nome=%s, sku=%s, quantidade=%s, estoque_minimo=%s, estoque_maximo=%s WHERE id=%s",
        (data["nome"], data["sku"], data["quantidade"], data["estoqueMinimo"], data["estoqueMaximo"], id)
    )
    db.commit()
    return jsonify({"status": "ok"})

@app.route("/api/produtos/<int:id>", methods=["DELETE"])
@admin_required
def deletar_produto(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM produtos WHERE id=%s", (id,))
    db.commit()
    return jsonify({"status": "ok"})

# ------------------ Usuários ------------------

@app.route("/api/usuarios", methods=["POST"])
@admin_required
def adicionar_usuario():
    data = request.json
    senha_hash = bcrypt.hashpw(data["senha"].encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO usuarios (nome, login, senha_hash, permissao) VALUES (%s, %s, %s, %s)",
        (data["nome"], data["login"], senha_hash, data["permissao"])
    )
    db.commit()
    return jsonify({"status": "ok"})

# ------------------ Inicialização ------------------

if __name__ == "__main__":
    app.run(debug=True, port=5000)
