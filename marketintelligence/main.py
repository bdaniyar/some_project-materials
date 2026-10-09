from fastapi import FastAPI

app = FastAPI()


@app.post("/generate")
async def generate_secret_key():
    ...

@app.post("/secrets/secret_key")
async def get_secret_data(secret_key: str):
    ...