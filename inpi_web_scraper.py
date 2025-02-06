from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time


def acessar_inpi(marca):
    try:
        # Configuração do navegador em modo headless (sem abrir janela)
        print("Iniciando consulta no INPI...")
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")  # Executar sem abrir o navegador
        chrome_options.add_argument("--disable-gpu")  # Necessário para algumas versões do Windows
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

        # Acessar a página inicial do INPI
        driver.get("https://busca.inpi.gov.br/pePI/")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Continuar....")))

        # Clicar no botão "Continuar"
        driver.find_element(By.LINK_TEXT, "Continuar....").click()
        time.sleep(2)

        # Alternar para a nova aba aberta
        driver.switch_to.window(driver.window_handles[1])

        # Acessar a página de pesquisa básica
        driver.get("https://busca.inpi.gov.br/pePI/jsp/marcas/Pesquisa_classe_basica.jsp")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "marca")))

        # Selecionar a opção "Radical"
        driver.find_element(By.XPATH, "//input[@type='radio' and @value='nao']").click()

        # Inserir a marca no campo de pesquisa
        marca_input = driver.find_element(By.NAME, "marca")
        marca_input.send_keys(marca)

        # Clicar no botão "Pesquisar"
        driver.find_element(By.NAME, "botao").click()

        # Aguardar o carregamento dos resultados
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "mainContainer")))

        # Capturar os resultados da pesquisa
        capturar_resultados(driver)

    except Exception as e:
        print(f"Erro inesperado: {e}")

    finally:
        driver.quit()


def capturar_resultados(driver):
    try:
        resultados = driver.find_elements(By.XPATH, "//table//tr[contains(@bgcolor, '#E0E0E0')]")
        if not resultados:
            print("Nenhum resultado encontrado para a marca pesquisada.")
            return

        print("Resultados encontrados:")
        for resultado in resultados:
            numero = resultado.find_element(By.XPATH, ".//td[1]").text.strip()
            marca = resultado.find_element(By.XPATH, ".//td[4]").text.strip()
            situacao = resultado.find_element(By.XPATH, ".//td[6]").text.strip()
            titular = resultado.find_element(By.XPATH, ".//td[7]").text.strip()
            classe = resultado.find_element(By.XPATH, ".//td[8]").text.strip()

            print(f"- Número: {numero}")
            print(f"  Marca: {marca}")
            print(f"  Situação: {situacao}")
            print(f"  Titular: {titular}")
            print(f"  Classe: {classe}")
            print("")

        avaliar_viabilidade(resultados)

    except Exception as e:
        print(f"Erro ao capturar os resultados: {e}")


def avaliar_viabilidade(resultados):
    try:
        if len(resultados) > 0:
            print("A marca pesquisada possui registros similares. Avaliação adicional é necessária.")
        else:
            print("A marca pesquisada parece viável para registro.")
    except Exception as e:
        print(f"Erro ao avaliar a viabilidade: {e}")


if __name__ == "__main__":
    print("==============================")
    print("Consulta de Marcas no INPI")
    print("==============================\n")
    marca = input("Digite o nome da marca para consultar: ").strip()
    acessar_inpi(marca)
