
import psycopg
import streamlit as st
import pandas as pd
import plotly.express as pl

conexao = psycopg.connect(
    host="localhost",
    port=5432,
    dbname="campeonato",
    user="postgres",
    password="9191",
)
cursor = conexao.cursor()

def login():
    
    if "sign_in" not in st.session_state:
        st.session_state.sign_in = False

    if not st.session_state.sign_in:
        usuario = st.text_input("digite o nome do login: ")
        senha = st.text_input("digite a senha: ",type="password")

        if st.button("Entrar"):
            cursor.execute(
                "SELECT * FROM login WHERE nome = %s AND senha = %s",
                (usuario, senha)
            )

            if cursor.fetchone():
                st.session_state.sign_in = True
                st.success("Login Feito com Sucesso!!")
                st.rerun()
                
            else:
                st.error("login não aceito")
    else:
        return True
       
def verificar_clube_existe (clube_id): # função que verifica se tem nome 
    # returna true ou false
    cursor.execute(
        "SELECT EXISTS (SELECT 1 FROM clube WHERE clube_id = %s);",
            (clube_id,)
            )
    return cursor.fetchone()[0]

def verificar_jogador_existe(nome_jogador): # função que verifica se tem nome 
    # returna true ou false
    cursor.execute(
        "SELECT EXISTS (SELECT 1 FROM jogador WHERE nome = %s);",
            (nome_jogador,)
            )
    return cursor.fetchone()[0]

def verificar_nome_igual(nome, tipo): # função que verifica se tem nome repetido
    # retorna true ou false
    if tipo == "1":
        cursor.execute(
            "SELECT EXISTS (SELECT * FROM jogador WHERE nome = %s);",
            (nome,)
            )
        return cursor.fetchone()[0]

    elif tipo == "2":
        cursor.execute(
            "SELECT EXISTS (SELECT * FROM clube WHERE nome = %s);",
            (nome,)
            )
        return cursor.fetchone()[0]


def verificar_dados(dado,tipo): #vefica se dados digitados são validos dos dados digitados e 
    #transforma dado em int quando tipo == 2 
    #retorna um texto de aviso

    if not dado:
        st.error("Preencha todos os campos")
        return False

    if tipo == "2" and not verificar_tipo_int(dado):
        st.error("Digite um número válido")
        return False

    return True


def verificar_resultado_existe(resultados,tipo):
    if tipo == "1":
        if not resultados:
            st.error("nenhum resultado encontrado")
            return False

    if tipo == "2":
        if not resultados:
            st.error("nenhum resultado encontrado")
            return False
        if len(resultados) > 1:
            st.error("mais de um resultado encontrado seja mais especifico")
            return False
        
    return True

def verificar_tipo_int(dado): # verifica se dado é int
    try:
        int(dado)
    except ValueError:
        return False
    else:
        return True
def criar_dados():
    decisao = st.selectbox(
        "o que deseja criar?",
        ["jogador","clube"]
    )

    if decisao == "jogador":

        novo_nome = st.text_input("digite o nome do jogador: ")
        camisa_jogador = st.text_input("digite o numero da camisa do jogador: ")
        clube_id = st.text_input("digite o id do clube: ")
        gol = st.text_input("digite o numero de gols desse jogador")

        if st.button("Cadastrar"):

            # verificações
            if not novo_nome or not camisa_jogador or not clube_id or not gol:
                st.error("Preencha todos os campos")
                return

            elif verificar_tipo_int(camisa_jogador) == False or verificar_tipo_int(clube_id) == False or verificar_tipo_int(gol) == False: 
                st.error("por favor digite dado numerico valido em camisa de jogador ou id clube")
                return 

            gol = int(gol)
            clube_id = int(clube_id)
            camisa_jogador = int(camisa_jogador)

            if verificar_nome_igual(novo_nome,"1"): # verifica se o nome é repetido
                st.error("não pode colocar nome que ja existe")
                return

            if not verificar_clube_existe(clube_id): # se não existe atribuir o id de "sem clube"
                cursor.execute(
                    "SELECT clube_id FROM clube WHERE nome = 'sem clube'"
                )
                st.warning("clube não indentitificado, por padrão será usado (sem clube)")
                clube_id = cursor.fetchall()[0][0]

            #efetivação
            cursor.execute(
            "INSERT INTO jogador (nome, numero_camisa, fk_clube_id, gols) "
            "VALUES (%s, %s, %s, %s)",
            (novo_nome, camisa_jogador, clube_id,gol)
            )

            conexao.commit()
            st.success("jogador criado com sucesso!!!")
            return

    elif decisao == "clube":
        novo_nome = st.text_input("digite o nome do clube: ")
        vitorias = st.text_input("digite o numero de vitorias do clube: ")

        if st.button("Cadastrar"):

            if not verificar_dados(novo_nome,"1"):
                return
            if not verificar_dados(vitorias,"2"):
                return

            elif verificar_nome_igual(novo_nome,"2") == True: # verificar nome é unico
                st.error("não pode colocar nome que ja existe")
                return
                
            else:
                vitorias = int(vitorias)
                cursor.execute(
                    "INSERT INTO clube (nome, vitorias) VALUES (%s, %s)",
                    (novo_nome, vitorias)
                )        

                conexao.commit()
                st.success("clube criado com sucesso!!")





def apagar_dados():
    decisao = st.selectbox( # selecionar dados
        "o que deseja apagar?",
        ["jogador","clube"]
    )

    if decisao == "jogador":
        nome = st.text_input("digite o nome do jogador: ") #input

        if st.button("Apagar jogador"):

            if not verificar_dados(nome,"1"):
                return
            #verifica se tem jogador
            cursor.execute(
                "SELECT jogador_id FROM jogador WHERE nome ILIKE %s",
                (f"%{nome}%",)
            )
            resultados = cursor.fetchall()

            if not verificar_resultado_existe(resultados,"2"):
                return
            cursor.execute(
                "DELETE FROM jogador WHERE nome ILIKE %s",
                (f"%{nome}%",)
            )

            conexao.commit()
            st.success("jogador apagado com sucesso!")

    elif decisao == "clube":

        st.text("apagar um clube vai mover todos os jogadores seram movidos para (sem clube!)")
        nome = st.text_input("digite o nome do clube: ")

        if st.button("Apagar Clube"):
            #verificações

            if not verificar_dados(nome,"1"):
                return

            cursor.execute(
                '''SELECT clube_id FROM clube WHERE nome = 'sem clube' '''
            )

            sem_clube_id = cursor.fetchall()[0][0]

            cursor.execute(
                "SELECT clube_id FROM clube WHERE nome ILIKE %s",
                (f"%{nome}%",)
            )
        
            resultados = cursor.fetchall()
    
            if not verificar_resultado_existe(resultados,"2"):
                return
            #efetivação
            clube_id = resultados[0][0]
            if clube_id == sem_clube_id:
                st.error("você não pode apagar um clube padrão do sistema!!!")
                return

            cursor.execute( #atualiza todos os jogadores para "sem clube"
                "UPDATE jogador SET fk_clube_id = (SELECT clube_id FROM clube WHERE nome = 'sem clube') WHERE fk_clube_id = %s",
                (clube_id,)
            )

            cursor.execute( # apaga clube
                "DELETE FROM clube WHERE clube_id = %s",
                (clube_id,)
            )

            conexao.commit()
            st.success("clube apagado com sucesso!")
            return


def listar_dados():
    # mostrar tambem gools
    decisao = st.selectbox(
        "o que deseja pesquisar?",
        ["jogador","clube","jogadores e clubes"]
    )
    # escolha jogador
    if decisao == "jogador":
        decisao_2 = st.selectbox(
            "pesquisar jogador por:",
            ["nome","numero da camisa"]
        )
        # filtre por nome
        if decisao_2 == "nome":
            nome = st.text_input("digite o nome do jogador: ")

            #verificações
            if st.button("Buscar"):
                if not verificar_dados(nome,"1"):
                    return
                #busca
                cursor.execute(
                    "SELECT nome, numero_camisa FROM jogador WHERE nome ILIKE %s",
                    (f"%{nome}%",)
                )

                resultado = cursor.fetchall()

                  #veficação
                if not verificar_resultado_existe(resultado,"1"):
                    return

                for jogador, numero_camisa in resultado:
                    st.text(f"jogador: {jogador} | numero da camisa: {numero_camisa}")

        elif decisao_2 == "numero da camisa":
            numero_camisa = st.text_input("digite o numero da camisa: ")

            #vericiações
            if st.button("Buscar"):
                if not verificar_dados(numero_camisa,"2"):
                    return
                numero_camisa = int(numero_camisa)
         
                #busca
                cursor.execute(
                    "SELECT nome, numero_camisa FROM jogador "
                    "WHERE numero_camisa = %s",
                    (numero_camisa,)
                )


                resultado = cursor.fetchall()

                  #veficação
                if not verificar_resultado_existe(resultado,"1"):
                    return

                for jogador, numero_camisa in resultado:
                    st.text(f"jogador: {jogador} | numero da camisa: {numero_camisa}")

    elif decisao == "clube":
        decisao_2 = st.selectbox(
            "pesquisar clube por:",
            ["nome","vitorias"]
        )

        if decisao_2 == "nome":
            nome = st.text_input("digite o nome do clube: ")
            
            if st.button("Buscar"):
                #verificações
                if not verificar_dados(nome,"1"):
                    return
                #busca
                cursor.execute(
                    "SELECT nome, vitorias FROM clube WHERE nome ILIKE %s",
                    (f"%{nome}%",)
                )

                resultado = cursor.fetchall()

                if not verificar_resultado_existe(resultado,"1"):
                    return
        
                for clube, vitorias in resultado:
                    st.text(f"clube: {clube} | vitorias: {vitorias}")

        elif decisao_2 == "vitorias":
            vitorias = st.text_input("digite o numero de vitorias: ")


            if st.button("Buscar"):
                #veficações
                if not verificar_dados(vitorias,"2"):
                    return
                vitorias = int(vitorias)

               

                #busca
                cursor.execute(
                    "SELECT nome, vitorias FROM clube WHERE vitorias = %s",
                    (vitorias,)
                )

                resultado = cursor.fetchall()

                if not verificar_resultado_existe(resultado,"1"):
                    return
        
                for clube, vitorias in resultado:
                    st.text(f"clube: {clube} | vitorias: {vitorias}")

    elif decisao == "jogadores e clubes":

        st.text("exibe um resultado de jogadores e quais clubes pertencem")

        if st.button("Buscar"):

            cursor.execute(
                "SELECT jogador.nome, clube.nome "
                "FROM jogador "
                "FULL OUTER JOIN clube "
                "ON jogador.fk_clube_id = clube.clube_id"
            )

            resultado = cursor.fetchall()

            if not verificar_resultado_existe(resultado,"1"):
                return

            for jogador, clube in resultado:
                st.text(f"jogador: {jogador} | clube: {clube}")



def atualizar_dados():
    decisao = st.selectbox(
        "o que deseja atualizar?",
        ["jogador","clube"]
    )

    if decisao == "jogador":
        nome = st.text_input("digite o nome atual do jogador: ")

        #verificações
        if st.button("Buscar Dado"):
            if not verificar_dados(nome,"1"):
                return
            
            cursor.execute(
                "SELECT jogador_id FROM jogador WHERE nome ILIKE %s",
                (f"%{nome}%",)
            )

            resultado = cursor.fetchall()

            if not verificar_resultado_existe(resultado,"2"):
                st.session_state.jogador_encontrado = False
                return

            st.session_state.jogador_id = resultado[0][0]
            st.session_state.jogador_encontrado = True
            #edição

        decisao = st.selectbox(
            "o que deseja atualizar?",
            ["nome","numero_camisa","clube","gols"]
        )
        #edição de jogador por nome
        if st.session_state.get("jogador_encontrado", False):
            if decisao == "nome":
                novo_nome = st.text_input("digite o novo nome: ")

                #verficações
                if st.button("Atualizar dado"):
                    if not verificar_dados(novo_nome,"1"):
                        return

                    if verificar_nome_igual(novo_nome,"1"):
                        st.error("esse nome ja existe, tente novamente")
                        return
                    #efetivação
                    cursor.execute(
                        "UPDATE jogador SET nome = %s WHERE jogador_id = %s",
                        (novo_nome, st.session_state.jogador_id)
                    )
                #editar por numero de camisa
            elif decisao == "numero_camisa":
                nova_camisa = st.text_input("digite o novo numero da camisa: ")

                #verficiações
                if st.button("Atualizar"):
                    if not verificar_dados(nova_camisa,"2"):
                        return
                    nova_camisa = int(nova_camisa)
                    

                    #efetivação
                    cursor.execute(
                        "UPDATE jogador SET numero_camisa = %s "
                        "WHERE jogador_id = %s",
                        (nova_camisa, st.session_state.jogador_id)
                    )

            elif decisao == "clube":
                clube_id = st.text_input("digite o novo id do clube: ")

                if st.button("Atualizar dado"):
                    #verficiações
                    if not verificar_dados(clube_id,"2"):
                        return
                    clube_id = int(clube_id)

                    if not verificar_clube_existe(clube_id):
                        st.error("clube não existe")
                        return

                    #efetivação
                    cursor.execute(
                        "UPDATE jogador SET fk_clube_id = %s "
                        "WHERE jogador_id = %s",
                        (clube_id, st.session_state.jogador_id)
                    )
            

            elif decisao == "gols":
                gol = st.text_input("digite a nova quantidade de gols: ")


                if st.button("Atualizar dado"):
                    #verficiações
                    if not verificar_dados(gol,"2"):
                        return
                    gol = int(gol)
                
                        
                    #efetivação
                    cursor.execute(
                        "UPDATE jogador SET gols = %s "
                        "WHERE jogador_id = %s",
                        (gol, st.session_state.jogador_id)
                    )



                conexao.commit()
                st.success("dados do jogador atualizados com sucesso!")

    elif decisao == "clube":
        nome = st.text_input("digite o nome atual do clube: ")

        
        if st.button("Buscar Dado"):
            #verficiações
            if not verificar_dados(nome,"1"):
                return

            #efetivação
            cursor.execute(
                "SELECT clube_id FROM clube WHERE nome ILIKE %s",
                (f"%{nome}%",)
            )

            resultado = cursor.fetchall()

            if not verificar_resultado_existe(resultado,"2"):
                st.session_state.clube_encontrado = False
                return

            st.session_state.clube_id = resultado[0][0]
            st.session_state.clube_encontrado = True

        if st.session_state.get("clube_encontrado", False):
            decisao = st.selectbox(
                "o que deseja atualizar?",
                ["nome","vitorias"]
            )

            if decisao == "nome":
                novo_nome = st.text_input("digite o novo nome do clube: ")

                if st.button("Atualizar dado"):
                    #verificações   
                    if not verificar_dados(novo_nome,"1"):
                        return


                    cursor.execute(
                        "UPDATE clube SET nome = %s WHERE clube_id = %s",
                        (novo_nome, st.session_state.clube_id)
                    )

            elif decisao == "vitorias":
                vitorias = st.text_input("digite o novo numero de vitorias: ")

                if st.button("Atualizar dado"):
                    #verificações
                    if not verificar_dados(vitorias,"2"):
                        return
                    vitorias = int(vitorias)

                    cursor.execute(
                        "UPDATE clube SET vitorias = %s WHERE clube_id = %s",
                        (vitorias, st.session_state.clube_id)
                    )

                conexao.commit()
                st.success("dados do clube atualizados com sucesso!")


def dados_estatisticos():
   # mostrar resultado de max, min e media

    cursor.execute(
        "SELECT nome,MAX(vitorias) FROM clube GROUP BY nome LIMIT 1;",
    )
    resultados = cursor.fetchall()
    nome_max = resultados[0][0]
    vitorias_max = resultados[0][1]


    cursor.execute(
        "SELECT nome, MIN(vitorias) FROM clube GROUP BY nome LIMIT 1;",
    )

    resultados = cursor.fetchall()

    nome_min = resultados[0][0]
    vitorias_min = resultados[0][1]



    cursor.execute(
        "SELECT CAST(AVG(vitorias) AS DECIMAL(10,2))  FROM clube;",
    )

    resultados = cursor.fetchall()
    vitorias_avg = resultados[0][0]

    st.text(f"clubes com menor numero de vitorias: nome = {nome_min}, numero de vitorias = {vitorias_min} ")

    st.text(f"media de vitorias = {vitorias_avg} ")

    st.text(f"clubes com maior numero de vitorias: nome = {nome_max}, numero de vitorias = {vitorias_max} ")

    # mostrar os 5 melhores clubes por vitorias

    cursor.execute(
        "SELECT nome,vitorias FROM clube ORDER BY vitorias DESC LIMIT 5;"
    )

    resultados = cursor.fetchall()

    data_frame = pd.DataFrame(
        resultados,
        columns=["Clube", "Vitórias"]
    )


    grafico_barras = pl.bar(
        data_frame,
        x="Clube",
        y="Vitórias",
        title="5 melhores clubes com mais vitórias",
        text="Vitórias"
    )

    st.plotly_chart(grafico_barras, width='stretch')

    #gols por jogador
    cursor.execute( 
    "SELECT nome,gols FROM jogador ORDER BY gols DESC LIMIT 5;"
    )

    resultados = cursor.fetchall()

    data_frame_2 = pd.DataFrame(
        resultados,
        columns=["jogadores", "gols"]
    )

    grafico_pizza = pl.pie (
        data_frame_2,
        names="jogadores",
        values="gols",
        title="melhores jogadores por gols",
        hole=0.3
    )
    

    st.plotly_chart(grafico_pizza, width='stretch')

    # numero de camisa mais usado pelos jogadores.
    cursor.execute(
        '''
    SELECT numero_camisa, COUNT(jogador_id) AS quantidade
    FROM jogador
    GROUP BY numero_camisa
    HAVING COUNT(jogador_id) > 1
    ORDER BY quantidade DESC
    LIMIT 5;'''
    )

    resultados = cursor.fetchall()

    data_frame_3 = pd.DataFrame(
        resultados,
        columns=["numero_camisa","quantidade"]
    )

    grafico_pizza_2 = pl.pie(
        data_frame_3,
        names="numero_camisa",
        values="quantidade",
        title="numero de camisa mais usados pelos jogadores"
    )

    st.plotly_chart(grafico_pizza_2,width='stretch')