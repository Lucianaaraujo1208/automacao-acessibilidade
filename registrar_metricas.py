import sqlite3

# Função para criar banco de dados se não existir
def criar_banco():
    conn = sqlite3.connect('acessibilidade.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS analises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            data_hora TEXT,
            violacoes INTEGER,
            detalhes_violacoes TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Função para salvar análise
def salvar_analise(url, violacoes, detalhes_violacoes):
    conn = sqlite3.connect('acessibilidade.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO analises (url, data_hora, violacoes, detalhes_violacoes) 
        VALUES (?, datetime('now'), ?, ?)
    ''', (url, violacoes, detalhes_violacoes))
    conn.commit()
    conn.close()

# Função para consultar todas as análises salvas
def consultar_analises():
    conn = sqlite3.connect('acessibilidade.db')
    c = conn.cursor()
    c.execute('SELECT * FROM analises')
    rows = c.fetchall()

    for row in rows:
        print(f"ID: {row[0]}, URL: {row[1]}, Data e Hora: {row[2]}, Violações: {row[3]}")
        print(f"Detalhes das Violações: {row[4]}\n")
    
    conn.close()

# Exemplo de uso
if __name__ == "__main__":
    criar_banco()  # Cria o banco de dados se não existir
    
    # Exemplo de como salvar uma análise
    salvar_analise('https://exemplo.com', 5, 'Problema de contraste, navegação via teclado ausente')
    
    # Consultar todas as análises realizadas
    consultar_analises()