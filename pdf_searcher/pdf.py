import os
import fitz
import requests
import pdfplumber
from dotenv import load_dotenv
from PyPDF2 import PdfWriter, PdfReader

def send_prompt(prompt):

    API_KEY = os.getenv("GEMINI_API_KEY")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

load_dotenv()
gazette_paths = os.getenv("DOEPI_FILEPATH")
decree_paths = os.getenv("DECREE_FILEPATH")
nomination_paths = os.getenv("NOMINATION_FILEPATH")


def decree(pdf_path, pdf_filename, data, h):
    
    index_pages = []

    with pdfplumber.open(pdf_path+pdf_filename) as pdf:

        aux = False
        first_index = 0
        last_index = 1000

        for i, page in enumerate(pdf.pages):
            page_text = page.extract_text()
            
            if page_text:
                if "decretos" in page_text.lower() and i != 1 and aux == False:
                    first_index = i
                    aux = True

                if aux ==True and ("nomeações e/ou exonerações" in page_text.lower() or "importante: decreto nº 19.876, de 15 de julho de 2021" in page_text.lower()):
                    last_index = i
                    break

        if first_index != 0 and last_index != 1000:
            index_pages = [j for j in range(first_index, last_index+1)]  
            
            reader = PdfReader(pdf_path+pdf_filename)
            writer = PdfWriter()

            for j in index_pages:
                writer.add_page(reader.pages[j])

            exit_path = "decretos/"+data+"/"
            os.makedirs(exit_path, exist_ok=True)
            with open(exit_path+pdf_filename, "wb") as exit_pdf:
                writer.write(exit_pdf)
            
            print(f"= {h} =DECRETOS EXTRAÍDOS COM SUCESSO DE {pdf_path+pdf_filename} PARA {exit_path+pdf_filename}")
        else:
            print(f"= {h} =IMPOSSÍVEL EXTRAIR DECRETOS DE {pdf_path+pdf_filename}")
                        

def nomination(pdf_path, pdf_filename, data, h):
    
    index_pages = []

    with pdfplumber.open(pdf_path+pdf_filename) as pdf:

        aux = False
        first_index = 0
        last_index = 1000

        for i, page in enumerate(pdf.pages):
            page_text = page.extract_text()
            
            if page_text:
                if "nomeações e/ou exonerações" in page_text.lower() and i != 1 and aux == False:
                    first_index = i
                    aux = True

                if aux ==True and ("portarias" in page_text.lower() or "importante: decreto nº 19.876, de 15 de julho de 2021" in page_text.lower()):
                    last_index = i
                    break

        if first_index != 0 and last_index != 1000:
            index_pages = [j for j in range(first_index, last_index+1)]  
            
            reader = PdfReader(pdf_path+pdf_filename)
            writer = PdfWriter()

            for j in index_pages:
                writer.add_page(reader.pages[j])

            exit_path = "nomeações eou exonerações/"+data+"/"
            os.makedirs(exit_path, exist_ok=True)
            with open(exit_path+pdf_filename, "wb") as exit_pdf:
                writer.write(exit_pdf)

            print(f"= {h} =NOMEAÇÕES E EXONERAÇÕES EXTRAÍDAS COM SUCESSO DE {pdf_path+pdf_filename} PARA {exit_path+pdf_filename}")
        else:
            print(f"= {h} =IMPOSSÍVEL EXTRAIR NOMEAÇÕES E EXONERAÇÕES DE {pdf_path+pdf_filename}")

def find_decree():
    # percorrendo todos os diarios
    h=1
    for data in os.listdir(gazette_paths):
        for pdf_filename in os.listdir(gazette_paths+"/"+data):
            pdf_path = gazette_paths+"/"+data+"/"
            if os.path.exists(decree_paths+"/"+data+"/"): pass
            else:
                decree(pdf_path, pdf_filename, data, h)
                h+=1

def find_nomination():
    # percorrendo todos os diarios
    h=1
    for data in os.listdir(gazette_paths):
        for pdf_filename in os.listdir(gazette_paths+"/"+data):
            pdf_path = gazette_paths+"/"+data+"/"
            if os.path.exists(nomination_paths+"/"+data+"/"): pass
            else:
                nomination(pdf_path, pdf_filename, data, h)
                h+=1


def gemini_decree(pdf_filename, pdf_text):

    prompt = (
    f"Analise o seguinte texto de decreto e resuma as seguintes informações:"
    f"o número do decreto, a data, o objeto do decreto, os envolvidos e a data de vigência.\n"
    f"{pdf_text}.\nRetorne um dicionário Python como texto com as seguintes chaves preenchidas: \n"
    f"'Número', 'Data de vigência', 'Objeto', 'Envolvidos'."
    )

    print(f"Insights para {pdf_filename}")

    resp = send_prompt(prompt=prompt)
    if 'error' in resp:
        print(resp)
    else:
        print("RESPOSTA: ", resp['candidates'][0]['content']['parts'][0]['text'])

    print("-" * 50)


def show_decree():
    decree_dict = {}
    j=1
    for data in os.listdir(decree_paths):
        for pdf_filename in os.listdir(decree_paths+"/"+data):
            decree_dict[j] = pdf_filename
            j+=1

    for i in range(len(decree_dict)):
        print(f"={i+1}= {decree_dict[i+1]}")

    return decree_dict


def show_cropped_decree(decree_pdf_path):
    os.startfile(decree_pdf_path)

def insights_decree():
    # percorrendo todos os decretos
    
    decree_dict = show_decree()
    pdf_index = int(input("= "))

    for data in os.listdir(decree_paths):
        for pdf_filename in os.listdir(decree_paths+"/"+data):
            if pdf_filename == decree_dict[pdf_index]:
                pdf_path = decree_paths+"/"+data+"/"
                
                pdf_doc = fitz.open(pdf_path+"/"+pdf_filename)
                text = ""
                for page in pdf_doc:
                    text += page.get_text()

                gemini_decree(pdf_filename, text)
                show_cropped_nomination(decree_paths+"/"+data+"/"+pdf_filename)


def gemini_nomination(pdf_filename, pdf_text):

    prompt = (
    f"Analise o seguinte texto e resuma as seguintes informações:"
    f" a data das nomeações e exonerações, a quantidade de nomeações e "
    f"exonerações e os funcionários nomeados e exonerados, bem como os seus respectivos cargos.\n"
    f"{pdf_text}.\nRetorne um dicionário Python como texto com as seguintes chaves preenchidas, logo abaixo da quantidade de nomeações"
    f" e exonerações: 'Situação (nomeação ou exoneração)', 'Data de vigência', 'Funcionário', 'Cargo'" 
    )

    print(f"Insights para {pdf_filename}")

    resp = send_prompt(prompt=prompt)
    
    if 'error' in resp:
        print(resp)
    else:
        print("RESPOSTA: ", resp['candidates'][0]['content']['parts'][0]['text'])

    print("-" * 50)


def show_nomination():
    nomination_dict = {}
    j=1
    for data in os.listdir(nomination_paths):
        for pdf_filename in os.listdir(nomination_paths+"/"+data):
            nomination_dict[j] = pdf_filename
            j+=1

    for i in range(len(nomination_dict)):
        print(f"={i+1}= {nomination_dict[i+1]}")

    return nomination_dict


def show_cropped_nomination(nomination_pdf_path):
    os.startfile(nomination_pdf_path)


def insights_nomination():
    nomination_dict = show_nomination()
    pdf_index = int(input("= "))

    for data in os.listdir(nomination_paths):
        for pdf_filename in os.listdir(nomination_paths+"/"+data):
            if pdf_filename == nomination_dict[pdf_index]:
                pdf_path = nomination_paths+"/"+data+"/"
                
                pdf_doc = fitz.open(pdf_path+"/"+pdf_filename)
                text = ""
                for page in pdf_doc:
                    text += page.get_text()
                
                gemini_nomination(pdf_filename, text)
                show_cropped_nomination(nomination_paths+"/"+data+"/"+pdf_filename)
