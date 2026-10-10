from fastapi import FastAPI, Depends, Body
from models import get_session, add_secret_record, setup_db, reveal_secret_data
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from security import security_instance
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(_: FastAPI):
    await setup_db()
    yield



app = FastAPI(lifespan=lifespan)

DBDep =  Annotated[AsyncSession, Depends(get_session)]


@app.post("/generate")
async def generate_secret_key(
    session: DBDep,
    secret_data: str = Body(embed=True),
):
    encrypted_data = security_instance.encrypt_data(secret_data)
    secret_id = security_instance.create_secret_key()
    await add_secret_record(session, secret_id, encrypted_data, None)
    return {"secret_key": secret_id}



@app.post("/secrets/secret_key")
async def get_secret_data(secret_key: str, session: DBDep):
    encrypted_secret = await reveal_secret_data(session, secret_key, hashed_password=None)
    decrypted_secret = security_instance.decrypt_data(encrypted_secret)
    return {"secret_data": decrypted_secret}