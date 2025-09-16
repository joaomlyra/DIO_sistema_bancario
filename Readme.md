# Sistema Bancário Simples em Python

Um projeto desenvolvido em Python que simula as operações básicas de um sistema bancário. O código foi estruturado de forma modular e funcional para garantir maior organização, legibilidade e manutenibilidade.

## Funcionalidades

O sistema oferece as seguintes operações:

* **Depositar:** Permite ao usuário depositar valores positivos em uma conta específica.
* **Sacar:** Permite realizar saques de uma conta, respeitando as seguintes regras:
    * Limite de 3 saques diários.
    * Valor máximo de R$ 500,00 por saque.
    * O saldo em conta deve ser suficiente para a transação.
* **Extrato:** Exibe todas as transações realizadas na conta (depósitos e saques) com a data e hora de cada operação, além do saldo atual.
* **Cadastrar Usuário:** Permite a criação de novos usuários (clientes) no sistema. O CPF é único e o sistema impede o cadastro de usuários duplicados.
* **Cadastrar Conta Bancária:** Cria uma nova conta corrente associada a um usuário já existente. As contas possuem uma agência fixa ("0001") e um número sequencial único.
* **Listar Contas:** Exibe uma lista com todas as contas bancárias cadastradas no sistema, mostrando a agência, o número da conta e o nome do titular.