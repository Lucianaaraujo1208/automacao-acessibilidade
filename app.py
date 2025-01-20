from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import logging
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from axe_selenium_python import Axe
import validators

app = Flask(__name__)

# Configuração do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def criar_banco_dados():
    with sqlite3.connect('acessibilidade.db') as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS analises (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL,
                data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
                violacoes INTEGER,
                detalhes_violacoes TEXT
            )
        ''')
        conn.commit()

criar_banco_dados()

def verificar_acessibilidade(url):
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        logging.info(f"Verificando acessibilidade para a URL: {url}")
        driver.get(url)
        axe = Axe(driver)
        axe.inject()
        resultados = axe.run()

        violacoes = []
        violations = resultados['violations']

        if not violations:
            logging.info("Nenhuma violação encontrada.")
            return 0, []

        for violation in violations:
            violacoes.append({
                'descricao': violation['description'],
                'ajuda': violation['help'],
                'impacto': violation['impact'],
                'elemento': violation.get('element', 'N/A'),
                'sugestao': violation.get('helpUrl', 'N/A')
            })

        num_violacoes = sum(len(v['nodes']) for v in violations)
        logging.info(f"Número de violações: {num_violacoes}")
        return num_violacoes, violacoes
    except Exception as e:
        logging.error(f"Erro ao verificar acessibilidade: {e}")
        return 0, []
    finally:
        driver.quit()

def salvar_analise(url, violacoes, detalhes_violacoes):
    try:
        with sqlite3.connect('acessibilidade.db') as conn:
            c = conn.cursor()
            c.execute('INSERT INTO analises (url, violacoes, detalhes_violacoes) VALUES (?, ?, ?)',
                      (url, violacoes, json.dumps(detalhes_violacoes)))  # Usando json.dumps
            conn.commit()
        logging.info(f"Análise de acessibilidade para {url} salva com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao salvar análise no banco de dados: {e}")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        if url and validators.url(url):  # Verificação da URL
            logging.info(f"Recebida URL para verificação: {url}")
            violacoes, detalhes_violacoes = verificar_acessibilidade(url)
            salvar_analise(url, violacoes, detalhes_violacoes)
            return redirect(url_for('resultado', url=url))
        else:
            logging.warning("URL inválida fornecida.")
            return render_template('index.html', error="URL inválida.")
    return render_template('index.html')

@app.route('/resultado')
def resultado():
    url = request.args.get('url')
    if not url:
        logging.error("Nenhuma URL fornecida para exibir resultados.")
        return redirect(url_for('index'))

    with sqlite3.connect('acessibilidade.db') as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM analises WHERE url = ? ORDER BY id DESC LIMIT 1', (url,))
        resultado = c.fetchone()

    if resultado:
        violacoes = resultado[3]  # Número de violações
        detalhes_violacoes = eval(resultado[4])  # Detalhes das violações como lista de dicionários
        violations_count = violacoes  # Certifique-se de que violacoes é um número
        logging.info(f"Violations count: {violations_count}")

        logging.info(f"Exibindo resultados para a URL: {url}")
        return render_template('resultado.html', 
                               url=url, 
                               violations=detalhes_violacoes, 
                               violations_count=violations_count, 
                               resultados={'status': 'sucesso', 'detalhes': 'Análise concluída'})
    else:
        logging.warning(f"Nenhum resultado encontrado para a URL: {url}")
        return render_template('resultado.html', 
                               url=url, 
                               violations=[], 
                               violations_count=0, 
                               resultados={'status': 'erro', 'detalhes': 'Nenhum resultado encontrado.'})

if __name__ == '__main__':
    app.run(debug=True)