import customtkinter as ctk
from tkinter import *
import sqlite3
from tkinter import messagebox


class BackEnd():
    def conectar_db(self):
        self.conn = sqlite3.connect("Usuarios cadastrados no sistema.db")
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
                Confirma_Senha TEXT NOT NULL
            );
        """)
        self.conn.commit()
        print("Tabela criada")
        self.desconectar_db()

    def cadastrar_usuario(self):
        self.usuario_cadastro = self.usuario_cadastro_entry.get()
        self.email_cadastro = self.email_cadastro_entry.get()
        self.senha_cadastro = self.senha_cadastro_entry.get()
        self.confirmar_senha_cadastro = self.confirmar_senha_entry.get()

        self.conectar_db()
        self.cursor.execute("""
            INSERT INTO Usuarios (Usuario, Email, Senha, Confirma_senha)
            VALUES (?, ?, ?, ?)""", (
        self.usuario_cadastro, self.email_cadastro, self.senha_cadastro, self.confirmar_senha_cadastro))

        # Requisitos para cadastro
        try:
            if (
                    self.usuario_cadastro == "" or self.email_cadastro == "" or self.senha_cadastro == "" or self.confirmar_senha_cadastro == ""):
                messagebox.showerror(title="Sistema de login", message="ERRO! \nCampos obrigatorios incompletos")
            elif (len(self.usuario_cadastro) < 4):
                messagebox.showwarning(title="Login", message="O nome de usuario deve conter pelo menos 4 caracteres")
            elif (len(self.senha_cadastro) < 6):
                messagebox.showwarning(title="Login", message="A senha do usuario deve conter pelo menos 6 caracteres")
            elif (self.senha_cadastro != self.confirmar_senha_cadastro):
                messagebox.showerror(title="Login", message="Senhas diferentes, coloque as senhas iguais")
            else:
                self.conn.commit()
                messagebox.showinfo(title="Login",
                                    message=f"Cadastro realizado com sucesso, bem vindo {self.usuario_cadastro}")
        except:
            messagebox.showerror(title="Login", message="Erro ao concluir o cadastro.\nPor favor, tente novamente.")


class App(ctk.CTk, BackEnd):
    def __init__(self):
        super().__init__()
        self.configuracao_janela_inicial()
        self.tela_login()
        self.criar_tabela()

    # config janela principal
    def configuracao_janela_inicial(self):
        self.geometry("700x330")
        self.title("Login Orkut")
        self.resizable(False, False)
        self.iconbitmap("orkut-icon.ico")

    def tela_login(self):
        # imagens
        self.img = PhotoImage(file='pagorkut2.png')
        self.lb_img = ctk.CTkLabel(self, text=None, image=self.img)
        self.lb_img.grid(row=1, column=0, padx=10)

        # login e senha
        self.frame_login = ctk.CTkFrame(self, width=350, height=330)
        self.frame_login.place(x=370, y=0)

        # widgets login
        self.lb_titulo = ctk.CTkLabel(self.frame_login, text="Faca o login", font=("Century Gothic bold", 20))
        self.lb_titulo.grid(row=0, column=0, padx=10, pady=10)

        self.usuario_login_entry = ctk.CTkEntry(self.frame_login, width=300, placeholder_text="Usuario",
                                                font=("Century Gothic bold", 14), corner_radius=15, border_color="pink")
        self.usuario_login_entry.grid(row=1, column=0, padx=10, pady=10)

        self.usuario_senha_entry = ctk.CTkEntry(self.frame_login, width=300, placeholder_text="Senha", show="*",
                                                font=("Century Gothic bold", 14), corner_radius=15, border_color="pink")
        self.usuario_senha_entry.grid(row=2, column=0, padx=10, pady=10)

        self.ver_senha = ctk.CTkCheckBox(self.frame_login, text="Visualizar senha", font=("Century Gothic bold", 12),
                                         corner_radius=20)
        self.ver_senha.grid(row=3, column=0, padx=10, pady=10)

        self.botao_login = ctk.CTkButton(self.frame_login, width=300, text="Entrar".upper(),
                                         font=("Century Gothic bold", 14), corner_radius=10)
        self.botao_login.grid(row=4, column=0, padx=10, pady=10)

        self.span = ctk.CTkLabel(self.frame_login, text="Nao tem conta?", font=("Century Gothic bold", 10))
        self.span.grid(row=5, column=0, pady=1, padx=10)

        self.botao_cadastro = ctk.CTkButton(self.frame_login, width=300, fg_color="green", text="Cadastre-se".upper(),
                                            font=("Century Gothic bold", 14), corner_radius=15,
                                            command=self.tela_cadastro)
        self.botao_cadastro.grid(row=6, column=0, pady=1, padx=10)

    # trocar tela de login para de cadastro
    def tela_cadastro(self):
        self.frame_login.place_forget()

        # formulario de cadastro
        self.frame_cadastro = ctk.CTkFrame(self, width=350, height=330)
        self.frame_cadastro.place(x=370, y=0)

        # Cadastro
        self.lb_titulo = ctk.CTkLabel(self.frame_login, text="Cadastro", font=("Century Gothic bold", 20))
        self.lb_titulo.grid(row=0, column=0, padx=10, pady=10)

        # campos de cadastro
        self.lb_titulo = ctk.CTkLabel(self.frame_cadastro, text="Campos obrigatorios (*)",
                                      font=("Century Gothic bold", 14))
        self.lb_titulo.grid(row=0, column=0, padx=10, pady=5)

        self.usuario_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="*Nome de usuario",
                                                   font=("Century Gothic bold", 14), corner_radius=15,
                                                   border_color="pink")
        self.usuario_cadastro_entry.grid(row=1, column=0, padx=10, pady=5)

        self.email_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="*E-mail do usuario",
                                                 font=("Century Gothic bold", 14), corner_radius=15,
                                                 border_color="pink")
        self.email_cadastro_entry.grid(row=2, column=0, padx=10, pady=5)

        self.senha_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="*Senha do usuario",
                                                 show="*", font=("Century Gothic bold", 14), corner_radius=15,
                                                 border_color="pink")
        self.senha_cadastro_entry.grid(row=3, column=0, padx=10, pady=5)

        self.confirmar_senha_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="*Confirme a senha",
                                                  show="*", font=("Century Gothic bold", 14), corner_radius=15,
                                                  border_color="pink")
        self.confirmar_senha_entry.grid(row=4, column=0, padx=10, pady=5)

        # check box para ver a senha
        self.ver_senha = ctk.CTkCheckBox(self.frame_cadastro, text="Visualizar senha", font=("Century Gothic bold", 12),
                                         corner_radius=20)
        self.ver_senha.grid(row=5, column=0, pady=5)

        # botao de cadastro
        self.botao_cadastro_usuario = ctk.CTkButton(self.frame_cadastro, width=300, fg_color="green",
                                                    text="Cadastrar".upper(), font=("Century Gothic bold", 14),
                                                    corner_radius=15, command=self.cadastrar_usuario)
        self.botao_cadastro_usuario.grid(row=6, column=0, pady=5, padx=10)

        # botao de voltar para tela de login
        self.botao_voltar_login = ctk.CTkButton(self.frame_cadastro, width=300, text="Voltar".upper(),
                                                font=("Century Gothic bold", 14), corner_radius=10, fg_color="#444",
                                                command=self.tela_login)
        self.botao_voltar_login.grid(row=7, column=0, padx=10, pady=5)

    # Limpando dados das caixas pos cadastro
    def limpa_entry_cadastro(self):
        self.usuario_cadastro_entry.delete(0, END)
        self.email_cadastro_entry.delete(0, END)
        self.senha_cadastro_entry.delete(0, END)
        self.confirmar_senha_cadastro_entry.delete(0, END)

    # Limpa dados das caixas apos logar
    def limpa_entry_login(self):
        self.usuario_login_entry.delete(0, END)
        self.usuario_senha_entry.delete(0, END)


if __name__ == "__main__":
    app = App()
    app.mainloop()

