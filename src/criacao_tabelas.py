import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pandas as pd
import numpy as np
import warnings
from utils.db.GeradorDeSessao import GerarSessao
from sqlalchemy import text
from typing import Dict
from sqlalchemy.engine import Engine


warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=pd.errors.SettingWithCopyWarning)
pd.options.display.float_format = '{:.2f}'.format

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise ValueError("DATABASE_URL env está vazia!")

sessao = GerarSessao(DATABASE_URL)

engine: Engine = sessao.get_engine

dataframes: Dict[str, pd.DataFrame] = {}
dataframes_atualizados: Dict[str, pd.DataFrame] = {}

def executar_sql(sql_file_path: str) -> None:
    with open(sql_file_path, 'r') as file:
        sql_script = file.read()

    with engine.connect() as conn:
        conn.execute(text(sql_script).execution_options(autocommit=True))
    

def replace_outliers_by_median(df: pd.DataFrame, col: pd.Series) -> None:

    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    median = df[col].median()

    df.loc[df[col] < lower_bound, col] = median
    df.loc[df[col] > upper_bound, col] = median


def gerar_dataframes(xls: pd.ExcelFile, sheet_name: str ,sheet_renames: Dict[str, str]) -> None:

    if sheet_name in sheet_renames:

                    if sheet_name in sheet_renames.keys():
                        df_nome = sheet_renames[sheet_name]
                    else:
                        df_nome = sheet_name  

                    df = pd.read_excel(xls, sheet_name=sheet_name, skiprows=4)
                    dataframes[df_nome] = df

def carregar_dfs(path: str) -> None:
 
    for arquivo in os.listdir(path):
        if arquivo.endswith(".xlsx"):
            file_path = os.path.join(path, arquivo)
            xls = pd.ExcelFile(file_path)
            sheet_renames = {
                'Brasil; Telecomunicações': 'telecom',
                'Brasil; Tecnologia da inform...': 'ti',
                'Brasil; Serviços audiovisuais': 'serv_audiovisuais',
                'Brasil; Edição e edição inte...': 'ed_e_ed_integradas_a_impressao',
                'Brasil; Agências de notícias...': 'agencia_noticias',
                'Notas': 'notas'
            }
            for sheet_name in xls.sheet_names:
                gerar_dataframes(xls, sheet_name, sheet_renames)
                
    
def tratar_df(df: pd.DataFrame) -> pd.DataFrame:
    
    nomes_colunas = ['ano', 'receita_liquida','coef_var_receita_liquida',                             'custo_mercadorias', 'coef_var_custo_mercadorias','subvencoes_receitas_op',                                         'coef_var_subvencoes_receitas', 'valor_bruto_producao','coef_var_valor_bruto_producao',                                        'consumo_intermediario_total', 'coef_var_consumo_intermediario_total',                                         'consumo_mercadorias_reposicao', 'coef_var_consumo_mercadorias_reposicao',                                        'consumo_combustiveis', 'coef_var_combustiveis', 'consumo_servicos_terceiros',                                        'coef_var_servicos_terceiros', 'consumo_alugueis_imoveis','coef_var_alugueis_imoveis',                                        'consumo_seguros', 'coef_var_seguros', 'consumo_comunicacao', 'coef_var_comunicacao',                                        'consumo_energia_gas_agua', 'coef_var_energia_gas_agua', 'consumo_outros_custos',                                        'coef_var_outros_custos', 'valor_adicionado_bruto', 'coef_var_valor_adicionado_bruto',                                        'gastos_pessoal_total', 'coef_var_gastos_pessoal_total', 'gastos_salarios_remuneracoes',                                         'coef_var_salarios_remuneracoes', 'gastos_previdencia_social',                                         'coef_var_previdencia_social', 'gastos_fgts', 'coef_var_fgts',                                         'gastos_previdencia_privada', 'coef_var_previdencia_privada',                                         'gastos_indenizacoes_trabalhistas', 'coef_var_indenizacoes_trabalhistas',                                         'gastos_beneficios_empregados', 'coef_var_beneficios_empregados', 'pis_folha_pagamento',                                         'coef_var_pis_folha_pagamento', 'excedente_operacional_bruto',                                         'coef_var_excedente_operacional_bruto', 'pessoal_ocupado', 'coef_var_pessoal_ocupado',                                         'numero_empresas', 'coef_var_numero_empresas']

    colunas_selecionadas = [col for col in nomes_colunas if "coef" not in col]
    

    if len(nomes_colunas) == len(df.columns):
        df.columns = nomes_colunas

    df = df[colunas_selecionadas].copy()
        
    df = df.iloc[:-1, :]

    df['ano'] = pd.to_datetime(df['ano'])
    df['ano'] = df['ano'].dt.year

    colunas_selecionadas= [col for col in df.columns if "ano" not in col]
    df.replace(['-', '...'], np.nan, inplace=True)
    df[colunas_selecionadas].apply(pd.to_numeric)

    for col in colunas_selecionadas:
        if df[col].dtype != "float64":
            df[col] = pd.to_numeric(df[col])
        df[col] = df[col] * 1000

    for col in colunas_selecionadas:
        replace_outliers_by_median(df[colunas_selecionadas], col)
        df[col].fillna(df[col].median(), inplace=True)
    return df

# Descomente e execute o seguinte comando apenas se você for rodar o projeto na sua máquina local. Não vai funcionar no render. 

executar_sql('./db/create_tables.sql');

carregar_dfs('./datasets/')    

for key,value in dataframes.items():
    if key != "notas":
        dataframes_atualizados[key] = tratar_df(value)

try:
    for key,value in dataframes_atualizados.items():
        value.to_sql(f'{key}', engine, index=False)
except Exception as e:
    print(f"Erro ao configurar o banco de dados: {e}")
    print("Prosseguindo sem falha crítica no setup.")