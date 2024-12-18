import os
from sqlalchemy import create_engine, Column, Integer, Numeric
from sqlalchemy.orm import Session, sessionmaker, declarative_base, DeclarativeMeta
from sqlalchemy.exc import SQLAlchemyError
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import Type


DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


class BaseTable(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True)
    ano = Column(Integer, unique=True, nullable=False)
    receita_liquida = Column(Numeric(12, 2), nullable=False)
    custo_mercadorias = Column(Numeric(12, 2), nullable=False)
    subvencoes_receitas_op = Column(Numeric(12, 2), nullable=False)
    valor_bruto_producao = Column(Numeric(12, 2), nullable=False)
    consumo_intermediario_total = Column(Numeric(12, 2), nullable=False)
    consumo_mercadorias_reposicao = Column(Numeric(12, 2), nullable=False)
    consumo_combustiveis = Column(Numeric(12, 2), nullable=False)
    consumo_servicos_terceiros = Column(Numeric(12, 2), nullable=False)
    consumo_alugueis_imoveis = Column(Numeric(12, 2), nullable=False)
    consumo_seguros = Column(Numeric(12, 2), nullable=False)
    consumo_comunicacao = Column(Numeric(12, 2), nullable=False)
    consumo_energia_gas_agua = Column(Numeric(12, 2), nullable=False)
    consumo_outros_custos = Column(Numeric(12, 2), nullable=False)
    valor_adicionado_bruto = Column(Numeric(12, 2), nullable=False)
    gastos_pessoal_total = Column(Numeric(12, 2), nullable=False)
    gastos_salarios_remuneracoes = Column(Numeric(12, 2), nullable=False)
    gastos_previdencia_social = Column(Numeric(12, 2), nullable=False)
    gastos_fgts = Column(Numeric(12, 2), nullable=False)
    gastos_previdencia_privada = Column(Numeric(12, 2), nullable=False)
    gastos_indenizacoes_trabalhistas = Column(Numeric(12, 2), nullable=False)
    gastos_beneficios_empregados = Column(Numeric(12, 2), nullable=False)
    pis_folha_pagamento = Column(Numeric(12, 2), nullable=False)
    excedente_operacional_bruto = Column(Numeric(12, 2), nullable=False)
    pessoal_ocupado = Column(Numeric(12, 2), nullable=False)
    numero_empresas = Column(Numeric(12, 2), nullable=False)


class Telecom(BaseTable):
    __tablename__ = "telecom"

class Ti(BaseTable):
    __tablename__ = "ti"

class ServAudiovisuais(BaseTable):
    __tablename__ = "serv_audiovisuais"

class EdIntegradasImpressao(BaseTable):
    __tablename__ = "ed_e_ed_integradas_a_impressao"

class AgenciaNoticias(BaseTable):
    __tablename__ = "agencia_noticias"

class DataEntry(BaseModel):
    ano: int
    receita_liquida: float
    custo_mercadorias: float
    subvencoes_receitas_op: float
    valor_bruto_producao: float
    consumo_intermediario_total: float
    consumo_mercadorias_reposicao: float
    consumo_combustiveis: float
    consumo_servicos_terceiros: float
    consumo_alugueis_imoveis: float
    consumo_seguros: float
    consumo_comunicacao: float
    consumo_energia_gas_agua: float
    consumo_outros_custos: float
    valor_adicionado_bruto: float
    gastos_pessoal_total: float
    gastos_salarios_remuneracoes: float
    gastos_previdencia_social: float
    gastos_fgts: float
    gastos_previdencia_privada: float
    gastos_indenizacoes_trabalhistas: float
    gastos_beneficios_empregados: float
    pis_folha_pagamento: float
    excedente_operacional_bruto: float
    pessoal_ocupado: float
    numero_empresas: float

tables = {
    "telecom": Telecom,
    "ti": Ti,
    "serv_audiovisuais": ServAudiovisuais,
    "ed_e_ed_integradas_a_impressao": EdIntegradasImpressao,
    "agencia_noticias": AgenciaNoticias
}

# Função de dependência para obter sessão de banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# FastAPI app
app = FastAPI()

# CRUD Operations (aplica para todas as tabelas)
@app.post("/data/{table}/", response_model=DataEntry)
def create_data(table: str, data_entry: DataEntry, db: Session = Depends(get_db)):
    
    model_class: Type[DeclarativeMeta] = tables.get(table.lower()) 

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
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
