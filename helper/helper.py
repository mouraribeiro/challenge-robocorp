import os
import re
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from RPA.Excel.Files import Files

# Configurações
search_phrase = "tecnologia"
news_category = "technology"
months = 1
output_excel = "news_data.xlsx"

# Função para baixar imagem
def download_image(url, folder="images"):
    if not os.path.exists(folder):
        os.makedirs(folder)
    response = requests.get(url)
    filename = os.path.join(folder, os.path.basename(url))
    with open(filename, 'wb') as f:
        f.write(response.content)
    return filename

# Função para verificar se contém valores monetários
def contains_money(text):
    return bool(re.search(r'\$\d+|\d+ dollars|\d+ USD', text))

# Inicializar Selenium WebDriver
driver = webdriver.Chrome()

try:
    # Abrir site de notícias
    driver.get("https://www.aljazeera.com/")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )

    # Pesquisar a frase
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(search_phrase)
    search_box.send_keys(Keys.RETURN)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".article-trending"))
    )

    # Extrair dados
    articles = driver.find_elements(By.CSS_SELECTOR, ".article-trending")
    data = []

    for article in articles[:5]:  # Limitar a 5 artigos para demonstração
        title = article.find_element(By.TAG_NAME, "h3").text
        date = article.find_element(By.CLASS_NAME, "date-simple").text
        description = article.find_element(By.CLASS_NAME, "text").text
        image_url = article.find_element(By.TAG_NAME, "img").get_attribute("src")
        image_file = download_image(image_url)

        data.append({
            "title": title,
            "date": date,
            "description": description,
            "image_file": image_file,
            "search_phrase_count": title.lower().count(search_phrase.lower()) + description.lower().count(search_phrase.lower()),
            "contains_money": contains_money(title) or contains_money(description)
        })

finally:
    driver.quit()

# Salvar dados em um arquivo Excel
excel = Files()
excel.create_workbook(output_excel)
excel.append_rows_to_worksheet(data, header=True)
excel.save_workbook()
excel.close_workbook()

print(f"Dados salvos em {output_excel}")
