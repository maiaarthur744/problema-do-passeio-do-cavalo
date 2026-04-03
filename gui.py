import time
import tkinter as tk
from tkinter import messagebox

from passeio_cavalo import PasseioDoCavalo

class InterfacePasseio:
    def __init__(self, root):
        self.root = root
        self.root.title("Problema do Passeio do Cavalo")
        self.root.geometry("600x700")
        
        self.frame_controles = tk.Frame(root, pady=10)
        self.frame_controles.pack(fill=tk.X)
        
        tk.Label(self.frame_controles, text="Tamanho (N):").grid(row=0, column=0, padx=5)
        self.entry_n = tk.Entry(self.frame_controles, width=5)
        self.entry_n.insert(0, "8")
        self.entry_n.grid(row=0, column=1, padx=5)
        
        tk.Label(self.frame_controles, text="Início X:").grid(row=0, column=2, padx=5)
        self.entry_x = tk.Entry(self.frame_controles, width=5)
        self.entry_x.insert(0, "0")
        self.entry_x.grid(row=0, column=3, padx=5)
        
        tk.Label(self.frame_controles, text="Início Y:").grid(row=0, column=4, padx=5)
        self.entry_y = tk.Entry(self.frame_controles, width=5)
        self.entry_y.insert(0, "0")
        self.entry_y.grid(row=0, column=5, padx=5)
        
        self.btn_iniciar = tk.Button(self.frame_controles, text="Resolver e Animar", command=self.iniciar_simulacao)
        self.btn_iniciar.grid(row=0, column=6, padx=15)
        
        self.lbl_status = tk.Label(root, text="Aguardando configuração...", fg="blue", font=("Arial", 10, "bold"))
        self.lbl_status.pack(pady=5)
        
        self.tamanho_canvas = 500
        self.canvas = tk.Canvas(root, width=self.tamanho_canvas, height=self.tamanho_canvas, bg="white", highlightthickness=1, highlightbackground="black")
        self.canvas.pack(pady=10)
        
        self.tamanho_celula = 0
        self.passo_atual_animacao = 0
        self.caminho_ordenado = {}

    def iniciar_simulacao(self):
        try:
            n = int(self.entry_n.get())
            start_x = int(self.entry_x.get())
            start_y = int(self.entry_y.get())
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira apenas números inteiros.")
            return

        if n <= 4 and n != 1:
            messagebox.showwarning("Aviso", f"Não há solução possível para tabuleiros {n}x{n}.")
            return
        if not (0 <= start_x < n and 0 <= start_y < n):
            messagebox.showerror("Erro", "Posição inicial fora dos limites do tabuleiro.")
            return

        self.canvas.delete("all")
        self.tamanho_celula = self.tamanho_canvas / n
        self.desenhar_grade(n)
        
        self.lbl_status.config(text="Calculando rota...")
        self.root.update()

        passeio = PasseioDoCavalo(n, start_x, start_y)
        inicio_tempo = time.perf_counter()
        sucesso = passeio.resolver()
        fim_tempo = time.perf_counter()
        
        if sucesso:
            tempo_exec = fim_tempo - inicio_tempo
            texto_status = f"Resolvido em {tempo_exec:.4f}s | {passeio.avaliacoes} operações"
            self.lbl_status.config(text=texto_status, fg="green")
            
            self.caminho_ordenado = {}
            for i in range(n):
                for j in range(n):
                    if passeio.tabuleiro[i][j] != -1:
                        self.caminho_ordenado[passeio.tabuleiro[i][j]] = (i, j)
            
            self.passo_atual_animacao = 0
            self.btn_iniciar.config(state=tk.DISABLED)
            self.animar_passo(n)
        else:
            self.lbl_status.config(text="Sem solução para esta posição.", fg="red")

    def desenhar_grade(self, n):
        for i in range(n):
            for j in range(n):
                x1 = j * self.tamanho_celula
                y1 = i * self.tamanho_celula
                x2 = x1 + self.tamanho_celula
                y2 = y1 + self.tamanho_celula
                
                cor = "#DDBB99" if (i + j) % 2 == 0 else "#8B5A2B"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=cor, outline="black")

    def animar_passo(self, n):
        total_passos = n * n
        if self.passo_atual_animacao < total_passos:
            x, y = self.caminho_ordenado[self.passo_atual_animacao]
            
            x1 = y * self.tamanho_celula
            y1 = x * self.tamanho_celula
            x2 = x1 + self.tamanho_celula
            y2 = y1 + self.tamanho_celula
            
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="#4CAF50", outline="black")
            
            centro_x = x1 + (self.tamanho_celula / 2)
            centro_y = y1 + (self.tamanho_celula / 2)
            fonte = max(8, int(self.tamanho_celula * 0.4)) 
            self.canvas.create_text(centro_x, centro_y, text=str(self.passo_atual_animacao), font=("Arial", fonte, "bold"), fill="white")
            
            self.passo_atual_animacao += 1
            
            self.root.after(50, lambda: self.animar_passo(n))
        else:
            self.btn_iniciar.config(state=tk.NORMAL)