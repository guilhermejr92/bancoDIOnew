# bank_operations.py

import datetime


def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        data_hora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        extrato += f"{data_hora}\tDepósito:\tR$ {valor:.2f}\n"
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

    elif excedeu_limite:
        print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

    elif excedeu_saques:
        print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

    elif valor > 0:
        saldo -= valor
        data_hora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        extrato += f"{data_hora}\tSaque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print("\n=== Saque realizado com sucesso! ===")

    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    return saldo, extrato


def exibir_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")

    if not extrato:
        print("Não foram realizadas movimentações.")
    else:
        print("{:<20} {:<15} {:<10}".format(
            "Data/Hora", "Movimentação", "Valor"))
        print("-" * 45)

        saldo_atual = 0
        for movimentacao in extrato.split("\n"):
            if movimentacao:
                # Adicionar esta linha para debug
                print("Movimentação:", movimentacao)
                partes = movimentacao.split("\t")
                if len(partes) >= 3:
                    data_hora = partes[0]
                    tipo_movimentacao = partes[1]
                    valor_str = partes[2]
                    if valor_str:  # Verificar se valor_str não está vazio
                        valor = float(valor_str.replace("R$ ", ""))
                        saldo_atual += valor
                        print("{:<20} {:<15} {:<10}".format(
                            data_hora, tipo_movimentacao, valor_str))
                    else:
                        print("Erro: Valor inválido")
                else:
                    print("Erro: Formato de movimentação inválido")


def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [
        usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

    print("=" * 45)
