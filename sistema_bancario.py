import textwrap
from datetime import datetime

def menu():
    menu_texto = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu_texto))


def depositar(conta, valor, /):
    if valor > 0:
        conta['saldo'] += valor
        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        conta['extrato'] += f"[{timestamp}] Depósito:\tR$ {valor:.2f}\n"
        print("\n=== Depósito realizado com sucesso! ===")
        return True
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
        return False

def sacar(*, conta, valor):
    saldo = conta['saldo']
    limite = conta['limite']
    numero_saques = conta['numero_saques']
    limite_saques = conta['limite_saques']

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
        conta['saldo'] -= valor
        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        conta['extrato'] += f"[{timestamp}] Saque:\t\tR$ {valor:.2f}\n"
        conta['numero_saques'] += 1
        print("\n=== Saque realizado com sucesso! ===")
        return True
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
    
    return False

def exibir_extrato(conta, /):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not conta['extrato'] else conta['extrato'])
    print(f"\nSaldo:\t\tR$ {conta['saldo']:.2f}")
    print("==========================================")


def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ").strip().replace(".", "").replace("-", "")
    if filtrar_usuario(cpf, usuarios):
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print("\n=== Usuário criado com sucesso! ===")

def filtrar_usuario(cpf, usuarios):
    return next((usuario for usuario in usuarios if usuario["cpf"] == cpf), None)

def criar_conta(agencia, numero_conta, usuarios, contas):
    cpf = input("Informe o CPF do usuário para vincular a conta: ").strip().replace(".", "").replace("-", "")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        # Cria a conta com seu próprio estado (saldo, extrato, etc.)
        nova_conta = {
            "agencia": agencia,
            "numero_conta": numero_conta,
            "usuario": usuario,
            "saldo": 0,
            "limite": 500,
            "extrato": "",
            "numero_saques": 0,
            "limite_saques": 3
        }
        contas.append(nova_conta)
        print("\n=== Conta criada com sucesso! ===")
    else:
        print("\n@@@ Usuário não encontrado! Não é possível criar a conta. @@@")

def listar_contas(contas):
    if not contas:
        print("\n@@@ Nenhuma conta cadastrada. @@@")
        return

    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("-" * 40)
        print(textwrap.dedent(linha))


def recuperar_conta_cliente(cliente):
    if not cliente['contas']:
        print("\n@@@ Cliente não possui conta cadastrada! @@@")
        return None

    if len(cliente['contas']) == 1:
        return cliente['contas'][0]

    print("\nContas encontradas para este CPF:")
    for i, conta in enumerate(cliente['contas']):
        print(f"  [{i+1}] - Agência: {conta['agencia']}, Conta: {conta['numero_conta']}")
    
    try:
        escolha = int(input("Digite o número da conta que deseja usar: "))
        if 1 <= escolha <= len(cliente['contas']):
            return cliente['contas'][escolha - 1]
        else:
            print("\n@@@ Opção inválida! @@@")
            return None
    except ValueError:
        print("\n@@@ Entrada inválida! Por favor, digite um número. @@@")
        return None

def obter_valor_monetario(mensagem):
    while True:
        try:
            return float(input(mensagem))
        except ValueError:
            print("\n@@@ Valor inválido! Por favor, digite um número (ex: 50.50). @@@")


def main():
    AGENCIA = "0001"
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(AGENCIA, numero_conta, usuarios, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao in ("d", "s", "e"):
            if not usuarios:
                print("\n@@@ Cadastre um usuário antes de realizar operações. @@@")
                continue

            cpf = input("Informe o CPF do titular da conta: ").strip().replace(".", "").replace("-", "")
            usuario = filtrar_usuario(cpf, usuarios)

            if not usuario:
                print("\n@@@ Usuário não encontrado! @@@")
                continue

            usuario['contas'] = [conta for conta in contas if conta['usuario']['cpf'] == cpf]
            conta_selecionada = recuperar_conta_cliente(usuario)

            if not conta_selecionada:
                continue

            if opcao == "d":
                valor = obter_valor_monetario("Informe o valor do depósito: ")
                depositar(conta_selecionada, valor)
            elif opcao == "s":
                valor = obter_valor_monetario("Informe o valor do saque: ")
                sacar(conta=conta_selecionada, valor=valor)
            elif opcao == "e":
                exibir_extrato(conta_selecionada)
        
        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


if __name__ == "__main__":
    main()