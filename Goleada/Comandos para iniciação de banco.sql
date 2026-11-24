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

ALTER TABLE jogador ADD COLUMN gols INTEGER;

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



--inserts
INSERT INTO jogador (nome, numero_camisa, fk_clube_id) VALUES
('Vinicius Junior', 7, 14),
('Jude Bellingham', 5, 14),
('Lamine Yamal', 19, 13),
('Pedri', 8, 13),
('Erling Haaland', 9, 13),
('Phil Foden', 47, 13),
('Mohamed Salah', 11, 14),
('Virgil van Dijk', 4, 14),
('Harry Kane', 9, 15),
('Jamal Musiala', 10, 15),
('Ousmane Dembele', 10, 16),
('Marquinhos', 5, 16),
('Bukayo Saka', 7, 17),
('Martin Odegaard', 8, 17),
('Cole Palmer', 20, 12),
('Enzo Fernandez', 8, 12),
('Dusan Vlahovic', 9, 11),
('Kenan Yildiz', 10, 17),
('Rafael Leao', 10, 10),
('Christian Pulisic', 11, 10);

INSERT INTO clube (nome, vitorias) VALUES
('Real Madrid', 25),
('Barcelona', 22),
('Manchester City', 28),
('Liverpool', 20),
('Bayern de Munique', 24),
('PSG', 18),
('Arsenal', 19),
('Chelsea', 15),
('Juventus', 17),
('Milan', 14);

-- buscas
-- clube com mais vitorias
SELECT nome,MAX(vitorias) FROM clube 
GROUP BY nome LIMIT 1;
-- clube com menos vitorias
SELECT nome, MIN(vitorias) FROM clube
GROUP BY nome LIMIT 1;
-- media de vitorias por clube
SELECT CAST(AVG(vitorias) AS DECIMAL(10,2)) FROM clube;
-- 5 melhores clubes por vitorias
SELECT nome,vitorias FROM clube 
ORDER BY vitorias DESC LIMIT 5;
-- 5 clubes com mais jogadores
SELECT nome FROM clube 
WHERE clube_id = (SELECT fk_clube_id FROM jogador);