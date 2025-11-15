📚 PDF Chatbot – AI Powered

Aplicação simples e eficiente que utiliza Groq LLM para realizar leitura, análise e interação com PDFs, direto pelo navegador.
Backend em Python + FastAPI e frontend estático minimalista.

🚀 Tecnologias Utilizadas
Backend

Python 3.8+

FastAPI

Groq Python SDK

Uvicorn

dotenv (variáveis de ambiente)

Frontend

HTML5 + CSS3 + JavaScript Vanilla

UI simples e direta

Comunicação com o backend via Fetch API

📋 Pré-requisitos

Python 3.8 ou superior

Conta no Groq (para obter sua GROQ_API_KEY)

Navegador atualizado

🔧 Instalação
1. Clone o repositório
git clone https://github.com/solerpedroo/pdf-chatbot.git
cd pdf-chatbot

2. Instale as dependências
python -m pip install -r backend/requirements.txt

3. Configure suas variáveis de ambiente

Crie um arquivo .env dentro de /backend, com a estrutura abaixo:

GROQ_API_KEY=CHAVE_AQUI
CHROMA_PERSIST_DIR=./chroma_db
EMBEDDING_MODEL=all-MiniLM-L6-v2
LLM_MODEL=llama-3.3-70b-versatile

4. Inicie o servidor backend
uvicorn backend.app:app --port 8000

5. Inicie o frontend

Abra o arquivo:

frontend/index.html


Você pode abrir direto no navegador
📌 ou usar extensões como Live Server para auto-reload.

📁 Estrutura do Projeto
pdf-chatbot/

├── backend/

│   ├── app.py              # API principal (FastAPI)

│   ├── services/

│   │   └── pdf_reader.py   # Lógica de leitura/análise de PDFs

│   ├── .env                # Variáveis de ambiente

│   └── requirements.txt    # Dependências Python

│

├── frontend/

│   ├── index.html          # Interface do usuário

│

└── README.md

🎯 Funcionalidades
📄 Leitura de PDF

Faz upload do PDF

Extrai o conteúdo automaticamente

🤖 Análise via Groq LLM

Responde perguntas sobre o PDF

Gera resumos

Explica partes específicas

Analisa e interpreta o conteúdo

💬 Chat com contexto

Conversa com o PDF em linguagem natural

Histórico de mensagens preservado durante a sessão

🎨 Características do Design

UI limpa e objetiva

Fluxo rápido: upload → análise → perguntas

Respostas em tempo real usando Groq LLM


Layout responsivo

