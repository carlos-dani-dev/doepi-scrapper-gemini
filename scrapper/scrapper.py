import os
import sys
import requests
import selenium as sl
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


# webdriver configurations
chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
    "excludeSwitches": ["enable-logging"],
    "profile.default_content_setting_values.automatic_downloads": 2,
    "download.default_directory": "/dev/null",  # Diretório inválido para impedir downloads
    "download.prompt_for_download": False,  # Bloqueia pop-ups de download
    "download.directory_upgrade": False,
    "download.extensions_to_open": "applications/docx",  # Apenas PDF pode abrir, docx fica bloqueado
    "plugins.always_open_pdf_externally": False,  # Impede que PDFs sejam baixados automaticamente
    "safebrowsing.enabled": False,  # Evita avisos de segurança sobre downloads
})


def get_gazzete():
    sys.stderr = open(os.devnull, 'w')

    chrome_options.add_argument(argument="--log-level=3")  # Suprime mensagens de INFO
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.diario.pi.gov.br/doe/")

    gazzete_table = driver.find_element(By.TAG_NAME, "table")
    tbody = gazzete_table.find_element(By.TAG_NAME, "tbody")
    lines = tbody.find_elements(By.TAG_NAME, "tr")
    
    exist_gazzete = 0
    for l in lines:
        td = l.find_elements(By.TAG_NAME, "td")
        file  = td[0].find_element(By.TAG_NAME, "a")
        url_file = file.get_attribute("href")
        file_name = td[1].text
        file_data = td[2].text

        path = "diario/"+file_data.replace("/", "de")+"/"
        # se a pasta já existir, não precisa criá-la novamente
        os.makedirs(path, exist_ok=True)

        gazzete_filename = path+"/"+file_name.replace("/", "_")+".pdf"
        
        download = requests.get(url_file)

        if os.path.exists(gazzete_filename):
            exist_gazzete +=1
            if exist_gazzete == 3:
                break
            else: pass
        
        else:
            with open(gazzete_filename, "wb") as f:
                f.write(download.content)

            print(file_name, "de", file_data, ": ", url_file)