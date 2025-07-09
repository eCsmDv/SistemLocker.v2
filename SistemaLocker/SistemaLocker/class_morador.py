class Morador:
    def __init__(self, nome, apartamento, senha):
        self.nome = nome
        self.apartamento = apartamento
        self.senha = senha

    def alterar_dados(self, novo_nome, nova_senha):
        self.nome = novo_nome
        self.senha = nova_senha