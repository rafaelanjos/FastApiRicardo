from fastapi import FastAPI
from pydantic import BaseModel

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
