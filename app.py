from flask import Flask, render_template, request
import sqlite3
import os
from werkzeug.utils import secure_filename

def pegar_cachorros():
    conexao = sqlite3.connect("dados.db")
    conexao.row_factory = sqlite3.Row
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM cachorros WHERE aprovado = 1")
    dados = cursor.fetchall()
    conexao.close()
    return dados

def pegar_cachorro_por_id(id):
    conexao = sqlite3.connect("dados.db")
    conexao.row_factory = sqlite3.Row
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT * FROM cachorros WHERE id = ?",
        (id,)
    )
    dog = cursor.fetchone()
    conexao.close()
    return dog

app = Flask(__name__)
UPLOAD_FOLDER = 'static/imagens'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def inicio():
    busca = request.args.get("busca", "").lower()
    status = request.args.get("status", "")
    cachorros = pegar_cachorros()
    filtrados = []

    for dog in cachorros:
        nome_match = busca in dog["nome"].lower()
        status_match = (
            status == ""
            or dog["status"] == status
        )
        if nome_match and status_match:
            filtrados.append(dog)

    return render_template(
        "index.html",
        cachorros=filtrados
    )

@app.route("/cachorro/<int:id>")
def pagina_cachorro(id):
    dog = pegar_cachorro_por_id(id)
    if dog is None:
        return "Cachorro não encontrado!", 404
    return render_template(
        "cachorro.html",
        dog=dog
    )

@app.route("/cadastrar")
def tela_cadastro():
    return render_template("cadastrar.html")

@app.route("/enviar-cachorro", methods=["POST"])
def enviar_cachorro():
    nome = request.form.get("nome")
    idade = request.form.get("idade")
    sexo = request.form.get("sexo")
    porte = request.form.get("porte")
    descricao = request.form.get("descricao")
    
    arquivo = request.files.get("imagem")
    if arquivo:
        nome_imagem = secure_filename(arquivo.filename)
        arquivo.save(os.path.join(app.config['UPLOAD_FOLDER'], nome_imagem))
    else:
        nome_imagem = "padrao.jpg"

    conexao = sqlite3.connect("dados.db")
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO cachorros (nome, idade, sexo, porte, descricao, imagem, status, aprovado)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (nome, idade, sexo, porte, descricao, nome_imagem, "Disponível", 0))
    conexao.commit()
    conexao.close()

    return "<h2>Cãozinho enviado com sucesso! Ele aparecerá no site assim que for aprovado.</h2> <a href='/'>Voltar</a>"

@app.route("/admin/pendentes")
def listar_pendentes():
    conexao = sqlite3.connect("dados.db")
    conexao.row_factory = sqlite3.Row
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM cachorros WHERE aprovado = 0")
    pendentes = cursor.fetchall()
    conexao.close()
    
    html = "<h1>Cães esperando aprovação:</h1>"
    for p in pendentes:
        html += f"<p>{p['nome']} - <a href='/admin/aprovar/{p['id']}'>Aprovar Agora</a></p>"
    return html

@app.route("/admin/aprovar/<int:id>")
def aprovar_cao(id):
    conexao = sqlite3.connect("dados.db")
    cursor = conexao.cursor()
    cursor.execute("UPDATE cachorros SET aprovado = 1 WHERE id = ?", (id,))
    conexao.commit()
    conexao.close()
    return f"Cão ID {id} aprovado! Ele já está visível na página principal."

@app.route("/admin/excluir/<int:id>")
def excluir_cachorro(id):
    conexao = sqlite3.connect("dados.db")
    conexao.row_factory = sqlite3.Row
    cursor = conexao.cursor()

    cursor.execute("SELECT imagem FROM cachorros WHERE id = ?", (id,))
    dog = cursor.fetchone()
    
    if dog:
        caminho_imagem = os.path.join("static/imagens", dog['imagem'])
        if os.path.exists(caminho_imagem):
            os.remove(caminho_imagem)

        cursor.execute("DELETE FROM cachorros WHERE id = ?", (id,))
        conexao.commit()

    conexao.close()
    return "Cachorro removido com sucesso! <a href='/'>Voltar</a>"

@app.errorhandler(404)
def pagina_nao_encontrada(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)