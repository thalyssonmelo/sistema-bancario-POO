from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime
class Conta():
    def __init__(self, numero, cliente,) -> None:
        self._saldo = 0
        self._numero = numero 
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
    
    @property
    def saldo(self):
        return self._saldo   
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = saldo < valor

        if excedeu_saldo:
            print("\n=== Operação falhou! Você não tem saldo suficiente. ===")

        elif valor > 0:
            print("\n=== Saque realizado com sucesso! ===")
            return True
        
        else:
            print("\n=== Operação falhou! O valor informado é inválido. ===")

        return False

    def depositar(self, valor):
        if valor>0:
            self.saldo -= valor
            print("\n=== Depósito realizado com sucesso! ===")
            return True
        else:
            print("\n=== Operação falhou! O valor informado é inválido. ===")

        return False

class Cliente():
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)    

class PessoaFisica(Cliente):
    def __init__(cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

class ContaCorrente(Conta):
    def __init__(self, numero, cliente):
        super().__init__(numero, cliente)
        self.limite = 500
        self.limite_saques = 3

    def sacar(self, valor):
        numero_saques = len([trasacao for transacao in self.historico.transacoes if transacao["tipo"] == "Saque"])

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("\n=== Operação falhou! O valor do saque excedeu o limite. ===")

        elif excedeu_saques:
            print("=== Operação falhou! Número máximo de saques excedido. ===")    

        else:
            return super().sacar(valor)    
        
        return False
    
    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C\C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
            """

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime
                ("%d-%m-%Y %H:%M:%s"),
            }
        )

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass        

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

        
