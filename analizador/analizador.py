import logging
import sqlite3
import json
from axe_selenium_python import Axe
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configuração do logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# Inicializa o driver do Selenium
driver = webdriver.Chrome()

def verificar_acessibilidade(url):
    try:
        driver.get(url)  # Carrega a URL no navegador
        axe = Axe(driver)  # Inicializa o Axe para análise de acessibilidade
        axe.inject()  # Injeta o Axe no DOM da página carregada
        resultados = axe.run()  # Executa a análise de acessibilidade

        logging.info(f"Resultados da análise: {resultados}")  # Registra os resultados da análise
        violations = resultados['violations']  # Obtém as violações detectadas

        violacoes = []  # Lista para armazenar detalhes das violações

        # Processa cada violação
        for violation in violations:
            for node in violation['nodes']:
                violacoes.append({
                    'descricao': violation['description'],  # Descrição da violação
                    'ajuda': violation['help'],  # Informação de ajuda sobre a violação
                    'impacto': violation['impact'],  # Impacto da violação
                    'elemento': node.get('html', 'N/A'),  # Elemento HTML afetado
                    'sugestao': violation.get('helpUrl', 'N/A')  # URL com sugestões para correção
                })

        return violacoes  # Retorna a lista de violações

    except Exception as e:
        logging.error(f"Erro ao verificar acessibilidade: {e}")
        return None
    finally:
        driver.quit()  # Fecha o driver do navegador após a execução

def salvar_analise(url, violacoes, detalhes_violacoes):
    with sqlite3.connect('acessibilidade.db') as conn:
        c = conn.cursor()
        try:
            # Insere os dados da análise no banco de dados
            c.execute('INSERT INTO analises (url, data_hora, violacoes, detalhes_violacoes) VALUES (?, datetime("now"), ?, ?)',
                      (url, violacoes, detalhes_violacoes))
            conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Erro ao salvar no banco de dados: {e}")

def criar_banco():
    with sqlite3.connect('acessibilidade.db') as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS analises (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        url TEXT,
                        data_hora TEXT,
                        violacoes INTEGER,
                        detalhes_violacoes TEXT)''')
        conn.commit()

# Função principal
def main():
    criar_banco()  # Cria o banco de dados
    url = 'https://example.com'  # URL a ser verificada
    violacoes = verificar_acessibilidade(url)  # Verifica a acessibilidade da URL
    
    if violacoes:
        salvar_analise(url, len(violacoes), json.dumps(violacoes))  # Salva a análise no banco de dados
        exibir_na_pagina(url, len(violacoes))  # Exibe o número de violações na página
    else:
        logging.info("Nenhuma violação encontrada ou erro na verificação.")

def exibir_na_pagina(url, num_violacoes):
    driver.get(url)  # Carrega a página novamente
    
    # Aguardar o carregamento completo da página
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    
    # Adiciona um elemento HTML na página para exibir o número de violações
    script = f"""
    var div = document.createElement('div');
    div.style.position = 'fixed';
    div.style.top = '20px';
    div.style.right = '20px';
    div.style.padding = '10px';
    div.style.backgroundColor = '#f8d7da';
    div.style.border = '1px solid #f5c6cb';
    div.style.color = '#721c24';
    div.style.fontSize = '16px';
    div.innerHTML = 'Número de Violações: {num_violacoes}';
    document.body.appendChild(div);
    """
    
    # Executa o script JavaScript para exibir a mensagem
    driver.execute_script(script) 

    # Aguardar um tempo para garantir que a página foi carregada completamente
    time.sleep(2)

if __name__ == '__main__':
    main()