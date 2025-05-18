from sqlalchemy import Column, Integer, Numeric
from typing import Type
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.ext.declarative import declarative_base

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

def create_tables(table_names: list[str])-> dict[str, Type[DeclarativeMeta]]:
    """
    Cria as tabelas no banco de dados com base nos nomes fornecidos.Eles devem ser separados por underscores.
    """

    class_names = [name.lower() for name in table_names]

    classes = {
        name: type(name.capitalize(), (BaseTable,), {"__tablename__": name})
        for name in class_names            
    }
    
    return classes
