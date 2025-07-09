import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext
from class_sistema import SistemaLocker

sistema = SistemaLocker()

def centralizar(janela, largura=600, altura=600):
    janela.update_idletasks()
    w = janela.winfo_screenwidth()
    h = janela.winfo_screenheight()
    x = (w // 2) - (largura // 2)
    y = (h // 2) - (altura // 2)
    janela.geometry(f"{largura}x{altura}+{x}+{y}")

def exibir_historico():
    janela = tk.Toplevel()
    janela.title("Histórico de Entregas")
    centralizar(janela, 600, 400)
    box = scrolledtext.ScrolledText(janela, width=70, height=20)
    box.pack(padx=10, pady=10)

    try:
        with open("data/entregas.json", "r") as f:
            entregas = sistema.carregar_lockers()  # Usar método se preferir
            with open("data/entregas.json", "r") as fe:
                entregas = json.load(fe)
            for e in entregas:
                linha = f"Locker {e['locker']} - Apto {e['apartamento']} - Código {e['codigo']} - {e['data']}\n"
                box.insert(tk.END, linha)
    except:
        box.insert(tk.END, "Nenhuma entrega encontrada.")

def menu_sindico():
    janela = tk.Toplevel()
    janela.title("Menu Síndico")
    centralizar(janela)
    tk.Label(janela, text="Menu do Síndico", font=("Helvetica", 14)).pack(pady=10)

    def cadastrar():
        nome = simpledialog.askstring("Nome", "Nome do morador:")
        ap = simpledialog.askstring("Apt", "Número do apartamento:")
        senha = simpledialog.askstring("Senha", "Senha do morador:")
        sistema.cadastrar_morador(nome, ap, senha)
        messagebox.showinfo("Sucesso", "Morador cadastrado!")

    def excluir():
        ap = simpledialog.askstring("Excluir", "Apartamento a excluir:")
        sistema.excluir_morador(ap)
        messagebox.showinfo("Sucesso", "Morador excluído!")

    def reconfigurar():
        for tam in ["P", "M", "G"]:
            nova_qtd = simpledialog.askinteger("Reconfigurar", f"Nova qtd para locker {tam}:")
            sistema.config["lockers"][tam] = nova_qtd
        sistema.salvar_configuracoes()
        sistema.criar_lockers()
        messagebox.showinfo("Sucesso", "Configuração atualizada!")

    def gerar_relatorio():
        sistema.gerar_relatorio_txt()
        messagebox.showinfo("Relatório", "Relatório gerado com sucesso em /data.")

    tk.Button(janela, text="Cadastrar Morador", width=30, command=cadastrar).pack(pady=5)
    tk.Button(janela, text="Excluir Morador", width=30, command=excluir).pack(pady=5)
    tk.Button(janela, text="Reconfigurar Lockers", width=30, command=reconfigurar).pack(pady=5)
    tk.Button(janela, text="Ver Histórico de Entregas", width=30, command=exibir_historico).pack(pady=5)
    tk.Button(janela, text="Gerar Relatório TXT", width=30, command=gerar_relatorio).pack(pady=5)
    tk.Button(janela, text="Fechar", width=30, command=janela.destroy).pack(pady=5)

def menu_morador(morador):
    janela = tk.Toplevel()
    janela.title("Menu Morador")
    centralizar(janela)
    tk.Label(janela, text=f"Bem-vindo, {morador.nome}", font=("Helvetica", 14)).pack(pady=10)

    def alterar_dados():
        novo_nome = simpledialog.askstring("Alterar", "Novo nome:")
        nova_senha = simpledialog.askstring("Alterar", "Nova senha:")
        morador.alterar_dados(novo_nome, nova_senha)
        sistema.salvar_moradores()
        messagebox.showinfo("Sucesso", "Dados alterados!")

    def retirar():
        numero = simpledialog.askinteger("Locker", "Número do locker:")
        codigo = simpledialog.askstring("Código", "Código recebido:")
        if sistema.retirar_encomenda(numero, codigo):
            messagebox.showinfo("Sucesso", "Encomenda retirada!")
        else:
            messagebox.showerror("Erro", "Dados incorretos.")

    tk.Button(janela, text="Alterar Dados", width=30, command=alterar_dados).pack(pady=5)
    tk.Button(janela, text="Retirar Encomenda", width=30, command=retirar).pack(pady=5)
    tk.Button(janela, text="Fechar", width=30, command=janela.destroy).pack(pady=5)

def menu_entregador():
    janela = tk.Toplevel()
    janela.title("Menu Entregador")
    centralizar(janela)
    tk.Label(janela, text="Bem-vindo, Entregador", font=("Helvetica", 14)).pack(pady=10)

    def entregar():
        tamanho = simpledialog.askstring("Tamanho", "Tamanho da encomenda (P/M/G):")
        apt = simpledialog.askstring("Apt", "Apartamento do destinatário:")
        locker_num, codigo = sistema.entregar_encomenda(tamanho, apt)
        if locker_num:
            messagebox.showinfo("Locker Designado", f"Locker: {locker_num} | Código: {codigo}")
        else:
            messagebox.showerror("Erro", codigo)

    tk.Button(janela, text="Entregar Encomenda", width=30, command=entregar).pack(pady=5)
    tk.Button(janela, text="Fechar", width=30, command=janela.destroy).pack(pady=5)

def tela_login():
    senha = simpledialog.askstring("Login", "Digite sua senha")
    if senha == sistema.config["senha_sindico"]:
        menu_sindico()
    elif senha == "entregador":
        menu_entregador()
    else:
        for m in sistema.moradores:
            if m.senha == senha:
                menu_morador(m)
                return
        messagebox.showerror("Erro", "Senha inválida")

# TELA INICIAL
root = tk.Tk()
root.title("Sistema de Lockers")
root.geometry("600x600")
centralizar(root)
tk.Label(root, text="Sistema de Lockers", font=("Helvetica", 16)).pack(pady=40)
tk.Button(root, text="Entrar no Sistema", font=("Helvetica", 14), command=tela_login).pack(pady=10)
root.mainloop()
