
import func
import sys
import streamlit as st
import pandas as pd


st.title("Programa Gerenciamento de jogadores e times de futebol V2.0")

def main():
 
    if "tela" not in st.session_state:
        st.session_state.tela = "inicial"
    
    if st.session_state.tela == "inicial":

        # controle de seção
        if st.button("Criar Dados"):
            st.session_state.tela = "criar_dados"
         

        elif st.button("apagar Dados"):
            st.session_state.tela = "apagar_dados"
       

        elif st.button("Atualizar Dados"):
            st.session_state.tela = "atualizar_dados"
    

        elif st.button("Listar Dados"):
            st.session_state.tela = "listar_dados"
          

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



resposta = func.login()
if resposta == True:
    main()