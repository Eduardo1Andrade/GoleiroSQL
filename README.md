
## Sistema
contem 3 tabelas:
 - 1 jogador: com atributos: id_jogador, nome , numero_camisa e fk_clube_id
 - 2 clube: clube_id, nome, vitorias

CRUD basico com algumas verificações porem pode dar erro ao digitar numeros em vez de letras nos campos onde peça algum numero tirando a navegação por menu.

## Tecnologias:
- docker para rodar containar postgres
- python com lib- psycopg
- postgres
- pg admin

## instrução 
	roda em qualquer lugar que tenha python 3.12+ instalado:
    rode um banco postgres com as expecificações de func.py linha 5
    coloque a primeira facha de comandos do arquivo em .sql
    No Windows: python -m venv venv e depois .\venv\Scripts\activate
    No Mac/Linux: python3 -m venv venv e depois source venv/bin/activate
    use o terminal para navegar na pasta do projeto usando "cd /pastas/local_do_projeto/"
    rode "python main.py"

## usuario de teste = root , senha = 1234
