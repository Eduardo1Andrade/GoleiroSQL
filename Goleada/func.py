
import psycopg
import sys

conexao = psycopg.connect(
    host="localhost",
    port=5432,
    dbname="campeonato",
    user="postgres",
    password="9191",
)
cursor = conexao.cursor()


def login():
    nome = input("digite o nome do login: ")
    senha = input("digite a senha: ")

    cursor.execute(
        "SELECT * FROM login WHERE nome = %s AND senha = %s",
        (nome, senha)
    )

    if cursor.fetchone():
        print("login aceito!!!")
    else:
        print("login não aceito")
        sys.exit()

def verificar_clube_existe (clube_id): # função que verifica se tem nome 
    # returna true ou false
    cursor.execute(
        "SELECT EXISTS (SELECT 1 FROM clube WHERE clube_id = %s);",
            (clube_id,)
            )

def verificar_nome_igual(nome, tipo): # função que verifica se tem nome repetido
    # retorna true ou false
    if tipo == 1:
        cursor.execute(
            "SELECT EXISTS (SELECT 1 FROM jogador WHERE nome = %s);",
            (nome,)
            )
        return cursor.fetchone()[0]

    elif tipo == 2:
        cursor.execute(
            "SELECT EXISTS (SELECT 1 FROM clube WHERE nome = %s);",
            (nome,)
            )
        return cursor.fetchone()
def criar_dados():
    decisao = input(
        "o que deseja criar?\n"
        "[1] jogador\n"
        "[2] clube\n"
        "opção: "
    )

    if decisao == "1":
        novo_nome = input("digite o nome do jogador: ")
        camisa_jogador = int(input("digite o numero da camisa do jogador: "))
        clube_id = int(input("digite o id do clube: "))

        nome_igual = verificar_nome_igual(novo_nome,1)
        print(nome_igual)
        if nome_igual == True: # verifica se o nome é repetido
            print("não pode colocar nome que ja existe")
            return

        clube_existe = verificar_clube_existe(clube_id)

        if clube_existe == False: # se não existe atribuir o id de "sem clube"
            clube_id = cursor.execute(
                "SELECT clube_id FROM clube WHERE nome = 'sem clube'"
            )

        cursor.execute(
            "INSERT INTO jogador (nome, numero_camisa, fk_clube_id) "
            "VALUES (%s, %s, %s)",
            (novo_nome, camisa_jogador, clube_id)
        )

    elif decisao == "2":
        novo_nome = input("digite o nome do clube: ")
        vitorias = int(input("digite o numero de vitorias do clube: "))
        nome_igual = nome_igual(novo_nome,2)

        if nome_igual == True:
            print("não pode colocar nome que ja existe")
            return

        cursor.execute(
            "INSERT INTO clube (nome, vitorias) VALUES (%s, %s)",
            (novo_nome, vitorias)
        )
        print("clube não indentitificado, por padrão será usado (sem clube)")
        
    else:
        print("opção inválida.")
        return

    conexao.commit()
    print("processando.....")
    print("feito")


def apagar_dados():
    decisao = input(
        "o que deseja apagar?\n"
        "[1] jogador\n"
        "[2] clube\n"
        "opção: "
    )

    if decisao == "1":
        nome = input("digite o nome do jogador: ")

        cursor.execute(
            "DELETE FROM jogador WHERE nome ILIKE %s",
            (f"%{nome}%",)
        )

        conexao.commit()
        print("jogador apagado com sucesso!")

    elif decisao == "2":
        print("apagar um clube vai mover todos os jogadores seram movidos para (sem clube!)")
        nome = input("digite o nome do clube: ")

        cursor.execute(
            "SELECT clube_id FROM clube WHERE nome ILIKE %s",
            (f"%{nome}%",)
        )

        resultados = cursor.fetchall()

        if not resultados:
            print("clube não encontrado.")
            return

        if len(resultados) > 1:
            print("mais de um clube encontrado. seja mais específico.")
            return

        clube_id = resultados[0][0]

        cursor.execute(
            "UPDATE jogador SET fk_clube_id = (SELECT clube_id FROM clube WHERE nome = 'sem clube') WHERE fk_clube_id = %s",
            (clube_id,)
        )

        cursor.execute(
            "DELETE FROM clube WHERE clube_id = %s",
            (clube_id,)
        )

        conexao.commit()
        print("clube e jogadores apagados com sucesso!")

    else:
        print("opção inválida.")


def listar_dados():
    decisao = input(
        "o que deseja pesquisar?\n"
        "[1] jogador\n"
        "[2] clube\n"
        "[3] tudo (jogadores e clubes)\n"
        "opção: "
    )

    if decisao == "1":
        decisao_2 = input(
            "pesquisar jogador por:\n"
            "[1] nome\n"
            "[2] numero da camisa\n"
            "opção: "
        )

        if decisao_2 == "1":
            nome = input("digite o nome do jogador: ")

            cursor.execute(
                "SELECT nome, numero_camisa FROM jogador WHERE nome ILIKE %s",
                (f"%{nome}%",)
            )

        elif decisao_2 == "2":
            numero_camisa = int(input("digite o numero da camisa: "))

            cursor.execute(
                "SELECT nome, numero_camisa FROM jogador "
                "WHERE numero_camisa = %s",
                (numero_camisa,)
            )

        else:
            print("opção inválida.")
            return

        resultado = cursor.fetchall()

        for jogador, numero_camisa in resultado:
            print(f"jogador: {jogador} | numero da camisa: {numero_camisa}")

    elif decisao == "2":
        decisao_2 = input(
            "pesquisar clube por:\n"
            "[1] nome\n"
            "[2] vitorias\n"
            "opção: "
        )

        if decisao_2 == "1":
            nome = input("digite o nome do clube: ")

            cursor.execute(
                "SELECT nome, vitorias FROM clube WHERE nome ILIKE %s",
                (f"%{nome}%",)
            )

        elif decisao_2 == "2":
            vitorias = int(input("digite o numero de vitorias: "))

            cursor.execute(
                "SELECT nome, vitorias FROM clube WHERE vitorias = %s",
                (vitorias,)
            )

        else:
            print("opção inválida.")
            return

        resultado = cursor.fetchall()

        for clube, vitorias in resultado:
            print(f"clube: {clube} | vitorias: {vitorias}")

    elif decisao == "3":
        cursor.execute(
            "SELECT jogador.nome, clube.nome "
            "FROM jogador "
            "FULL OUTER JOIN clube "
            "ON jogador.fk_clube_id = clube.clube_id"
        )

        resultado = cursor.fetchall()

        for jogador, clube in resultado:
            print(f"jogador: {jogador} | clube: {clube}")

    else:
        print("opção inválida.")


def atualizar_dados():
    decisao = input(
        "o que deseja atualizar?\n"
        "[1] jogador\n"
        "[2] clube\n"
        "opção: "
    )

    if decisao == "1":
        nome = input("digite o nome atual do jogador: ")

        cursor.execute(
            "SELECT jogador_id FROM jogador WHERE nome ILIKE %s",
            (f"%{nome}%",)
        )

        resultado = cursor.fetchall()

        if not resultado:
            print("jogador não encontrado.")
            return

        if len(resultado) > 1:
            print("mais de um jogador encontrado. seja mais específico.")
            return

        jogador_id = resultado[0][0]

        decisao = input(
            "o que deseja atualizar?\n"
            "[1] nome\n"
            "[2] numero da camisa\n"
            "[3] clube\n"
            "opção: "
        )

        if decisao == "1":
            novo_nome = input("digite o novo nome: ")

            cursor.execute(
                "UPDATE jogador SET nome = %s WHERE jogador_id = %s",
                (novo_nome, jogador_id)
            )

        elif decisao == "2":
            nova_camisa = int(input("digite o novo numero da camisa: "))

            cursor.execute(
                "UPDATE jogador SET numero_camisa = %s "
                "WHERE jogador_id = %s",
                (nova_camisa, jogador_id)
            )

        elif decisao == "3":
            clube_id = int(input("digite o novo id do clube: "))

            cursor.execute(
                "UPDATE jogador SET fk_clube_id = %s "
                "WHERE jogador_id = %s",
                (clube_id, jogador_id)
            )

        else:
            print("opção inválida.")
            return

        conexao.commit()
        print("dados do jogador atualizados com sucesso!")

    elif decisao == "2":
        nome = input("digite o nome atual do clube: ")

        cursor.execute(
            "SELECT clube_id FROM clube WHERE nome ILIKE %s",
            (f"%{nome}%",)
        )

        resultado = cursor.fetchall()

        if not resultado:
            print("clube não encontrado.")
            return

        if len(resultado) > 1:
            print("mais de um clube encontrado. seja mais específico.")
            return

        clube_id = resultado[0][0]

        decisao = input(
            "o que deseja atualizar?\n"
            "[1] nome\n"
            "[2] vitorias\n"
            "opção: "
        )

        if decisao == "1":
            novo_nome = input("digite o novo nome do clube: ")

            cursor.execute(
                "UPDATE clube SET nome = %s WHERE clube_id = %s",
                (novo_nome, clube_id)
            )

        elif decisao == "2":
            vitorias = int(input("digite o novo numero de vitorias: "))

            cursor.execute(
                "UPDATE clube SET vitorias = %s WHERE clube_id = %s",
                (vitorias, clube_id)
            )

        else:
            print("opção inválida.")
            return

        conexao.commit()
        print("dados do clube atualizados com sucesso!")

    else:
        print("opção inválida.")

