import os
from dotenv import load_dotenv
from groq import Groq
import re

# Carregar .env
load_dotenv()

# Lista de modelos disponíveis (em ordem de preferência)
AVAILABLE_MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "mixtral-8x7b-32768",
    "gemma2-9b-it"
]

LLM_MODEL = os.getenv("LLM_MODEL", AVAILABLE_MODELS[0])
GROQ_KEY = os.getenv("GROQ_API_KEY")

# Verificar se a chave foi carregada
if not GROQ_KEY:
    print("ERRO: GROQ_API_KEY não encontrada!")
else:
    print(f"✓ Groq API Key carregada")
    print(f"✓ Modelo selecionado: {LLM_MODEL}")

# Armazenamento em memória simples - GLOBAL
_documents = {}

def add_document(doc_id: str, text: str, metadata: dict = None):
    """Armazena documento em memória"""
    global _documents
    print(f"✓ Salvando documento: {doc_id}")
    
    _documents[doc_id] = {
        'text': text,
        'metadata': metadata or {}
    }
    
    print(f"✓ Total de documentos: {len(_documents)}")

def search_similar(query: str, k: int = 3):
    """Busca simples por palavras-chave"""
    global _documents
    
    if not _documents:
        return []
    
    results = []
    query_lower = query.lower()
    query_words = re.findall(r'\w+', query_lower)
    
    for doc_id, doc_data in _documents.items():
        text = doc_data['text']
        
        chunk_size = 1000
        for i in range(0, len(text), chunk_size):
            chunk = text[i:i+chunk_size]
            chunk_lower = chunk.lower()
            
            score = sum(1 for word in query_words if word in chunk_lower)
            
            if score > 0:
                results.append({
                    'text': chunk,
                    'meta': doc_data['metadata'],
                    'score': score
                })
    
    results.sort(key=lambda x: x['score'], reverse=True)
    return results[:k]

def answer_with_context(question: str, k: int = 3):
    """Gera resposta usando Groq"""
    
    if not GROQ_KEY:
        return "ERRO: Chave do Groq não configurada."
    
    docs = search_similar(question, k=k)
    
    if not docs:
        global _documents
        if _documents:
            first_doc = list(_documents.values())[0]
            context = first_doc['text'][:3000]
        else:
            return "Nenhum documento encontrado. Por favor, faça upload de um PDF primeiro."
    else:
        context = "\n\n---\n\n".join([d['text'] for d in docs])
    
    if len(context) > 6000:
        context = context[:6000] + "..."
    
    prompt = f"""Você é um assistente especializado em análise de documentos. Use o contexto abaixo para responder a pergunta.

IMPORTANTE: Formate sua resposta usando Markdown para melhor legibilidade:
- Use **negrito** para destacar pontos importantes
- Use listas (- ou 1.) quando listar itens
- Separe parágrafos com linha em branco
- Use ## para subtítulos se necessário
- Use > para citações quando citar o documento

Contexto:
{context}

Pergunta: {question}

Resposta (em Markdown):"""
    
    print(f"Gerando resposta com {LLM_MODEL}...")
    
    client = Groq(api_key=GROQ_KEY)
    
    for model in [LLM_MODEL] + [m for m in AVAILABLE_MODELS if m != LLM_MODEL]:
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=model,
                temperature=0.0,
                max_tokens=1024,
            )
            
            answer = chat_completion.choices[0].message.content
            print(f"✓ Resposta gerada ({len(answer)} chars)")
            
            return answer
        
        except Exception as e:
            print(f"Erro com {model}: {e}")
            if model == AVAILABLE_MODELS[-1]:
                return f"Erro ao gerar resposta: {str(e)}"
            continue

def get_documents_status():
    """Retorna status dos documentos"""
    global _documents
    return {
        'total': len(_documents),
        'documents': list(_documents.keys())
    }