CREATE OR REPLACE FUNCTION adicionar_coluna_id_para_tabelas(nomes TEXT[]) 
RETURNS VOID AS $$
DECLARE 
    nome TEXT;
    coluna_existe BOOLEAN;
BEGIN
    FOREACH nome IN ARRAY nomes
    LOOP
        BEGIN
            SELECT EXISTS (
                SELECT 1 
                FROM information_schema.columns 
                WHERE table_schema = 'public'
                AND table_name = nome 
                AND column_name = 'id'
            ) INTO coluna_existe;
            
            IF NOT coluna_existe THEN
                EXECUTE format('ALTER TABLE %I ADD COLUMN id SERIAL PRIMARY KEY', nome);
                RAISE NOTICE 'Coluna id adicionada à tabela % com sucesso.', nome;
            ELSE
                RAISE NOTICE 'Coluna id já existe na tabela %.', nome;
            END IF;
            
        EXCEPTION
            WHEN OTHERS THEN
                RAISE WARNING 'Erro ao adicionar coluna id na tabela %: %', nome, SQLERRM;
        END;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

SELECT adicionar_coluna_id_para_tabelas(ARRAY['telecom', 'agencia_noticias', 'ti', 'serv_audiovisuais', 'ed_e_ed_integradas_a_impressao']);