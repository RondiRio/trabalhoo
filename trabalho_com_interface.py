from search import Problem, breadth_first_graph_search, best_first_graph_search, astar_search
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time

class RecipientesAgua(Problem):
    """Problema dos recipientes de água configurável"""
    
    def __init__(self, cap1, cap2, objetivo, inicial1=0, inicial2=0):
        self.cap1 = cap1
        self.cap2 = cap2
        self.objetivo = objetivo
        super().__init__((inicial1, inicial2))
    
    def actions(self, state):
        """Ações possíveis: encher, esvaziar, transferir"""
        x, y = state
        acoes = []
        
        if x < self.cap1: acoes.append(f'encher_{self.cap1}L')
        if y < self.cap2: acoes.append(f'encher_{self.cap2}L')
        if x > 0: acoes.append(f'esvaziar_{self.cap1}L')
        if y > 0: acoes.append(f'esvaziar_{self.cap2}L')
        if x > 0 and y < self.cap2: acoes.append(f'{self.cap1}L_para_{self.cap2}L')
        if y > 0 and x < self.cap1: acoes.append(f'{self.cap2}L_para_{self.cap1}L')
        
        return acoes
    
    def result(self, state, action):
        """Retorna novo estado após ação"""
        x, y = state
        
        if action == f'encher_{self.cap1}L':
            return (self.cap1, y)
        elif action == f'encher_{self.cap2}L':
            return (x, self.cap2)
        elif action == f'esvaziar_{self.cap1}L':
            return (0, y)
        elif action == f'esvaziar_{self.cap2}L':
            return (x, 0)
        elif action == f'{self.cap1}L_para_{self.cap2}L':
            transfer = min(x, self.cap2 - y)
            return (x - transfer, y + transfer)
        elif action == f'{self.cap2}L_para_{self.cap1}L':
            transfer = min(y, self.cap1 - x)
            return (x + transfer, y - transfer)
    
    def goal_test(self, state):
        """Verifica se atingiu objetivo"""
        return sum(state) == self.objetivo
    
    def h(self, node):
        """Heurística: distância até objetivo"""
        return abs(self.objetivo - sum(node.state))

class ModernButton(tk.Canvas):
    """Botão moderno customizado com hover effects"""
    def __init__(self, parent, text, command, bg_color, hover_color, **kwargs):
        super().__init__(parent, highlightthickness=0, **kwargs)
        self.command = command
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text = text
        
        self.config(bg=bg_color, cursor='hand2')
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
        self.bind('<Button-1>', self.on_click)
        
        self.create_text(self.winfo_reqwidth()//2, self.winfo_reqheight()//2,
                        text=text, fill='white', font=('Segoe UI', 11, 'bold'),
                        tags='text')
    
    def on_enter(self, e):
        self.config(bg=self.hover_color)
    
    def on_leave(self, e):
        self.config(bg=self.bg_color)
    
    def on_click(self, e):
        self.command()

class RecipientesGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Problema dos Recipientes de Água")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f5f5f7')
        self.root.resizable(False, False)
        
        # Estilo moderno
        self.colors = {
            'primary': '#007AFF',
            'primary_hover': '#0051D5',
            'secondary': '#5856D6',
            'secondary_hover': '#4644B8',
            'success': '#34C759',
            'success_hover': '#2AAD4B',
            'warning': '#FF9500',
            'danger': '#FF3B30',
            'bg': '#f5f5f7',
            'card': '#ffffff',
            'text': '#1d1d1f',
            'text_secondary': '#86868b',
            'border': '#d2d2d7',
            'water': '#007AFF'
        }
        
        self.problema = None
        self.animacao_ativa = False
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configura a interface moderna"""
        # Container principal com padding
        main_container = tk.Frame(self.root, bg=self.colors['bg'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Header
        header = tk.Frame(main_container, bg=self.colors['bg'])
        header.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(header, text="Problema dos Recipientes de Água", 
                font=('Segoe UI', 28, 'bold'), bg=self.colors['bg'], 
                fg=self.colors['text']).pack(anchor='w')
        
        tk.Label(header, text="Configure os parâmetros e escolha um algoritmo de busca", 
                font=('Segoe UI', 12), bg=self.colors['bg'], 
                fg=self.colors['text_secondary']).pack(anchor='w', pady=(5, 0))
        
        # Card de configuração
        config_card = tk.Frame(main_container, bg=self.colors['card'], 
                              relief=tk.FLAT, bd=0)
        config_card.pack(fill=tk.X, pady=(0, 20))
        
        # Adicionar sombra simulada
        shadow = tk.Frame(config_card, bg='#e0e0e0', height=1)
        shadow.pack(side=tk.BOTTOM, fill=tk.X)
        
        config_inner = tk.Frame(config_card, bg=self.colors['card'])
        config_inner.pack(fill=tk.X, padx=25, pady=20)
        
        tk.Label(config_inner, text="Configuração do Problema", 
                font=('Segoe UI', 16, 'bold'), bg=self.colors['card'], 
                fg=self.colors['text']).pack(anchor='w', pady=(0, 15))
        
        # Grid de inputs
        inputs_frame = tk.Frame(config_inner, bg=self.colors['card'])
        inputs_frame.pack(fill=tk.X)
        
        # Função helper para criar input estilizado
        def criar_input(parent, label, default, row, col):
            frame = tk.Frame(parent, bg=self.colors['card'])
            frame.grid(row=row, column=col, padx=10, pady=8, sticky='w')
            
            tk.Label(frame, text=label, font=('Segoe UI', 11), 
                    bg=self.colors['card'], fg=self.colors['text_secondary']).pack(anchor='w')
            
            entry = tk.Entry(frame, font=('Segoe UI', 12), relief=tk.FLAT, 
                           bg='#f9f9f9', fg=self.colors['text'], 
                           insertbackground=self.colors['primary'],
                           highlightthickness=1, highlightcolor=self.colors['primary'],
                           highlightbackground=self.colors['border'])
            entry.pack(fill=tk.X, ipady=8, ipadx=10, pady=(5, 0))
            entry.insert(0, default)
            return entry
        
        self.cap1_entry = criar_input(inputs_frame, "Capacidade Recipiente 1 (L)", "4", 0, 0)
        self.cap2_entry = criar_input(inputs_frame, "Capacidade Recipiente 2 (L)", "3", 0, 1)
        self.obj_entry = criar_input(inputs_frame, "Objetivo (L)", "2", 0, 2)
        self.ini1_entry = criar_input(inputs_frame, "Inicial Recipiente 1 (L)", "0", 1, 0)
        self.ini2_entry = criar_input(inputs_frame, "Inicial Recipiente 2 (L)", "0", 1, 1)
        
        # Botão configurar
        btn_frame = tk.Frame(inputs_frame, bg=self.colors['card'])
        btn_frame.grid(row=1, column=2, padx=10, pady=8, sticky='ew')
        
        self.btn_config = tk.Button(btn_frame, text="Configurar", 
                                    command=self.configurar_problema,
                                    bg=self.colors['primary'], fg='white',
                                    font=('Segoe UI', 11, 'bold'), relief=tk.FLAT,
                                    cursor='hand2', activebackground=self.colors['primary_hover'],
                                    activeforeground='white', bd=0)
        self.btn_config.pack(fill=tk.BOTH, expand=True, ipady=8, pady=(24, 0))
        
        # Área de visualização e controles
        content_frame = tk.Frame(main_container, bg=self.colors['bg'])
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Coluna esquerda - Visualização
        left_frame = tk.Frame(content_frame, bg=self.colors['card'])
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        shadow_left = tk.Frame(left_frame, bg='#e0e0e0', height=1)
        shadow_left.pack(side=tk.BOTTOM, fill=tk.X)
        
        left_inner = tk.Frame(left_frame, bg=self.colors['card'])
        left_inner.pack(fill=tk.BOTH, expand=True, padx=25, pady=20)
        
        tk.Label(left_inner, text="Visualização", 
                font=('Segoe UI', 16, 'bold'), bg=self.colors['card'], 
                fg=self.colors['text']).pack(anchor='w', pady=(0, 15))
        
        # Canvas para recipientes
        self.canvas = tk.Canvas(left_inner, width=650, height=400, 
                               bg=self.colors['card'], highlightthickness=0)
        self.canvas.pack()
        
        # Info label
        self.info_label = tk.Label(left_inner, text="Configure o problema para começar", 
                                   font=('Segoe UI', 11), bg=self.colors['card'], 
                                   fg=self.colors['text_secondary'])
        self.info_label.pack(pady=(10, 0))
        
        # Coluna direita - Controles e Log
        right_frame = tk.Frame(content_frame, bg=self.colors['bg'], width=400)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))
        right_frame.pack_propagate(False)
        
        # Card de algoritmos
        algo_card = tk.Frame(right_frame, bg=self.colors['card'])
        algo_card.pack(fill=tk.X, pady=(0, 10))
        
        shadow_algo = tk.Frame(algo_card, bg='#e0e0e0', height=1)
        shadow_algo.pack(side=tk.BOTTOM, fill=tk.X)
        
        algo_inner = tk.Frame(algo_card, bg=self.colors['card'])
        algo_inner.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(algo_inner, text="Algoritmos de Busca", 
                font=('Segoe UI', 14, 'bold'), bg=self.colors['card'], 
                fg=self.colors['text']).pack(anchor='w', pady=(0, 15))
        
        # Botões de algoritmo
        self.btn_bfs = tk.Button(algo_inner, text="🔵 Busca em Largura (BFS)",
                                command=lambda: self.executar_busca('bfs'),
                                bg=self.colors['primary'], fg='white',
                                font=('Segoe UI', 10, 'bold'), relief=tk.FLAT,
                                cursor='hand2', activebackground=self.colors['primary_hover'],
                                activeforeground='white', bd=0)
        self.btn_bfs.pack(fill=tk.X, ipady=12, pady=(0, 8))
        
        self.btn_greedy = tk.Button(algo_inner, text="⚡ Busca Gulosa (Greedy)",
                                    command=lambda: self.executar_busca('greedy'),
                                    bg=self.colors['secondary'], fg='white',
                                    font=('Segoe UI', 10, 'bold'), relief=tk.FLAT,
                                    cursor='hand2', activebackground=self.colors['secondary_hover'],
                                    activeforeground='white', bd=0)
        self.btn_greedy.pack(fill=tk.X, ipady=12, pady=(0, 8))
        
        self.btn_astar = tk.Button(algo_inner, text="⭐ Busca A*",
                                   command=lambda: self.executar_busca('astar'),
                                   bg=self.colors['success'], fg='white',
                                   font=('Segoe UI', 10, 'bold'), relief=tk.FLAT,
                                   cursor='hand2', activebackground=self.colors['success_hover'],
                                   activeforeground='white', bd=0)
        self.btn_astar.pack(fill=tk.X, ipady=12)
        
        # Card de log
        log_card = tk.Frame(right_frame, bg=self.colors['card'])
        log_card.pack(fill=tk.BOTH, expand=True)
        
        shadow_log = tk.Frame(log_card, bg='#e0e0e0', height=1)
        shadow_log.pack(side=tk.BOTTOM, fill=tk.X)
        
        log_inner = tk.Frame(log_card, bg=self.colors['card'])
        log_inner.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(log_inner, text="Log de Execução", 
                font=('Segoe UI', 14, 'bold'), bg=self.colors['card'], 
                fg=self.colors['text']).pack(anchor='w', pady=(0, 10))
        
        # Text widget para log
        log_container = tk.Frame(log_inner, bg=self.colors['card'])
        log_container.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = tk.Text(log_container, bg='#f9f9f9', fg=self.colors['text'], 
                               font=('Consolas', 9), relief=tk.FLAT, wrap=tk.WORD,
                               highlightthickness=1, highlightcolor=self.colors['border'],
                               highlightbackground=self.colors['border'])
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(log_container, command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scrollbar.set)
        
        self.log_text.insert(tk.END, "Aguardando configuração...\n")
        self.log_text.config(state=tk.DISABLED)
    
    def configurar_problema(self):
        """Configura o problema com os valores inseridos"""
        try:
            cap1 = int(self.cap1_entry.get())
            cap2 = int(self.cap2_entry.get())
            obj = int(self.obj_entry.get())
            ini1 = int(self.ini1_entry.get())
            ini2 = int(self.ini2_entry.get())
            
            if cap1 <= 0 or cap2 <= 0 or obj <= 0:
                raise ValueError("Valores devem ser positivos")
            
            if ini1 > cap1 or ini2 > cap2:
                raise ValueError("Valores iniciais não podem exceder capacidades")
            
            self.problema = RecipientesAgua(cap1, cap2, obj, ini1, ini2)
            self.desenhar_recipientes(ini1, ini2)
            self.info_label.config(text=f"✓ Configurado com sucesso! Objetivo: {obj}L")
            
            self.log_text.config(state=tk.NORMAL)
            self.log_text.delete(1.0, tk.END)
            self.log_text.insert(tk.END, f"✓ Problema configurado\n")
            self.log_text.insert(tk.END, f"  Recipiente 1: {cap1}L\n")
            self.log_text.insert(tk.END, f"  Recipiente 2: {cap2}L\n")
            self.log_text.insert(tk.END, f"  Objetivo: {obj}L\n")
            self.log_text.insert(tk.END, f"  Estado inicial: ({ini1}L, {ini2}L)\n\n")
            self.log_text.insert(tk.END, "Selecione um algoritmo de busca.\n")
            self.log_text.config(state=tk.DISABLED)
            
        except ValueError as e:
            messagebox.showerror("Erro de Validação", str(e))
    
    def desenhar_recipientes(self, x, y, acao=""):
        """Desenha os recipientes com design moderno"""
        self.canvas.delete("all")
        
        if not self.problema:
            # Estado vazio
            self.canvas.create_text(325, 200, text="Configure o problema", 
                                   fill=self.colors['text_secondary'], 
                                   font=('Segoe UI', 14))
            return
        
        # Recipiente 1
        x1, y1 = 100, 80
        largura, altura = 140, 250
        raio = 10
        
        # Desenhar recipiente com cantos arredondados
        self._rounded_rect(self.canvas, x1, y1, x1+largura, y1+altura, 
                          raio, outline=self.colors['border'], width=2, fill='#fafafa')
        
        # Água no recipiente 1
        nivel1 = (x / self.problema.cap1) * altura if self.problema.cap1 > 0 else 0
        if nivel1 > 0:
            y_agua = y1 + altura - nivel1
            self._rounded_rect(self.canvas, x1+2, y_agua, x1+largura-2, y1+altura-2,
                             raio-2, fill=self.colors['water'], outline='')
            
            # Efeito de brilho na água
            self.canvas.create_rectangle(x1+10, y_agua, x1+30, y_agua+20,
                                        fill='#4DA6FF', outline='', stipple='gray50')
        
        # Label do recipiente 1
        self.canvas.create_text(x1+largura//2, y1+altura+25, 
                               text=f"Recipiente 1", 
                               fill=self.colors['text'], 
                               font=('Segoe UI', 12, 'bold'))
        self.canvas.create_text(x1+largura//2, y1+altura+45, 
                               text=f"{x}L / {self.problema.cap1}L", 
                               fill=self.colors['text_secondary'], 
                               font=('Segoe UI', 11))
        
        # Recipiente 2
        x2, y2 = 410, 80
        
        self._rounded_rect(self.canvas, x2, y2, x2+largura, y2+altura, 
                          raio, outline=self.colors['border'], width=2, fill='#fafafa')
        
        # Água no recipiente 2
        nivel2 = (y / self.problema.cap2) * altura if self.problema.cap2 > 0 else 0
        if nivel2 > 0:
            y_agua2 = y2 + altura - nivel2
            self._rounded_rect(self.canvas, x2+2, y_agua2, x2+largura-2, y2+altura-2,
                             raio-2, fill=self.colors['water'], outline='')
            
            # Efeito de brilho na água
            self.canvas.create_rectangle(x2+10, y_agua2, x2+30, y_agua2+20,
                                        fill='#4DA6FF', outline='', stipple='gray50')
        
        # Label do recipiente 2
        self.canvas.create_text(x2+largura//2, y2+altura+25, 
                               text=f"Recipiente 2", 
                               fill=self.colors['text'], 
                               font=('Segoe UI', 12, 'bold'))
        self.canvas.create_text(x2+largura//2, y2+altura+45, 
                               text=f"{y}L / {self.problema.cap2}L", 
                               fill=self.colors['text_secondary'], 
                               font=('Segoe UI', 11))
        
        # Total
        total = x + y
        cor_total = self.colors['success'] if total == self.problema.objetivo else self.colors['text']
        self.canvas.create_text(325, 30, text=f"Total: {total}L", 
                               fill=cor_total, font=('Segoe UI', 18, 'bold'))
        
        if total == self.problema.objetivo:
            self.canvas.create_text(325, 55, text="✓ Objetivo alcançado!", 
                                   fill=self.colors['success'], font=('Segoe UI', 12))
        
        # Ação atual
        if acao:
            self.canvas.create_text(325, 370, text=f"▶ {acao}", 
                                   fill=self.colors['primary'], 
                                   font=('Segoe UI', 11, 'italic'))
    
    def _rounded_rect(self, canvas, x1, y1, x2, y2, radius, **kwargs):
        """Desenha retângulo com cantos arredondados"""
        points = [
            x1+radius, y1,
            x2-radius, y1,
            x2, y1,
            x2, y1+radius,
            x2, y2-radius,
            x2, y2,
            x2-radius, y2,
            x1+radius, y2,
            x1, y2,
            x1, y2-radius,
            x1, y1+radius,
            x1, y1
        ]
        return canvas.create_polygon(points, smooth=True, **kwargs)
    
    def executar_busca(self, tipo):
        """Executa o algoritmo de busca selecionado"""
        if not self.problema:
            messagebox.showwarning("Atenção", "Configure o problema primeiro!")
            return
        
        if self.animacao_ativa:
            messagebox.showinfo("Aguarde", "Uma busca já está em execução.")
            return
        
        thread = threading.Thread(target=self._buscar, args=(tipo,))
        thread.daemon = True
        thread.start()
    
    def _buscar(self, tipo):
        """Executa a busca em thread separada"""
        self.animacao_ativa = True
        
        # Desabilita botões durante busca
        self.root.after(0, lambda: self.btn_bfs.config(state=tk.DISABLED))
        self.root.after(0, lambda: self.btn_greedy.config(state=tk.DISABLED))
        self.root.after(0, lambda: self.btn_astar.config(state=tk.DISABLED))
        
        # Limpa log
        self.root.after(0, lambda: self.log_text.config(state=tk.NORMAL))
        self.root.after(0, lambda: self.log_text.delete(1.0, tk.END))
        
        # Seleciona algoritmo
        if tipo == 'bfs':
            nome = "Busca em Largura (BFS)"
            resultado = breadth_first_graph_search(self.problema)
        elif tipo == 'greedy':
            nome = "Busca Gulosa (Greedy)"
            resultado = best_first_graph_search(self.problema, lambda n: self.problema.h(n))
        else:
            nome = "Busca A*"
            resultado = astar_search(self.problema, lambda n: self.problema.h(n))
        
        # Exibe resultado
        self.root.after(0, lambda: self.log_text.insert(tk.END, f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"))
        self.root.after(0, lambda: self.log_text.insert(tk.END, f"🔍 {nome}\n"))
        self.root.after(0, lambda: self.log_text.insert(tk.END, f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"))
        
        if not resultado:
            self.root.after(0, lambda: self.log_text.insert(tk.END, "❌ Nenhuma solução encontrada!\n"))
            self.root.after(0, lambda: self.log_text.config(state=tk.DISABLED))
            self.animacao_ativa = False
            self.root.after(0, lambda: self.btn_bfs.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.btn_greedy.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.btn_astar.config(state=tk.NORMAL))
            return
        
        caminho = resultado.path()
        self.root.after(0, lambda: self.log_text.insert(tk.END, f"✓ Solução encontrada!\n"))
        self.root.after(0, lambda: self.log_text.insert(tk.END, f"📊 Total de passos: {len(caminho)-1}\n\n"))
        
        # Anima cada passo
        for i, no in enumerate(caminho):
            x, y = no.state
            acao = no.action if i > 0 else "Estado inicial"
            
            self.root.after(0, self.desenhar_recipientes, x, y, acao)
            
            def inserir_log(passo, ac, xx, yy):
                self.log_text.insert(tk.END, f"Passo {passo}:\n")
                self.log_text.insert(tk.END, f"  Ação: {ac}\n")
                self.log_text.insert(tk.END, f"  Estado: ({xx}L, {yy}L)\n")
                self.log_text.insert(tk.END, f"  Total: {xx+yy}L\n\n")
                self.log_text.see(tk.END)
            
            self.root.after(0, inserir_log, i, acao, x, y)
            
            if self.problema.goal_test(no.state):
                self.root.after(0, lambda: self.log_text.insert(tk.END, "🎉 OBJETIVO ALCANÇADO!\n"))
            
            time.sleep(1.2)
        
        self.root.after(0, lambda: self.log_text.config(state=tk.DISABLED))
        self.root.after(0, lambda: self.btn_bfs.config(state=tk.NORMAL))
        self.root.after(0, lambda: self.btn_greedy.config(state=tk.NORMAL))
        self.root.after(0, lambda: self.btn_astar.config(state=tk.NORMAL))
        
        self.animacao_ativa = False

if __name__ == "__main__":
    root = tk.Tk()
    app = RecipientesGUI(root)
    root.mainloop()