from fastapi import FastAPI
import cipher

app = FastAPI()


@app.get("/encode")
def encode(message: str, key: str):
    if cipher.add_key(key) == True:
        return {"Response": cipher.encode_message(message)}
    else:
        return {"KEY not accepted"}


@app.get("/decode")
def decode(message: str, key: str):
    if cipher.add_key(key) == True:
        return {"Response": cipher.decode_message(message)}
    else:
        return {"KEY not accepted"}
