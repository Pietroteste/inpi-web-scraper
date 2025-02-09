from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)

# Configurar o WebDriver do Selenium
def iniciar_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Rodar sem abrir janela
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# Rota para consulta de marca
@app.route('/consultar', methods=['GET'])
def consultar_marca():
    marca = request.args.get('marca')  # Pega o nome da marca da URL

    if not marca:
        return jsonify({"erro": "É necessário fornecer uma marca para consulta."}), 400

    try:
        driver = iniciar_driver()
        driver.get(f"https://busca.inpi.gov.br/pePI/jsp/marcas/Pesquisa_classe_basica.jsp?texto={marca}")

        # Simulação de extração (ajustar conforme necessário)
        resultado = {"marca": marca, "status": "Registro disponível"}

        driver.quit()
        return jsonify(resultado)

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# Página inicial informativa
@app.route('/')
def home():
    return '''
    <h1>API de Consulta de Marcas no INPI</h1>
    <p>Use o endpoint <code>/consultar?marca=NomeDaMarca</code> para buscar uma marca.</p>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
