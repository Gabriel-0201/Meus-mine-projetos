from customtkinter import *

class Interface:
    def __init__(self, largura, altura, titulo, comando_gerar):
        set_appearance_mode("dark") # Tema escuro como na imagem
        self.largura = largura
        self.altura = altura
        self.comando_gerer = comando_gerar
        
        self.janela = CTk()
        self.janela.title(titulo)
        self.centralizar()

        # --- Divisão em Colunas ---
        self.janela.grid_columnconfigure(0, weight=2) # Coluna da esquerda (mais larga)
        self.janela.grid_columnconfigure(1, weight=1) # Coluna da direita

        self.adicionar_widgets()

    def centralizar(self):
        largura_tela = self.janela.winfo_screenwidth()
        altura_tela = self.janela.winfo_screenheight()
        pos_x = (largura_tela // 2) - (self.largura // 2)
        pos_y = (altura_tela // 2) - (self.altura // 2)
        self.janela.geometry(f"{self.largura}x{self.altura}+{pos_x}+{pos_y}")

    def atualizar_label_slide_pro(self, valor):
        self.valor_pro.configure(text=f"Criatividade (Pró): {valor:.2f}")

    def atualizar_label_slide_contra(self, valor):
        self.valor_contra.configure(text=f"Criatividade (Contra): {valor:.2f}")

    def ao_clicar(self): 
        dados = {
            "tema": self.txt_tema.get("1.0", "end-1c"),
            "nucleo": self.ent_Keywords.get(),
            "perspectiva": self.var_perspectiva.get(),
            "temp_pro": self.slider_pro.get(),
            "temp_contra": self.slider_contra.get()
        }

        # Desativa o botão temporariamente para não clicar duas vezes
        self.btn_gerar.configure(state="disabled", text="Processando...")
        #envia os dados
        self.comando_gerer(dados)
        #reativa o botão
        self.btn_gerar.configure(state="normal", text="Gerar Debate")

    def adicionar_widgets(self):
        # --- COLUNA ESQUERDA (Geral) ---
        frame_esq = CTkFrame(self.janela, fg_color="transparent")
        frame_esq.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        CTkLabel(frame_esq, text="Geral", font=("Arial", 20, "bold")).pack(anchor="w", pady=(0, 10))
        
        # Tema do Debate
        CTkLabel(frame_esq, text="Tema do Debate").pack(anchor="w")
        self.txt_tema = CTkTextbox(frame_esq, height=100)
        self.txt_tema.pack(fill="x", pady=(0, 10))

        # Palavras-chave
        CTkLabel(frame_esq, text="Núcleo / Palavra-chave").pack(anchor="w")
        self.ent_Keywords = CTkEntry(frame_esq, placeholder_text="Ex: ética no jornalismo...")
        self.ent_Keywords.pack(fill="x", pady=(0, 10))

        # Nível de Tokens
        CTkLabel(frame_esq, text="Nível de Tokens / Perspectiva").pack(anchor="w", pady=(10, 0))
        
        # Variável que armazena qual opção está selecionada
        self.var_perspectiva = StringVar(value="Moderado") 

        self.tok_button = CTkSegmentedButton(frame_esq, 
                                            values=["Direto", "Moderado", "Palestrante"],
                                            variable=self.var_perspectiva)
        self.tok_button.pack(fill="both", expand= True, pady=(5, 10))

        # --- COLUNA DIREITA (Cofigurações Dos Debatentes) ---
        frame_dir = CTkFrame(self.janela, fg_color="transparent")
        frame_dir.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        CTkLabel(frame_dir, text="Cofigurações Dos Debatentes", font=("Arial", 20, "bold")).pack(anchor="w", pady=(0, 10))

        # Slider de Temperatura
        self.valor_pro = CTkLabel(frame_dir, text="Criatividade (Pró): 0.50")
        self.valor_pro.pack(anchor="w")
        self.slider_pro = CTkSlider(frame_dir, from_=0.1, to=1.0,
                                    command= self.atualizar_label_slide_pro)
        self.slider_pro.set(0.5) # Define valor inicial no slider
        self.slider_pro.pack(fill="x", pady=6)

        self.valor_contra = CTkLabel(frame_dir, text="Criatividade (Contra): 0.50")
        self.valor_contra.pack(anchor="w")
        
        self.slider_contra = CTkSlider(frame_dir, from_=0.1, to=1.0, 
                                    command=self.atualizar_label_slide_contra)
        self.slider_contra.set(0.5)
        self.slider_contra.pack(fill="x", pady=6)

        # --- BOTÃO GERAR ---
        self.btn_gerar = CTkButton(self.janela, 
                           text="Gerar Debate",
                           command= self.ao_clicar, #chama a função interna

                           fg_color="#040507",    # Azul Escuro (Base)
                           hover_color="#3b82f6", # Azul Claro (Brilho ao passar o mouse)
                           height=40, 
                           font=("Arial", 14, "bold"),
                           border_width=2,
                           border_color="#3b82f6") # Borda clara para dar profundidade
        self.btn_gerar.grid(row=1, column=1, padx=20, pady=40, sticky="ew")

    def rodar(self):
        self.janela.mainloop()