from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def get(line: str):
    return {"Hello": "World"}