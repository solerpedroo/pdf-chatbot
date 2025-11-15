from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import io

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "ok", "message": "PDF Chatbot RAG - API Online!"}

@app.get("/debug")
async def debug():
    from backend.rag import get_documents_status
    status = get_documents_status()
    print(f"DEBUG: {status}")
    return status

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    print(f"\n========== UPLOAD INICIADO ==========")
    print(f"Arquivo: {file.filename}")
    print(f"Content-Type: {file.content_type}")
    
    try:
        print("Passo 1: Lendo bytes...")
        contents = await file.read()
        print(f"✓ Bytes lidos: {len(contents)}")
        
        print("Passo 2: Extraindo texto do PDF...")
        from pypdf import PdfReader
        reader = PdfReader(io.BytesIO(contents))
        print(f"✓ PDF tem {len(reader.pages)} páginas")
        
        text = "\n\n".join([p.extract_text() or "" for p in reader.pages])
        print(f"✓ Texto extraído: {len(text)} caracteres")
        print(f"✓ Primeiros 100 chars: {text[:100]}...")
        
        if not text.strip():
            print("ERRO: PDF sem texto!")
            return JSONResponse({"error": "PDF sem texto"}, status_code=400)
        
        print("Passo 3: Importando módulo rag...")
        from backend import rag
        print(f"✓ Módulo rag importado: {rag}")
        
        print("Passo 4: Chamando add_document...")
        rag.add_document(file.filename, text, {"filename": file.filename})
        
        print("Passo 5: Verificando se salvou...")
        status = rag.get_documents_status()
        print(f"✓ Status após salvar: {status}")
        
        print("========== UPLOAD CONCLUÍDO ==========\n")
        return {"status": "ok", "filename": file.filename, "docs_count": status['total']}
        
    except Exception as e:
        print(f"\n========== ERRO NO UPLOAD ==========")
        print(f"Tipo: {type(e).__name__}")
        print(f"Mensagem: {str(e)}")
        import traceback
        traceback.print_exc()
        print("=====================================\n")
        return JSONResponse({"error": str(e)}, status_code=500)

@app.get("/ask")
async def ask(q: str = ""):
    print(f"\n========== PERGUNTA ==========")
    print(f"Pergunta: {q}")
    
    if not q:
        return JSONResponse({"error": "Pergunta vazia"}, status_code=400)
    
    try:
        print("Verificando documentos disponíveis...")
        from backend.rag import get_documents_status, answer_with_context
        status = get_documents_status()
        print(f"Status: {status}")
        
        if status['total'] == 0:
            print("AVISO: Nenhum documento encontrado!")
            return {"answer": "Nenhum documento encontrado. Por favor, faça upload de um PDF primeiro."}
        
        print("Gerando resposta...")
        answer = answer_with_context(q)
        
        print(f"✓ Resposta: {answer[:100]}...")
        print("========== RESPOSTA ENVIADA ==========\n")
        return {"answer": answer}
        
    except Exception as e:
        print(f"\n========== ERRO NA PERGUNTA ==========")
        print(f"Tipo: {type(e).__name__}")
        print(f"Mensagem: {str(e)}")
        import traceback
        traceback.print_exc()
        print("======================================\n")
        return JSONResponse({"error": str(e)}, status_code=500)