import requests # Biblioteca para fazer requisições HTTP
from bs4 import BeautifulSoup # Biblioteca para análise de documentos HTML e XML
from urllib.parse import urlparse # Módulo para análise de URLs 

def validar_url(url):
     #Verifica se a URL fornecida é válida.
    try:
        resultado = urlparse(url) # Analisa a URL
        return all([resultado.scheme, resultado.netloc])  # Retorna True se a URL possui um esquema (http/https) e um domínio (netloc)
    except ValueError:
        return False # Retorna False em caso de erro na análise 

def extrair_html(url):
     #Extrai o HTML da página fornecida.
    try:
        resposta = requests.get(url, timeout=10)  # Realiza uma requisição GET para a URL com um timeout de 10 segundos
        resposta.raise_for_status()  # Levanta um erro se a resposta for inválida
        return resposta.text # Retorna o conteúdo HTML da resposta
    except requests.exceptions.Timeout:
        print(f"Erro: A solicitação para {url} excedeu o tempo limite.")
        return None # Retorna None se houver um erro de timeout
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar {url}: {e}")
        return None # Retorna None em caso de erro na requisição

if __name__ == "__main__":  # Executa este bloco se o script for executado diretamente
    url = input("Insira a URL para verificar: ") # Solicita a URL
    
    if validar_url(url): # Valida a URL
        html = extrair_html(url) # Tenta extrair o HTML da URL
        if html: # Se a extração for bem-sucedida
            print("HTML extraído com sucesso!")
            
            # Exemplo de uso do BeautifulSoup para analisar o HTML extraído
            soup = BeautifulSoup(html, 'html.parser') # Cria um objeto BeautifulSoup com o HTML
            # Imprime o título da página se ele existir; caso contrário, imprime "Sem título"
            print("Título da página:", soup.title.string if soup.title else "Sem título")
        else:
            print("Falha ao extrair o HTML.") # Mensagem de falha na extração
    else:
        print("URL inválida. Verifique e tente novamente.")  # Mensagem de erro para URL inválida