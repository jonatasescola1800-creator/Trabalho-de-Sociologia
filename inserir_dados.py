import sqlite3

conexao = sqlite3.connect("dados.db")
cursor = conexao.cursor()

cursor.execute("""
INSERT INTO cachorros
(nome, idade, status, vacina, vermifugo, descricao, castrado, sexo, porte, imagem)

VALUES
(
    'Luna',
    '3 meses',
    'Adotado',
    'Sim',
    'Sim',
    'Muito carinhosa e brincalhona, adora crianças e outros animais. Está ansiosa para encontrar um lar cheio de amor!',
    'Não',
    'Fêmea',
    'Pequeno',
    'luna.jpg'
)
""")

conexao.commit()
conexao.close()

print("Cachorro inserido!")