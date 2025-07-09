import json
import random
from class_morador import Morador
from class_locker import Locker
import datetime

class SistemaLocker:
    def __init__(self):
        self.moradores = self.carregar_moradores()
        self.config = self.carregar_configuracoes()
        self.lockers = self.carregar_lockers()

    def carregar_moradores(self):
        with open("data/moradores.json", "r") as f:
            return [Morador(**m) for m in json.load(f)]

    def salvar_moradores(self):
        with open("data/moradores.json", "w") as f:
            json.dump([m.__dict__ for m in self.moradores], f, indent=4)

    def carregar_configuracoes(self):
        with open("data/configuracoes.json", "r") as f:
            return json.load(f)

    def salvar_configuracoes(self):
        with open("data/configuracoes.json", "w") as f:
            json.dump(self.config, f, indent=4)

    def carregar_lockers(self):
        try:
            with open("data/lockers.json", "r") as f:
                dados = json.load(f)
                return [Locker(**d) for d in dados]
        except FileNotFoundError:
            return self.criar_lockers()

    def salvar_lockers(self):
        with open("data/lockers.json", "w") as f:
            json.dump([l.__dict__ for l in self.lockers], f, indent=4)

    def criar_lockers(self):
        lockers = []
        index = 1
        for tam, qtd in self.config["lockers"].items():
            for _ in range(qtd):
                lockers.append(Locker(numero=index, tamanho=tam))
                index += 1
        self.lockers = lockers
        self.salvar_lockers()
        return lockers

    def encontrar_locker_disponivel(self, tamanho):
        for locker in self.lockers:
            if locker.tamanho == tamanho and not locker.ocupado:
                return locker
        return None

    def entregar_encomenda(self, tamanho, apartamento):
        locker = self.encontrar_locker_disponivel(tamanho)
        if not locker:
            return None, "Não há locker disponível desse tamanho."
        codigo = str(random.randint(1000, 9999))
        locker.ocupar(codigo, apartamento)
        self.salvar_lockers()
        self.salvar_entrega(locker.numero, codigo, apartamento)
        return locker.numero, codigo

    def retirar_encomenda(self, numero, codigo):
        for locker in self.lockers:
            if locker.numero == numero and locker.codigo == codigo:
                locker.liberar()
                self.salvar_lockers()
                return True
        return False

    def cadastrar_morador(self, nome, ap, senha):
        self.moradores.append(Morador(nome, ap, senha))
        self.salvar_moradores()

    def excluir_morador(self, apartamento):
        self.moradores = [m for m in self.moradores if m.apartamento != apartamento]
        self.salvar_moradores()

    def salvar_entrega(self, locker_num, codigo, apartamento):
        try:
            with open("data/entregas.json", "r") as f:
                entregas = json.load(f)
        except FileNotFoundError:
            entregas = []
        entregas.append({
            "locker": locker_num,
            "codigo": codigo,
            "apartamento": apartamento,
            "data": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        with open("data/entregas.json", "w") as f:
            json.dump(entregas, f, indent=4)