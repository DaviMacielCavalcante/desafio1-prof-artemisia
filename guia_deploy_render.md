# Um pequeno guia sobre como fazer o deploy deste projeto no Render

Após a criação da conta:

1. Crie uma instância do Postgres 
2. Coloque as variáveis de ambiente que estão lá em um arquivo local chamado ```.env``` na raiz do projeto.
3. Crie o arquivo ```build.sh```, e adicione a seguinte linha: 
```bash
uvicorn main:app --host 0.0.0.0 --port $PORT 
``` 
4. Crie um arquivo chamado ```render.yaml``` com as seguintes configurações:
```yaml
services:
  - type: web
    name: desafio-app
    env: python
    buildCommand: |
      pip install -r requirements.txt
    startCommand: |
      uvicorn main:app --host 0.0.0.0 --port 10000
    plan: free
```
5. Faça um conexão a partir da sua máquina com o Postgres do render, crie e rode a função de criação de tabelas no arquivo ```create_tables_.sql```

6. Rode o seguinte o comando para **CADA TABELA** do banco:

```sql
ALTER TABLE nome_da_tabela ADD COLUMN id SERIAL PRIMARY KEY;
```
Por alguma razão, mesmo estando no ```create_tables.sql```, a coluna ```id``` não é criada então esta etapa deve ser executada.

7. Rode o script ```criacao_tabelas.py```:

```bash
python criacao_tabelas.py
```

Seguindo esses passos, você pode fazer o deploy do projeto no Render, e a API deve funcionar normalmente.