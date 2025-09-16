from datetime import datetime

def menu():
    """Exibe o menu de opções para o usuário."""
    menu_texto = """
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(menu_texto)

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    """
    Realiza a operação de saque.
    Argumentos devem ser passados apenas por nome (keyword-only).
    """
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
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        extrato += f"[{timestamp}] Saque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print("\n=== Saque realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    return saldo, extrato, numero_saques

def depositar(saldo, valor, extrato, /):
    """
    Realiza a operação de depósito.
    Argumentos devem ser passados apenas por posição (position-only).
    """
    if valor > 0:
        saldo += valor
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        extrato += f"[{timestamp}] Depósito:\tR$ {valor:.2f}\n"
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
    
    return saldo, extrato

def exibir_extrato(saldo, /, *, extrato):
    """
    Exibe o extrato da conta.
    'saldo' é posicional e 'extrato' é keyword-only.
    """
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("==========================================")

def cadastrar_usuario(usuarios):
    """Cadastra um novo usuário (cliente) no sistema."""
    cpf = input("Informe o CPF (somente número): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    usuarios.append({"nome": nome, "cpf": cpf})

    print("=== Usuário criado com sucesso! ===")

def filtrar_usuario(cpf, usuarios):
    """Busca um usuário na lista de usuários pelo CPF."""
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def cadastrar_conta(agencia, numero_conta, usuarios, contas):
    """Cria uma nova conta bancária associada a um usuário."""
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        conta = {
            "agencia": agencia,
            "numero_conta": numero_conta,
            "usuario": usuario,
            "saldo": 0,
            "limite": 500,
            "extrato": "",
            "numero_saques": 0,
            "limite_saques": 3,
        }
        contas.append(conta)
        print("\n=== Conta criada com sucesso! ===")
    else:
        print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")

def listar_contas(contas):
    """Exibe uma lista de todas as contas cadastradas."""
    if not contas:
        print("\n@@@ Nenhuma conta cadastrada. @@@")
        return

    print("\n================ LISTA DE CONTAS ================")
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print(textwrap.dedent(linha))
    print("================================================")


def main():
    """Função principal que executa o sistema bancário."""
    AGENCIA = "0001"
    
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            numero_conta = int(input("Informe o número da conta para depósito: "))
            conta_encontrada = next((c for c in contas if c['numero_conta'] == numero_conta), None)
            
            if conta_encontrada:
                valor = float(input("Informe o valor do depósito: "))
                novo_saldo, novo_extrato = depositar(
                    conta_encontrada['saldo'], 
                    valor, 
                    conta_encontrada['extrato']
                )
                conta_encontrada['saldo'] = novo_saldo
                conta_encontrada['extrato'] = novo_extrato
            else:
                print("\n@@@ Conta não encontrada! @@@")

        elif opcao == "s":
            numero_conta = int(input("Informe o número da conta para saque: "))
            conta_encontrada = next((c for c in contas if c['numero_conta'] == numero_conta), None)

            if conta_encontrada:
                valor = float(input("Informe o valor do saque: "))
                novo_saldo, novo_extrato, novo_num_saques = sacar(
                    saldo=conta_encontrada['saldo'],
                    valor=valor,
                    extrato=conta_encontrada['extrato'],
                    limite=conta_encontrada['limite'],
                    numero_saques=conta_encontrada['numero_saques'],
                    limite_saques=conta_encontrada['limite_saques'],
                )
                conta_encontrada['saldo'] = novo_saldo
                conta_encontrada['extrato'] = novo_extrato
                conta_encontrada['numero_saques'] = novo_num_saques
            else:
                print("\n@@@ Conta não encontrada! @@@")

        elif opcao == "e":
            numero_conta = int(input("Informe o número da conta para exibir o extrato: "))
            conta_encontrada = next((c for c in contas if c['numero_conta'] == numero_conta), None)
            
            if conta_encontrada:
                exibir_extrato(
                    conta_encontrada['saldo'], 
                    extrato=conta_encontrada['extrato']
                )
            else:
                print("\n@@@ Conta não encontrada! @@@")

        elif opcao == "nu":
            cadastrar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            cadastrar_conta(AGENCIA, numero_conta, usuarios, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

if __name__ == "__main__":
    import textwrap
    main()