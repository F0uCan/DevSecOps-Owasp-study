import os
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from typing import Optional
from contextlib import asynccontextmanager  # 1. Importar o gerenciador de contexto

# --- Setup: Função para criar os arquivos ---
def setup_database():
    if not os.path.exists("./logs"):
        os.makedirs("./logs")
    with open("./logs/app.log", "w") as f:
        f.write("INFO: Application started.\n")
    with open("./secrets.txt", "w") as f:
        f.write("THIS_IS_A_VERY_SECRET_API_KEY_12345")
# --- Fim do Setup ---

# 2. Criar o gerenciador de ciclo de vida (lifespan)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Código para rodar na inicialização
    setup_database()
    print("Servidor iniciando... arquivos de log e secrets criados.")
    yield
    # Código para rodar no desligamento (opcional)
    print("Servidor desligando...")

# 3. Registrar o lifespan na aplicação FastAPI
app = FastAPI(lifespan=lifespan)

@app.get("/view-file", response_class=PlainTextResponse)
def view_file(filename: str):
    """
    VULNERABLE ENDPOINT!
    It trusts the 'filename' parameter completely.
    """
    
    file_path = f"./logs/{filename}"
    
    try:
        with open(file_path, "r") as f:
            content = f.read()
        return content
    except FileNotFoundError:
        return "File not found."
    except Exception as e:
        return f"An error occurred: {e}"