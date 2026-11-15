--criação de tabelas

CREATE TABLE clube (
	clube_id SERIAL PRIMARY KEY, 
	nome VARCHAR(200) NOT NULL UNIQUE,
	vitorias INTEGER NOT NULL
);

CREATE TABLE jogador (
	jogador_id SERIAL PRIMARY KEY, 
	nome VARCHAR(200) NOT NULL UNIQUE,
	numero_camisa INTEGER NOT NULL,
	fk_clube_id INTEGER REFERENCES clube(clube_id)
);

CREATE TABLE login(
	nome VARCHAR(200) NOT NULL,
	senha VARCHAR(20) NOT NULL
);

-- informações de login
INSERT INTO login (nome,senha) VALUES ('root', '1234')
INSERT INTO clube (nome,vitorias) VALUES ('Vasco', 0)
INSERT INTO jogador (nome, numero_camisa,fk_clube_id) VALUES ('ana', 10, 1)



-- o Resto foi somente para teste proprio não é necessario usar
-- apagar coluna
DROP TABLE jogador
DROP TABLE clube
DROP TABLE login

--SELECIONAR TUDO
SELECT * FROM jogador
SELECT * FROM clube


-- correçãoc
SELECT * FROM clube WHERE nome ILIKE '%Vas%' 

--clube vazio
INSERT INTO clube (nome,vitorias) VALUES ('sem clube', 0)

--teste
SELECT EXISTS (SELECT 1 FROM jogador WHERE nome = 'ana');