import json
import textwrap
import datetime


def menu(contas):
    menu_str = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu_str))


def validar_valor(mensagem):
    while True:
        try:
            valor = float(input(mensagem))
            if valor < 0:
                print("O valor inserido deve ser positivo.")
            else:
                return valor
        except ValueError:
            print("Por favor, insira um número válido.")


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
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("==========================================")


def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente número): ")
    usuario_existente = filtrar_usuario(cpf, usuarios)

    if usuario_existente:
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return None

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input(
        "Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    novo_usuario = {
        "cpf": cpf,
        "nome": nome,
        "data_nascimento": data_nascimento,
        "endereco": endereco
    }

    usuarios.append(novo_usuario)
    print("=== Usuário criado com sucesso! ===")
    return novo_usuario


def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [
        usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_conta(agencia, numero_conta, usuarios, contas):
    usuario = criar_usuario(usuarios)

    if usuario:
        nova_conta = {
            "agencia": agencia,
            "numero_conta": numero_conta,
            "usuario": usuario,
            "saldo": 0,
            "extrato": ""
        }
        contas.append(nova_conta)  # Adicione a nova conta à lista de contas
        salvar_contas(contas)  # Salvar as contas no arquivo contas.json
        return nova_conta
    else:
        return None


def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))


# Função para carregar as contas do arquivo JSON
def carregar_contas():
    try:
        with open('contas.json', 'r') as file:
            contas = json.load(file)
    except FileNotFoundError:
        contas = []
    return contas


# Função para salvar as contas no arquivo JSON
def salvar_contas(contas):
    with open('contas.json', 'w') as file:
        json.dump(contas, file, indent=4)


def escolher_conta(contas):
    print("\n### Escolha a conta ###")
    for i, conta in enumerate(contas):
        print(f"{i + 1}: {conta['agencia']} - {conta['numero_conta']}")

    while True:
        try:
            escolha = int(input("Escolha o número da conta: "))
            if 1 <= escolha <= len(contas):
                return contas[escolha - 1]
            else:
                print("Número de conta inválido, por favor tente novamente.")
        except ValueError:
            print("Por favor, insira um número válido.")


def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = carregar_contas()  # Carregar as contas salvas

    while True:
        opcao = menu(contas)

        if opcao == "d":
            conta = escolher_conta(contas)
            if conta:
                valor = validar_valor("Informe o valor do depósito: ")
                saldo, extrato = depositar(
                    conta['saldo'], valor, conta['extrato'])
                conta['saldo'] = saldo
                conta['extrato'] = extrato
                salvar_contas(contas)  # Salvar as contas após o depósito

        elif opcao == "s":
            valor = validar_valor("Informe o valor do saque: ")
            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "e":
            conta = escolher_conta(contas)
            if conta:
                exibir_extrato(conta['saldo'], extrato=conta['extrato'])

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(
                AGENCIA, numero_conta, usuarios, contas)

            if conta:
                contas.append(conta)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


if __name__ == "__main__":
    main()
