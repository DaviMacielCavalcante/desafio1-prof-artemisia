CREATE OR REPLACE FUNCTION criar_tabelas(nomes TEXT[]) 
RETURNS VOID AS $$
DECLARE 
	nome TEXT;
BEGIN
	FOREACH nome IN ARRAY nomes
	LOOP
		BEGIN
			EXECUTE format($fmt$
				CREATE TABLE IF NOT EXISTS % (
				id SERIAL PRIMARY KEY,
				ano INT UNIQUE NOT NULL,
				receita_liquida NUMERIC(12,2) NOT NULL,	
				custo_mercadorias NUMERIC(12,2) NOT NULL,	
				subvencoes_receitas_op NUMERIC(12,2) NOT NULL,	
				valor_bruto_producao NUMERIC(12,2) NOT NULL,	
				consumo_intermediario_total NUMERIC(12,2) NOT NULL, 	
				consumo_mercadorias_reposicao NUMERIC(12,2) NOT NULL,	
				consumo_combustiveis NUMERIC(12,2) NOT NULL, 	
				consumo_servicos_terceiros NUMERIC(12,2) NOT NULL,	
				consumo_alugueis_imoveis NUMERIC(12,2) NOT NULL,	
				consumo_seguros NUMERIC(12,2) NOT NULL, 	
				consumo_comunicacao NUMERIC(12,2) NOT NULL, 
				consumo_energia_gas_agua NUMERIC(12,2) NOT NULL,  
				consumo_outros_custos NUMERIC(12,2) NOT NULL,
				valor_adicionado_bruto NUMERIC(12,2) NOT NULL, 
				gastos_pessoal_total NUMERIC(12,2) NOT NULL, 
				gastos_salarios_remuneracoes NUMERIC(12,2) NOT NULL,
				gastos_previdencia_social NUMERIC(12,2) NOT NULL,
				gastos_fgts NUMERIC(12,2) NOT NULL,
				gastos_previdencia_privada NUMERIC(12,2) NOT NULL,
				gastos_indenizacoes_trabalhistas NUMERIC(12,2) NOT NULL,
				gastos_beneficios_empregados NUMERIC(12,2) NOT NULL, 
				pis_folha_pagamento NUMERIC(12,2) NOT NULL,
				excedente_operacional_bruto NUMERIC(12,2) NOT NULL,     
				pessoal_ocupado NUMERIC(12,2) NOT NULL, 
				numero_empresas NUMERIC(12,2) NOT NULL
			)
			$fmt$, nome);
			 RAISE NOTICE 'Tabela % criada com sucesso.', nome;
        EXCEPTION
            WHEN OTHERS THEN
                RAISE WARNING 'Erro ao criar a tabela %: %', nome, SQLERRM;
		END;
	END LOOP;
END;
$$ LANGUAGE plpgsql;

SELECT criar_tabelas(ARRAY['telecom', 'agencia_noticias', 'ti', 'serv_audiovisuais', 'ed_e_ed_integradas_a_impressao']);