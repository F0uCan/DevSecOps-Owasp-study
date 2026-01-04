from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from jose import JWTError, jwt
from typing import List

# --- (O código de setup, DB, User, get_current_user continua o mesmo) ---
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
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
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
def read_post(post_id: int, current_user: User = Depends(get_current_user)):
    if post_id not in db_posts:
        raise HTTPException(status_code=404, detail="Post not found")
    
    get_post_id = db_posts[post_id]
    if get_post_id["owner"] != current_user.username and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="get out of here.",
        )
    return db_posts[post_id]

@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, current_user: User = Depends(get_current_user)):
    """
    CORRIGIDO!
    Agora verificamos as permissões do usuário antes de realizar a ação.
    """
    if post_id not in db_posts:
        raise HTTPException(status_code=404, detail="Post not found")

    post_to_delete = db_posts[post_id]
    
    # LÓGICA DE AUTORIZAÇÃO:
    # A ação só é permitida se o usuário for o dono do post OU se ele for um admin.
    if post_to_delete["owner"] != current_user.username and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to delete this post",
        )
        
    del db_posts[post_id]
    return {"message": "Post deleted successfully"}

# Para rodar a aplicação: uvicorn fixed_app:app --reload