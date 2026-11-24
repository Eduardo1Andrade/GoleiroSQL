
import func
import sys
import streamlit as st
import pandas as pd


st.title("Programa Gerenciamento de jogadores e times de futebol V2.0")

def main():
 
    if "tela" not in st.session_state:
        st.session_state.tela = "inicial"

    if "jogador_id" not in st.session_state:
        st.session_state.jogador_id = 0
    
    if "clube_id" not in st.session_state:
        st.session_state.clube_id = 0
    
    if "jogador_encontrado" not in st.session_state:
        st.session_state.jogador_encontrado = False
           
    if "clube_encontrado" not in st.session_state:
        st.session_state.clube_encontrado = False
    
    if st.session_state.tela == "inicial":

        # controle de seção
        if st.button("Criar Dados"):
            st.session_state.tela = "criar_dados"
         

        elif st.button("Apagar Dados"):
            st.session_state.tela = "apagar_dados"
       

        elif st.button("Atualizar Dados"):
            st.session_state.tela = "atualizar_dados"
    

        elif st.button("Listar Dados"):
            st.session_state.tela = "listar_dados"

        elif st.button("Estatisticas graficas"):
            st.session_state.tela = "estisticas_graficas"

        elif st.button("Sair"):
            st.text("encerrando o programa...")
            return

    # função

    if st.session_state.tela == "criar_dados":
        func.criar_dados()
    

    elif st.session_state.tela == "apagar_dados":
        func.apagar_dados()

    
    if st.session_state.tela == "atualizar_dados":
        func.atualizar_dados()

    if st.session_state.tela == "listar_dados":
        func.listar_dados()

    if st.session_state.tela == "estisticas_graficas":
        func.dados_estatisticos()

    if st.session_state.tela != "inicial":

        if st.button("Voltar ao menu"):
            st.session_state.tela = "inicial"

#func.dados_estatisticos()
resposta = func.login()
if resposta == True:
    main()