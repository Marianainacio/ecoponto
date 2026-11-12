import tkinter as tk
from tkinter import messagebox
import json
import hashlib
import os

# Arquivo onde ficam os cadastros
arquivo = "usuarios.json"

if os.path.exists(arquivo):
    with open(arquivo, "r") as f:
        usuarios = json.load(f)
else:
    usuarios = {}


def salvar():
    with open(arquivo, "w") as f:
        json.dump(usuarios, f, indent=4)


def limpar():
    for item in tela.winfo_children():
        item.destroy()


def titulo():
    tk.Label(
        tela,
        text="EcoPonto",
        font=("Arial", 30, "bold"),
        bg="#C9F2D0",
        fg="#176B35"
    ).pack(pady=20)

    tk.Label(
        tela,
        text="Recicle hoje, preserve o amanhã.",
        font=("Arial", 13),
        bg="#C9F2D0",
        fg="#176B35"
    ).pack(pady=5)


def campo(texto, senha=False):
    tk.Label(
        quadro,
        text=texto,
        bg="white",
        fg="#333333",
        font=("Arial", 11)
    ).pack(anchor="w", padx=25, pady=(10, 3))

    entrada = tk.Entry(
        quadro,
        font=("Arial", 12),
        show="*" if senha else "",
        relief="flat",
        bg="#EEEEEE"
    )
    entrada.pack(fill="x", padx=25, ipady=8)

    return entrada


def botao(texto, funcao):
    tk.Button(
        quadro,
        text=texto,
        command=funcao,
        bg="#55B957",
        fg="white",
        font=("Arial", 13, "bold"),
        relief="flat",
        cursor="hand2"
    ).pack(fill="x", padx=25, pady=20, ipady=8)


# Tela de login
def login():
    limpar()
    titulo()

    global quadro
    quadro = tk.Frame(tela, bg="white")
    quadro.pack(fill="x", padx=30, pady=25)

    tk.Label(
        quadro,
        text="LOGIN",
        font=("Arial", 20, "bold"),
        bg="white",
        fg="#176B35"
    ).pack(pady=15)

    email = campo("Email")
    senha = campo("Senha", True)

    def entrar():
        e = email.get().lower().strip()
        s = hashlib.sha256(senha.get().encode()).hexdigest()

        if e == "" or senha.get() == "":
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
        elif e not in usuarios:
            messagebox.showerror("Erro", "Usuário não encontrado!")
        elif usuarios[e]["senha"] == s:
            inicio(usuarios[e]["nome"])
        else:
            messagebox.showerror("Erro", "Senha incorreta!")

    botao("Entrar", entrar)

    tk.Button(
        tela,
        text="Não tem conta? Cadastre-se",
        command=cadastro,
        bg="#C9F2D0",
        fg="#176B35",
        font=("Arial", 11),
        relief="flat"
    ).pack(pady=15)


# Tela de cadastro
def cadastro():
    limpar()
    titulo()

    global quadro
    quadro = tk.Frame(tela, bg="white")
    quadro.pack(fill="x", padx=30, pady=15)

    tk.Label(
        quadro,
        text="CADASTRO",
        font=("Arial", 20, "bold"),
        bg="white",
        fg="#176B35"
    ).pack(pady=10)

    nome = campo("Nome")
    email = campo("Email")
    senha = campo("Senha", True)
    confirmar = campo("Confirmar senha", True)

    def cadastrar():
        n = nome.get().strip()
        e = email.get().lower().strip()
        s = senha.get()
        c = confirmar.get()

        if n == "" or e == "" or s == "" or c == "":
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
        elif "@" not in e or "." not in e:
            messagebox.showwarning("Aviso", "Digite um email válido!")
        elif e in usuarios:
            messagebox.showerror("Erro", "Email já cadastrado!")
        elif len(s) < 6:
            messagebox.showwarning("Aviso", "A senha precisa ter 6 caracteres!")
        elif s != c:
            messagebox.showerror("Erro", "As senhas não são iguais!")
        else:
            senha_hash = hashlib.sha256(s.encode()).hexdigest()

            usuarios[e] = {
                "nome": n,
                "senha": senha_hash
            }

            salvar()

            messagebox.showinfo("Sucesso", "Cadastro realizado!")
            login()

    botao("Cadastrar", cadastrar)

    tk.Button(
        tela,
        text="Voltar para o login",
        command=login,
        bg="#C9F2D0",
        fg="#176B35",
        font=("Arial", 11),
        relief="flat"
    ).pack(pady=10)


# Tela inicial
def inicio(nome):
    limpar()

    tk.Label(
        tela,
        text="EcoPonto 🌱",
        font=("Arial", 30, "bold"),
        bg="#C9F2D0",
        fg="#176B35"
    ).pack(pady=70)

    tk.Label(
        tela,
        text="Bem-vindo, " + nome + "!",
        font=("Arial", 20, "bold"),
        bg="#C9F2D0",
        fg="#176B35"
    ).pack(pady=20)

    tk.Label(
        tela,
        text="Obrigado por ajudar o meio ambiente!",
        font=("Arial", 12),
        bg="#C9F2D0",
        fg="#176B35"
    ).pack(pady=10)

    tk.Button(
        tela,
        text="Sair",
        command=login,
        bg="#55B957",
        fg="white",
        font=("Arial", 13),
        relief="flat"
    ).pack(pady=30, ipadx=40, ipady=8)


# Configuração da janela
janela = tk.Tk()
janela.title("EcoPonto")
janela.geometry("430x650")
janela.resizable(False, False)

tela = tk.Frame(janela, bg="#C9F2D0")
tela.pack(fill="both", expand=True)

login()

janela.mainloop()