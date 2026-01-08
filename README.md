# 🕵️‍♂️ DOEPI-Scrapper-Gemini

Um coletor (scraper) automatizado para o Diário Oficial do Estado do Piauí (DOE-PI) com foco em extração e organização de documentos relevantes (decretos, diários oficiais, nomeações/exonerações etc.), possivelmente integrando capacidades de IA para auxiliar no processamento e análise de conteúdo.
Este projeto foi desenvolvido para automatizar a captura e pré-processamento de documentos públicos, facilitando o uso dos dados em aplicações de busca, análise ou consulta automatizada.
O projeto foi paralizado em Setembro de 2025, mas será continuado.

## 🧠 Funcionalidade

✔ Baixa conteúdo público do Diário Oficial do Estado do Piauí
✔ Organiza documentos por tipo (decretos, diários, ato administrativo, etc.)
✔ Possibilidade de integração com modelos de IA (como Gemini ou outro) para análise ou classificação dos textos
✔ Interface Python simples para automação

## 📂 Estrutura do Repositório

├── decretos/                  # Decretos extraídos
├── diario/                    # Arquivos ou PDFs de diários oficiais
├── front/                     # Código front-end (interface de visualização?)
├── nomeações eou exonerações/ # Nomeações e exonerações capturadas
├── pdf_searcher/              # Scripts para localizar e extrair texto de PDFs
├── scrapper/                  # Scripts de scraping
├── main.py                    # Script principal de execução
└── readme.md                  # Documento com instruções (atualmente vazio)

## 🚀 Instalação

Clone o repositório:

git clone https://github.com/carlos-dani-dev/doepi-scrapper-gemini.git
cd doepi-scrapper-gemini


Crie um ambiente virtual (recomendado):

python3 -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows


Instale as dependências (se houver um requirements.txt):

pip install -r requirements.txt

## ▶️ Como Usar
🪝 1. Configurar variáveis / parâmetros

Antes de rodar o scraper, ajuste as configurações no main.py ou nos scripts correspondentes para indicar:

✔ URLs de onde os dados devem ser extraídos
✔ Padrões de arquivos que você deseja baixar
✔ Local de saída dos dados

🧾 2. Executar o scraper
python main.py


O script principal (main.py) deve iniciar o processo de coleta de documentos, salvar os PDFs/textos localmente e organizá-los nas pastas correspondentes.

🧠 3. (Opcional) Processar textos com IA

Se o projeto integrar algum módulo de IA (por exemplo, usando um modelo como Gemini para resumo/classificação), adicione as chaves de API necessárias e ajuste os módulos para processar os textos extraídos.

## 🧰 Possíveis usos

✅ Pesquisa automatizada no Diário Oficial
✅ Extração e classificação de atos administrativos
✅ Construção de bases de dados para análise jurídica ou de políticas públicas
✅ Integração com chatbots ou ferramentas de busca semântica

