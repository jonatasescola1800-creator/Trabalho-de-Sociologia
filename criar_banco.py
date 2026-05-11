import sqlite3

conexao = sqlite3.connect("dados.db")

cursor = conexao.cursor()

cursor.execute("""
CREATE TABLE cachorros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    idade TEXT,
    status TEXT,
    vacina TEXT,
    vermifugo TEXT,
    descricao TEXT,
    castrado TEXT,
    sexo TEXT,
    porte TEXT,
    imagem TEXT,
    aprovado INTEGER DEFAULT 0
)
""")

conexao.commit()
conexao.close()

print("Banco criado!")