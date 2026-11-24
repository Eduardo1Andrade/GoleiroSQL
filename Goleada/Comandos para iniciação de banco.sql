--criação de tabelas

CREATE TABLE clube (
	clube_id SERIAL PRIMARY KEY, 
	nome VARCHAR(200) NOT NULL UNIQUE,
	vitorias INTEGER NOT NULL,
	gols INTEGER NOT NULL
);

CREATE TABLE jogador (
	jogador_id SERIAL PRIMARY KEY, 
	nome VARCHAR(200) NOT NULL UNIQUE,
	numero_camisa INTEGER NOT NULL,
	fk_clube_id INTEGER REFERENCES clube(clube_id)
);

CREATE TABLE login(
	login_id SERIAL PRIMARY KEY,
	nome VARCHAR(200) NOT NULL,
	senha VARCHAR(20) NOT NULL
);

-- informações de login
INSERT INTO login (nome,senha) VALUES ('root', '1234')
INSERT INTO clube (nome,vitorias) VALUES ('Vasco', 0)
INSERT INTO jogador (nome, numero_camisa,fk_clube_id) VALUES ('ana', 10, 1)

--clube vazio
INSERT INTO clube (nome,vitorias) VALUES ('sem clube', 0)


--até aqui é necessario executar para bom funcionamento do sistema


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
INSERT INTO jogador (nome, numero_camisa, fk_clube_id, gols) VALUES
('Vinicius Junior', 7, 14,6),
('Jude Bellingham', 5, 14,4),
('Lamine Yamal', 19, 13,1),
('Pedri', 8, 13,4),
('Erling Haaland', 9, 13,60),
('Phil Foden', 47, 13,40),
('Mohamed Salah', 11, 14,5),
('Virgil van Dijk', 4, 14,10),
('Harry Kane', 9, 15,60),
('Jamal Musiala', 10, 15,14),
('Ousmane Dembele', 10, 16,10),
('Marquinhos', 5, 16,60),
('Bukayo Saka', 7, 17,20),
('Martin Odegaard', 8, 17,23),
('Cole Palmer', 20, 12,43),
('Enzo Fernandez', 8, 12,50),
('Dusan Vlahovic', 9, 11,20),
('Kenan Yildiz', 10, 17,15),
('Rafael Leao', 10, 10,12),
('Christian Pulisic', 11, 10,20);

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
GROUP BY nome LIMIT 1 WHERE gols = (
    SELECT MAX(gols)
    FROM jogador
);;
-- clube com menos vitorias
SELECT nome, MIN(vitorias) FROM clube
GROUP BY nome LIMIT 1;
-- media de vitorias por clube
SELECT CAST(AVG(vitorias) AS DECIMAL(10,2)) FROM clube;
-- 5 melhores clubes por vitorias
SELECT nome,vitorias FROM clube 
ORDER BY vitorias DESC LIMIT 5;
-- 5 jogadores com mais gols
SELECT nome,gols FROM jogador ORDER BY gols DESC LIMIT 5;

--
SELECT numero_camisa, COUNT(jogador_id) AS quantidade
FROM jogador
GROUP BY numero_camisa
HAVING COUNT(jogador_id) > 1 LIMIT 5;