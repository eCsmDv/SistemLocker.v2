class Locker:
    def __init__(self, numero, tamanho, ocupado=False, codigo=None, apartamento_destino=None):
        self.numero = numero
        self.tamanho = tamanho
        self.ocupado = ocupado
        self.codigo = codigo
        self.apartamento_destino = apartamento_destino

    def ocupar(self, codigo, apartamento):
        self.ocupado = True
        self.codigo = codigo
        self.apartamento_destino = apartamento

    def liberar(self):
        self.ocupado = False
        self.codigo = None
        self.apartamento_destino = None