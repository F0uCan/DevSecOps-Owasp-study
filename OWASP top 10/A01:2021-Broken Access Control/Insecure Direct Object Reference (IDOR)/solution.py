# fixed_app_tenant.py
from fastapi import FastAPI, Depends, HTTPException, status
# ... (imports, DB e modelo de dados continuam os mesmos) ...
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

# --- Simulação de um Banco de Dados ---
db_companies = {
    1: {"name": "InnovateCorp"},
    2: {"name": "DataSolutions"},
}

db_projects = {
    101: {"company_id": 1, "name": "Projeto Fênix", "budget": 50000},
    102: {"company_id": 1, "name": "Marketing Digital Q4", "budget": 15000},
    201: {"company_id": 2, "name": "Reestruturação do Big Data", "budget": 120000},
    202: {"company_id": 2, "name": "App Mobile Interno", "budget": 35000},
}

# --- Modelo de Dados (mais complexo) ---
class User(BaseModel):
    username: str
    role: str
    company_id: int

# --- Autenticação (simulada com mais detalhes) ---
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    users_from_tokens = {
        "token_de_bob_empresa1": {"sub": "bob", "role": "member", "cid": 1},
        "token_de_sara_empresa2": {"sub": "sara", "role": "manager", "cid": 2},
    }
    payload = users_from_tokens.get(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    return User(
        username=payload.get("sub"),
        role=payload.get("role"),
        company_id=payload.get("cid")
    )

app = FastAPI()

# O endpoint /my-projects continua igual e seguro.
@app.get("/my-projects")
def get_my_company_projects(current_user: User = Depends(get_current_user)):
    user_company_id = current_user.company_id
    company_projects = [
        proj for proj in db_projects.values() if proj["company_id"] == user_company_id
    ]
    return company_projects

@app.get("/projects/{project_id}")
def get_project_by_id(project_id: int, current_user: User = Depends(get_current_user)):
    """
    CORRIGIDO!
    Agora o endpoint verifica se o projeto pertence à empresa do usuário.
    """
    if project_id not in db_projects:
        raise HTTPException(status_code=404, detail="Project not found")

    project = db_projects[project_id]

    # ADIÇÃO DA VERIFICAÇÃO DE AUTORIZAÇÃO:
    if project["company_id"] != current_user.company_id:
        # Retornamos 404 para não vazar a informação de que o projeto existe.
        raise HTTPException(status_code=404, detail="Project not found")

    return project

# Para rodar: uvicorn fixed_app_tenant:app --reload