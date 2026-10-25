
import func
import sys


def main():
    print("programa sobre jogadores e times de futebol")

    decisao = ""

    while decisao != "5":
        decisao = input(
            "\ndigite sua operação:\n"
            "[1] criar dados\n"
            "[2] excluir dados\n"
            "[3] atualizar dados\n"
            "[4] listar dados\n"
            "[5] sair\n"
            "opção: "
        )

        if decisao == "1":
            func.criar_dados()

        elif decisao == "2":
            func.apagar_dados()

        elif decisao == "3":
            func.atualizar_dados()

        elif decisao == "4":
            func.listar_dados()

        elif decisao == "5":
            print("encerrando o programa...")
            return

        else:
            print("opção inválida!!")


func.login()
main()
