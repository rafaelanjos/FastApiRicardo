from typing import List
import databases
import sqlalchemy

from fastapi import FastAPI
from pydantic import BaseModel

DATABASE_URL = "sqlite:///./FastRicardoDB.db"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

# Criando um squema para tabela tarefas
tarefas = sqlalchemy.Table(
    "tarefas",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("nome", sqlalchemy.String),
    sqlalchemy.Column("concluido", sqlalchemy.Boolean),
)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)


app = FastAPI()


class Tarefa(BaseModel):
    id: int
    name: str
    concluido: bool


lista_tarefas_db = []


@app.get("/")
async def home_or_index():
    return "Pagina inicial"


@app.get("/api/tarefas")
async def get_terefas():
    return lista_tarefas_db


@app.post("/api/tarefas")
async def create_tarefa(tarefa: Tarefa):
    lista_tarefas_db.append(tarefa)
    return tarefa
