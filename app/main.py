import secrets
import cipher
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()

security = HTTPBasic()

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "123")
    correct_password = secrets.compare_digest(credentials.password, "1234")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    elif correct_username and correct_password:
        return True


@app.get("/encode/{message}")
def encode(message: str, is_authenticated: str = Depends(get_current_username)):
    if is_authenticated == True:
        return {"Response": cipher.encode_message(message)}


@app.get("/decode/{message}")
def decode(message: str, is_authenticated: str = Depends(get_current_username)):
    if is_authenticated == True:
        return {"Response": cipher.decode_message(message)}


@app.get("/add_key/{key}")
def decode(key: str, is_authenticated: str = Depends(get_current_username)):
    if is_authenticated == True:
        if cipher.add_key(key) == True:
            return {"KEY accepted"}
        else:
            return {"KEY not accepted"}
