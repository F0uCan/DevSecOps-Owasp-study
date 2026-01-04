from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from jose import JWTError, jwt
from typing import List

# --- Configurações de Segurança (Simuladas) ---
SECRET_KEY = "uma-chave-secreta-muito-forte"
ALGORITHM = "HS256"

# --- Simulação de um Banco de Dados ---
db_posts = {
    1: {"owner": "alice", "content": "Post da Alice."},
    2: {"owner": "bob", "content": "Post do Bob."},
    3: {"owner": "admin_user", "content": "Post do Admin."},
}

# --- Modelo de Dados ---
class User(BaseModel):
    username: str
    role: str

# --- "Autenticação" ---
# Em um app real, isso viria de um token decodificado e validado.
# Aqui, vamos simular a obtenção do usuário a partir de um token falso.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        # Em um app real, você decodificaria o token e buscaria o usuário no banco.
        # Aqui, vamos simular o payload para fins de exemplo.
        if token == "token_de_alice":
            payload = {"sub": "alice", "role": "user"}
        elif token == "token_de_bob":
            payload = {"sub": "bob", "role": "user"}
        elif token == "token_de_admin":
            payload = {"sub": "admin_user", "role": "admin"}
        else:
            raise JWTError
            
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None or role is None:
            raise credentials_exception
        return User(username=username, role=role)
    except JWTError:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        raise credentials_exception

# --- Aplicação FastAPI ---
app = FastAPI()

@app.get("/posts/{post_id}")
def read_post(post_id: int):
    """Qualquer um pode ler um post."""
    if post_id not in db_posts:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_posts[post_id]

@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, current_user: User = Depends(get_current_user)):
    """
    VULNERABILIDADE AQUI!
    A função verifica se o usuário está logado, mas não verifica se ele
    é o dono do post ou se tem permissão de admin para deletá-lo.
    """
    if post_id not in db_posts:
        raise HTTPException(status_code=404, detail="Post not found")

    # A única verificação é se o usuário está autenticado.
    # Não há controle de acesso para a AÇÃO de deletar.
    del db_posts[post_id]
    return {"message": "Post deleted successfully"}

# Para rodar a aplicação: uvicorn vulnerable_app:app --reload