from sqlalchemy.orm import Session, DeclarativeMeta
from sqlalchemy.exc import SQLAlchemyError
from fastapi import FastAPI, Depends, HTTPException
from typing import Generator, Any, Type, Dict
from utils.db.GeradorDeTabelas import create_tables
from utils.db.GeradorDeSessao import GerarSessao
from utils.db import ModeloDeDadosDeEnvio
import uvicorn
import os

tabelas = ["telecom", "ti", "serv_audiovisuais", "ed_e_ed_integradas_a_impressao", "agencia_noticias"]

tabelas_geradas: Dict[str, Type[DeclarativeMeta]]  = create_tables(table_names=tabelas)

database_url = os.getenv("DATABASE_URL")
if database_url is None:
    raise ValueError("DATABASE_URL env está vazia!")

conn = GerarSessao(database_url=database_url)

DataEntry = ModeloDeDadosDeEnvio.DataEntry  

app = FastAPI()

TABLE_NOT_FOUND = "Table not found"
DATA_NOT_FOUND = "Data not found"

def get_db() -> Generator[Session, None, None]:
    """Usar o generator da classe GerarSessao"""
    for db in conn.get_db():
        yield db


@app.post("/data/{table}/", response_model=DataEntry)
def create_data(table: str, data_entry: DataEntry, db: Session = Depends(get_db)) -> Any:

    if (model_class := tabelas_geradas.get(table.lower())) is None:
        raise HTTPException(status_code=404, detail=TABLE_NOT_FOUND)
    
    try:
        new_entry = model_class(**data_entry.dict())
        db.add(new_entry)
        db.commit()
        db.refresh(new_entry)
        return new_entry
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Transaction error: {e}")
    

@app.get("/data/{table}/", response_model=list[DataEntry])
def get_data(table: str, db: Session = Depends(get_db)) -> list[Any]:
    model_class = tabelas_geradas.get(table.lower())
    if not model_class:
        raise HTTPException(status_code=404, detail=TABLE_NOT_FOUND)
    data = db.query(model_class).all()
    return data

@app.get("/data/{table}/{year}", response_model=DataEntry)
def get_data_by_year(table: str, year: int, db: Session = Depends(get_db)) -> Any:
    model_class = tabelas_geradas.get(table.lower())
    if not model_class:
        raise HTTPException(status_code=404, detail=TABLE_NOT_FOUND)
    data = db.query(model_class).filter(getattr(model_class, "ano") == year).first()
    if not data:
        raise HTTPException(status_code=404, detail=DATA_NOT_FOUND)
    return data

@app.put("/data/{table}/{year}", response_model=DataEntry)
def update_data(table: str, year: int, data_entry: DataEntry, db: Session = Depends(get_db)) -> Any:
    model_class = tabelas_geradas.get(table.lower())
    if not model_class:
        raise HTTPException(status_code=404, detail=TABLE_NOT_FOUND)
    existing_data = db.query(model_class).filter(getattr(model_class, "ano") == year).first()
    if not existing_data:
        raise HTTPException(status_code=404, detail=DATA_NOT_FOUND)
    for key, value in data_entry.dict().items():
        setattr(existing_data, key, value)
    db.commit()
    db.refresh(existing_data)
    return existing_data

@app.delete("/data/{table}/{year}", response_model=dict)
def delete_data(table: str, year: int, db: Session = Depends(get_db)) -> dict:
    model_class = tabelas_geradas.get(table.lower())
    if not model_class:
        raise HTTPException(status_code=404, detail=TABLE_NOT_FOUND)
    data = db.query(model_class).filter(getattr(model_class, "ano") == year).first()
    if not data:
        raise HTTPException(status_code=404, detail=DATA_NOT_FOUND)
    db.delete(data)
    db.commit()
    return {"detail": "Data deleted successfully"}

# Iniciar o servidor FastAPI
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
