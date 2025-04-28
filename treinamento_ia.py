import sqlite3
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

# Função para extrair dados do banco de dados
def extrair_dados():
    conn = sqlite3.connect('acessibilidade.db')
    c = conn.cursor()
    c.execute('SELECT violacoes, detalhes_violacoes FROM analises')
    dados = c.fetchall()
    conn.close()
    
    # Transformar dados em arrays para usar no modelo
    violacoes = np.array([ [row[0]] for row in dados ])  # Número de violações
    melhorias = np.array([ [1 if 'alto contraste' in row[1] else 0] for row in dados ])  # Exemplo de sugestão: solução manual para alto contraste
    return violacoes, melhorias

# Função para treinar o modelo de IA
def treinar_modelo():
    violacoes, melhorias = extrair_dados()

    # Dividindo os dados em treino e teste
    X_train, X_test, y_train, y_test = train_test_split(violacoes, melhorias, test_size=0.25)

    # Treinando o modelo de Regressão Logística
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # Avaliando o modelo
    score = model.score(X_test, y_test)
    print(f"Acurácia do modelo: {score * 100:.2f}%")

# Exemplo de uso
if __name__ == "__main__":
    treinar_modelo()