import customtkinter as ctk
from tkinter import *
import sqlite3
from tkinter import messagebox

# tema escuro
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class BackEnd():
    def conectar_db(self):
        self.conn = sqlite3.connect("Usuarios e produto.db")
        self.cursor = self.conn.cursor()
        print("Banco de dados conectado com sucesso")

    def desconectar_db(self):
        self.conn.close()
        print("Banco de dados desconectado")

    def criar_tabela(self):
        self.conectar_db()

        self.cursor.execute(""" 
            CREATE TABLE IF NOT EXISTS Usuarios(
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Usuario TEXT NOT NULL,
                EMAIL TEXT NOT NULL,
                Senha TEXT NOT NULL,
                Produto TEXT NOT NULL,
                Cor_produto TEXT NOT NULL
            );
        """)
        self.conn.commit()
        print("Tabela criada")
        self.desconectar_db()

# Cadastro do usuario no banco de dados
    def cadastrar_usuario(self):
        self.usuario_cadastro = self.usuario_cadastro_entry.get()
        self.email_cadastro = self.email_cadastro_entry.get()
        self.senha_cadastro = self.senha_cadastro_entry.get()
        self.produto_favorito = self.produto_favorito_entry.get()
        self.cor_produto = self.cor_produto.get()

        self.conectar_db()
        self.cursor.execute("""
            INSERT INTO Usuarios (Usuario, Email, Senha, Produto, Cor_produto)
            VALUES (?, ?, ?, ?, ?)""", (self.usuario_cadastro, self.email_cadastro, self.senha_cadastro, self.produto_favorito.upper(), self.cor_produto))

        try:
            if (self.usuario_cadastro == "" or self.email_cadastro == "" or self.senha_cadastro == "" or self.produto_favorito == ""):
                messagebox.showwarning(
                    title="Sistema de login", message="ERRO! \nCampos obrigatorios incompletos(*)!")
            elif (len(self.usuario_cadastro) < 4):
                messagebox.showwarning(
                    title="Cadastro", message="O nome de usuario deve conter pelo menos 4 caracteres")
            elif (len(self.senha_cadastro) < 6 or self.senha_cadastro == "123456"):
                messagebox.showwarning(
                    title="Cadastro", message="A senha do usuario deve conter pelo menos 6 caracteres e nao pode ser uma sequencia ")
            else:
                self.conn.commit()
                messagebox.showinfo(
                    title="Cadastro", message=f"Cadastro realizado com sucesso, bem vindo {self.usuario_cadastro}")
                self.desconectar_db()
                self.limpa_entry_cadastro()
        except:
            messagebox.showwarning(
                title="Cadastro", message="Erro ao concluir o cadastro.\nPor favor, tente novamente.")
            self.desconectar_db


# Verifica se o usuario esta cadastrado no banco de dados


    def verifica_login(self):
        self.usuario_login = self.usuario_login_entry.get()
        self.usuario_senha = self.usuario_senha_entry.get()

        self.conectar_db()
        self.cursor.execute(""" SELECT * FROM Usuarios WHERE (Usuario =? AND Senha =?)""",
                            (self.usuario_login, self.usuario_senha))

        self.verifica_dados = self.cursor.fetchone()

        try:
            if (self.usuario_login == "" or self.usuario_senha == ""):
                messagebox.showwarning(
                    title="Login", message="Preencha todos os campos.")
            elif (self.usuario_login in self.verifica_dados and self.usuario_senha in self.verifica_dados):
                messagebox.showinfo(
                    title="Login", message=f"Login efetuado com sucesso, bem vindo {self.usuario_login}")
                self.desconectar_db
                self.limpa_entry_login()

        except:
            messagebox.showerror(
                title="Login", message="Dados nao cadastrado no sistema.\nVerifique o usuario e a senha ou cadastre-se no sistema")


class App(ctk.CTk, BackEnd):
    def __init__(self):
        super().__init__()
        self.configuracao_janela_inicial()
        self.tela_login()
        self.criar_tabela()

    # config janela principal

    def configuracao_janela_inicial(self):
        self.geometry("700x330")
        self.title("Login Usuario")
        self.resizable(False, False)
        self.iconbitmap("icon_creme.ico")

    def tela_login(self):

        # imagens
        self.img = PhotoImage(file='cosmeticos (4).png')
        self.lb_img = ctk.CTkLabel(self, text=None, image=self.img)
        self.lb_img.grid(row=1, column=0, padx=10)

        # login e senha
        self.frame_login = ctk.CTkFrame(self, width=350, height=330)
        self.frame_login.place(x=370, y=0)

        # widgets login
        self.lb_titulo = ctk.CTkLabel(
            self.frame_login, text="Faca o login", font=("Century Gothic bold", 20))
        self.lb_titulo.grid(row=0, column=0, padx=10, pady=10)

        self.usuario_login_entry = ctk.CTkEntry(self.frame_login, width=300, placeholder_text="Usuario", font=(
            "Century Gothic bold", 14), corner_radius=15, border_color="teal")
        self.usuario_login_entry.grid(row=1, column=0, padx=10, pady=10)

        self.usuario_senha_entry = ctk.CTkEntry(self.frame_login, width=300, placeholder_text="Senha", show="*", font=(
            "Century Gothic bold", 14), corner_radius=15, border_color="teal")
        self.usuario_senha_entry.grid(row=2, column=0, padx=10, pady=10)

        self.botao_login = ctk.CTkButton(self.frame_login, width=300, text="Entrar".upper(
        ), font=("Century Gothic bold", 14), corner_radius=10, command=self.verifica_login)
        self.botao_login.grid(row=4, column=0, padx=10, pady=10)

        self.span = ctk.CTkLabel(
            self.frame_login, text="Nao tem conta?", font=("Century Gothic bold", 10))
        self.span.grid(row=5, column=0, pady=1, padx=10)

        self.botao_cadastro = ctk.CTkButton(self.frame_login, width=300, fg_color="green", text="Cadastre-se".upper(
        ), font=("Century Gothic bold", 14), corner_radius=15, command=self.tela_cadastro)
        self.botao_cadastro.grid(row=6, column=0, pady=11, padx=10)

        self.botao_vazio = ctk.CTkButton(self.frame_login, width=300, text="".upper(
        ), font=("Century Gothic bold", 14), corner_radius=10, fg_color="#212020", command=self.tela_login, state=DISABLED)
        self.botao_vazio.grid(row=7, column=0, padx=10, pady=5)


# trocar tela de login para de cadastro


    def tela_cadastro(self):
        self.title("Cadastro do usuario e produto")
        self.frame_login.place_forget()

        # formulario de cadastro
        self.frame_cadastro = ctk.CTkFrame(self, width=350, height=330)
        self.frame_cadastro.place(x=370, y=0)

        # Cadastro
        self.lb_titulo = ctk.CTkLabel(
            self.frame_login, text="Cadastro", font=("Century Gothic bold", 20))
        self.lb_titulo.grid(row=0, column=0, padx=10, pady=10)

        # campos de cadastro
        self.lb_titulo = ctk.CTkLabel(
            self.frame_cadastro, text="Pesquisa rapida", font=("Century Gothic bold", 14))
        self.lb_titulo.grid(row=0, column=0, padx=10, pady=5)

        self.usuario_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="*Nome", font=(
            "Century Gothic bold", 14), corner_radius=15, border_color="teal")
        self.usuario_cadastro_entry.grid(row=1, column=0, padx=10, pady=5)

        self.senha_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="*Senha do usuario",
                                                 show="*", font=("Century Gothic bold", 14), corner_radius=15, border_color="teal")
        self.senha_cadastro_entry.grid(row=2, column=0, padx=10, pady=5)

        self.email_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="*E-mail para contato", font=(
            "Century Gothic bold", 14), corner_radius=15, border_color="teal")
        self.email_cadastro_entry.grid(row=3, column=0, padx=10, pady=5)

        self.produto_favorito_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="*Produto favorito",
                                                   font=("Century Gothic bold", 14), corner_radius=15, border_color="teal", )
        self.produto_favorito_entry.grid(row=4, column=0, padx=10, pady=5)

        # janela das cores do produto
        cor_default = ctk.StringVar(value="Qual a cor do produto: ")
        self.cor_produto = ctk.CTkOptionMenu(self.frame_cadastro,
                                             values=["Clara",
                                                     "Escura", "Incolor"],
                                             variable=cor_default,
                                             width=300,
                                             fg_color="grey",
                                             dropdown_text_color="white",
                                             button_color="teal",
                                             button_hover_color="teal",
                                             )
        self.cor_produto.grid(row=5, column=0, padx=10, pady=10)

        # botao de cadastro
        self.botao_cadastro_usuario = ctk.CTkButton(self.frame_cadastro, width=300, fg_color="green", text="Cadastrar".upper(
        ), font=("Century Gothic bold", 14), corner_radius=15, command=self.cadastrar_usuario)
        self.botao_cadastro_usuario.grid(row=6, column=0, pady=5, padx=10)

        # botao de voltar para tela de login
        self.botao_voltar_login = ctk.CTkButton(self.frame_cadastro, width=300, text="Voltar".upper(
        ), font=("Century Gothic bold", 14), corner_radius=10, fg_color="#444", command=self.tela_login)
        self.botao_voltar_login.grid(row=7, column=0, padx=10, pady=5)

    # Limpando dados das caixas pos cadastro

    def limpa_entry_cadastro(self):
        self.usuario_cadastro_entry.delete(0, END)
        self.email_cadastro_entry.delete(0, END)
        self.produto_favorito_entry.delete(0, END)
        self.senha_cadastro_entry.delete(0, END)

    # Limpa dados das caixas apos logar

    def limpa_entry_login(self):
        self.usuario_login_entry.delete(0, END)
        self.usuario_senha_entry.delete(0, END)


if __name__ == "__main__":
    app = App()
    app.mainloop()
