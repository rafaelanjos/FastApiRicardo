from calendar import c
from email.policy import default
from pickle import FALSE, TRUE
from typing import List
import databases
import sqlalchemy
from sqlalchemy import delete, update, insert, select

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

DATABASE_URL = "sqlite:///./FastRicardoDB.db"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

# Criando um squema para tabela tarefas
tarefas = sqlalchemy.Table(
    "tarefas",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("descricao", sqlalchemy.String),
    sqlalchemy.Column("concluido", sqlalchemy.Boolean),
)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)


app = FastAPI()

# Classe modelo de negocio
class Tarefa(BaseModel):
    id: int
    descricao: str
    concluido: bool

class TarefaCadastro(BaseModel):
    descricao: str


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
async def home_or_index():
    return "Pagina inicial"


@app.get("/api/tarefas", response_model=List[Tarefa])
async def get_terefas():
    query = tarefas.select()
    return await database.fetch_all(query)


@app.post("/api/tarefas", response_model=Tarefa)
async def create_tarefa(tarefa: TarefaCadastro):
    query = tarefas.insert().values(descricao=tarefa.descricao, concluido=False)
    last_record_id = await database.execute(query)
    return Tarefa(id=last_record_id, descricao=tarefa.descricao, concluido=False)

@app.delete("/api/tarefas/{id}")
async def delete_tarefa(id: int):
    return await database.execute(tarefas.delete().where(tarefas.c.id==id))
    


@app.get("/api/tarefas/{id}", response_model=Tarefa)
async def get_terefa(id: int):
    query = tarefas.select().where(tarefas.c.id==id) # Estou montando uma consulta.
    model = await database.fetch_one(query) # Executei uma consulta no banco e aguarda o retorno de um objeto tarefa.
    if model: # Se model tem valor?
        return model
    else:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada.")
        

        
#deixe por ultimo
#@app.put("/api/tarefas/concluido/{id}", response_model=Tarefa)
#async def update_tarefa(id: int):
    # codigo inicio
    # buscar no banco pelo ID (cenario registro que existe) (2 linhas de codigo)
    # tarefa.concluido = not tarefa.concluido
    # atualiza o banco de dados com o novo valor do atributo concluido (update) (2 linhas de codigo)
    # retornar objeto tarefa alterado
    #return Tarefa(id=id, descricao=f"Você deve trocar o valor de concluido. da tarefa {id}", concluido=False)
    #codigo termino

    #depois - depois que o update tiver funcionando
    #se registro da tarefa não existe retorne status code 404 - Not Found