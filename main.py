from sqlalchemy.orm import Session, DeclarativeMeta
from sqlalchemy.exc import SQLAlchemyError
from fastapi import FastAPI, Depends, HTTPException
from typing import Type
from utils.db.GeradorDeTabelas import create_tables
from utils.db.GeradorDeSessao import get_db
from utils.db import ModeloDeDadosDeEnvio
import uvicorn

tabelas = ["telecom", "ti", "serv_audiovisuais", "ed_e_ed_integradas_a_impressao", "agencia_noticias"]

tabelas_geradas  = create_tables(table_names=tabelas)

get_db()

DataEntry = ModeloDeDadosDeEnvio.DataEntry  

# FastAPI app
app = FastAPI()

# CRUD Operations (aplica para todas as tabelas)
@app.post("/data/{table}/", response_model=DataEntry)
def create_data(table: str, data_entry: DataEntry, db: Session = Depends(get_db)):
    
    model_class: Type[DeclarativeMeta] = tabelas_geradas.get(table.lower()) 

    if not model_class:
        raise HTTPException(status_code=404, detail="Table not found")
    
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
def get_data(table: str, db: Session = Depends(get_db)):
    model_class = globals().get(table.capitalize())
    if not model_class:
        raise HTTPException(status_code=404, detail="Table not found")
    data = db.query(model_class).all()
    return data

@app.get("/data/{table}/{year}", response_model=DataEntry)
def get_data_by_year(table: str, year: int, db: Session = Depends(get_db)):
    model_class = globals().get(table.capitalize())
    if not model_class:
        raise HTTPException(status_code=404, detail="Table not found")
    data = db.query(model_class).filter(model_class.ano == year).first()
    if not data:
        raise HTTPException(status_code=404, detail="Data not found")
    return data

@app.put("/data/{table}/{year}", response_model=DataEntry)
def update_data(table: str, year: int, data_entry: DataEntry, db: Session = Depends(get_db)):
    model_class = globals().get(table.capitalize())
    if not model_class:
        raise HTTPException(status_code=404, detail="Table not found")
    existing_data = db.query(model_class).filter(model_class.ano == year).first()
    if not existing_data:
        raise HTTPException(status_code=404, detail="Data not found")
    for key, value in data_entry.dict().items():
        setattr(existing_data, key, value)
    db.commit()
    db.refresh(existing_data)
    return existing_data

@app.delete("/data/{table}/{year}", response_model=dict)
def delete_data(table: str, year: int, db: Session = Depends(get_db)):
    model_class = globals().get(table.capitalize())
    if not model_class:
        raise HTTPException(status_code=404, detail="Table not found")
    data = db.query(model_class).filter(model_class.ano == year).first()
    if not data:
        raise HTTPException(status_code=404, detail="Data not found")
    db.delete(data)
    db.commit()
    return {"detail": "Data deleted successfully"}

# Iniciar o servidor FastAPI
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
