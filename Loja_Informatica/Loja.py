import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

# Conectar ao banco de dados SQLite
def conectar_banco():
    try:
        conexao = sqlite3.connect('lojainformatica.db')
        return conexao
    except sqlite3.Error as e:
        messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {e}")
        return None

# Criar tabela "estoque" no banco de dados
def criar_tabela():
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS estoque (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Produto TEXT NOT NULL UNIQUE,
        Preco REAL NOT NULL,
        Tipo TEXT NOT NULL,
        Quantidade INTEGER NOT NULL
    )''')
    conexao.commit()
    cursor.close()
    conexao.close()

# Inserir produtos no banco de dados
def inserir_dados():
    conexao = conectar_banco()
    cursor = conexao.cursor()
    produtos = [
        # Processadores
        ("Intel i9-13900K", 2800.00, "Processador", 5),
        ("AMD Ryzen 9 7900X", 3200.00, "Processador", 4),
        ("Intel i7-12700K", 1600.00, "Processador", 8),
        ("AMD Ryzen 7 5800X", 1500.00, "Processador", 10),
        # Placas Mãe
        ("ASUS ROG Strix Z790-E", 1200.00, "Placa Mãe", 6),
        ("MSI MPG B550 Gaming Edge", 700.00, "Placa Mãe", 7),
        ("Gigabyte Z690 AORUS", 1400.00, "Placa Mãe", 4),
        ("ASRock B450M Pro4", 400.00, "Placa Mãe", 12),
        # Memórias RAM
        ("Corsair Vengeance LPX 16GB (2x8GB)", 500.00, "Memória RAM", 20),
        ("G.Skill Trident Z Royal 32GB (2x16GB)", 1200.00, "Memória RAM", 10),
        ("Kingston HyperX Fury 8GB", 300.00, "Memória RAM", 25),
        ("Corsair Vengeance DDR4 64GB (4x16GB)", 2500.00, "Memória RAM", 3),
        # SSDs
        ("Samsung 980 PRO 1TB", 800.00, "SSD", 15),
        ("WD Black SN850X 1TB", 700.00, "SSD", 18),
        ("Crucial P5 Plus 500GB", 350.00, "SSD", 25),
        ("Kingston A2000 500GB", 300.00, "SSD", 30),
        # Placas de Vídeo
        ("NVIDIA RTX 4090", 12000.00, "Placa de Vídeo", 3),
        ("AMD Radeon RX 7900XTX", 11000.00, "Placa de Vídeo", 4),
        ("NVIDIA RTX 3080 Ti", 7500.00, "Placa de Vídeo", 8),
        ("NVIDIA GTX 1660 Super", 2200.00, "Placa de Vídeo", 12),
        # Fontes de Alimentação
        ("Corsair RM850x 850W", 650.00, "Fonte", 10),
        ("Cooler Master MWE Gold 650W", 400.00, "Fonte", 15),
        ("EVGA SuperNOVA 1000 G5", 1200.00, "Fonte", 5),
        ("Seasonic FOCUS GX 750W", 700.00, "Fonte", 8),
        # Gabinetes
        ("NZXT H510 Elite", 800.00, "Gabinete", 12),
        ("Cooler Master MasterBox Q300L", 350.00, "Gabinete", 18),
        ("Phanteks Eclipse P400A", 500.00, "Gabinete", 20),
        ("Corsair iCUE 4000X", 650.00, "Gabinete", 10)
    ]
    for produto, preco, tipo, quantidade in produtos:
        cursor.execute("SELECT 1 FROM estoque WHERE Produto = ?", (produto,))
        if not cursor.fetchone():  # Produto não existe
            cursor.execute("INSERT INTO estoque (Produto, Preco, Tipo, Quantidade) VALUES (?, ?, ?, ?)", 
                           (produto, preco, tipo, quantidade))
    conexao.commit()
    cursor.close()
    conexao.close()

# Obter componentes de um tipo específico
def obter_componentes(tipo):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("SELECT ID, Produto, Preco, Quantidade FROM estoque WHERE Tipo = ?", (tipo,))
    componentes = cursor.fetchall()
    cursor.close()
    conexao.close()
    return componentes

# Adicionar produto ao carrinho
def adicionar_ao_carrinho(tree, carrinho_tree, carrinho):
    selecionado = tree.selection()
    if not selecionado:
        messagebox.showwarning("Atenção", "Selecione um item para adicionar ao carrinho.")
        return
    item = tree.item(selecionado, "values")
    produto_id, descricao, preco, quantidade_estoque = int(item[0]), item[1], float(item[2][2:]), int(item[3])

    # Solicitar quantidade ao usuário
    quantidade_str = simpledialog.askstring("Quantidade", f"Digite a quantidade para '{descricao}' (Máx: {quantidade_estoque}):")
    if not quantidade_str or not quantidade_str.isdigit():
        messagebox.showerror("Erro", "Quantidade inválida.")
        return
    quantidade = int(quantidade_str)

    # Verificar se a quantidade solicitada é válida
    if quantidade > quantidade_estoque or quantidade <= 0:
        messagebox.showerror("Erro", "Quantidade excede o estoque ou é inválida.")
        return

    # Verificar se o carrinho já possui o produto, para garantir que não exceda o estoque
    quantidade_no_carrinho = sum([item[3] for item in carrinho if item[0] == produto_id])
    if quantidade_no_carrinho + quantidade > quantidade_estoque:
        messagebox.showerror("Erro", f"A quantidade solicitada para '{descricao}' excede o estoque disponível.")
        return

    # Adicionar ao carrinho
    carrinho.append((produto_id, descricao, preco, quantidade))
    carrinho_tree.insert("", "end", values=(descricao, f"R${preco:.2f}", quantidade))

# Finalizar compra
def finalizar_compra(carrinho_tree, carrinho):
    if not carrinho:
        messagebox.showwarning("Carrinho Vazio", "Adicione itens ao carrinho antes de finalizar a compra.")
        return

    conexao = conectar_banco()
    cursor = conexao.cursor()

    for produto_id, descricao, preco, quantidade_carrinho in carrinho:
        cursor.execute("SELECT Quantidade FROM estoque WHERE ID = ?", (produto_id,))
        estoque_disponivel = cursor.fetchone()
        if not estoque_disponivel or estoque_disponivel[0] < quantidade_carrinho:
            messagebox.showerror(
                "Erro de Estoque",
                f"O produto '{descricao}' tem apenas {estoque_disponivel[0]} unidade(s) disponível(is) no estoque, "
                f"mas você adicionou {quantidade_carrinho} ao carrinho."
            )
            conexao.rollback()
            cursor.close()
            conexao.close()
            return

    # Atualizar o estoque no banco
    for produto_id, descricao, preco, quantidade_carrinho in carrinho:
        cursor.execute("UPDATE estoque SET Quantidade = Quantidade - ? WHERE ID = ?", (quantidade_carrinho, produto_id))

    conexao.commit()
    cursor.close()
    conexao.close()

    # Limpar o carrinho
    carrinho.clear()
    carrinho_tree.delete(*carrinho_tree.get_children())
    messagebox.showinfo("Compra Finalizada", "Compra realizada com sucesso!")

# Limpar carrinho
def limpar_carrinho(carrinho_tree, carrinho):
    carrinho.clear()
    carrinho_tree.delete(*carrinho_tree.get_children())

# Interface gráfica
def criar_janela():
    janela = tk.Tk()
    janela.title("Loja de Informática")
    
    # Definindo o tema escuro total
    janela.tk_setPalette(background='#1c1c1c', foreground='white')

    # Estilo do ttk com tema escuro
    style = ttk.Style()
    style.configure("TButton",
                    font=("Arial", 12),
                    padding=10,
                    relief="flat",
                    background="#444444",
                    foreground="black",  # Texto preto
                    focuscolor="none")
    style.configure("TCombobox",
                    font=("Arial", 12),
                    fieldbackground="#444444",
                    background="#444444",
                    foreground="black")  # Texto preto
    style.configure("TTreeview",
                    font=("Arial", 12),
                    background="#444444",
                    foreground="black",  # Texto preto
                    rowheight=25,
                    fieldbackground="#444444",
                    selectbackground="#555555",
                    selectforeground="white")
    style.configure("TLabel",
                    font=("Arial", 14),
                    foreground="black")  # Texto preto
    
    # Frame de seleção de produtos
    frame_selecao = ttk.Frame(janela, padding=10)
    frame_selecao.grid(row=0, column=0, padx=10, pady=10)

    tipo_var = tk.StringVar(value="Selecionar")
    componentes = ["Processador", "Placa Mãe", "Memória RAM", "SSD", "Placa de Vídeo", "Fonte", "Gabinete"]

    ttk.Label(frame_selecao, text="Tipo de Produto:").grid(row=0, column=0, sticky="w", pady=5)
    tipo_combobox = ttk.Combobox(frame_selecao, textvariable=tipo_var, values=componentes, state="readonly", width=20)
    tipo_combobox.grid(row=0, column=1, pady=5)

    tree = ttk.Treeview(frame_selecao, columns=("ID", "Produto", "Preço", "Quantidade"), show="headings", height=8)
    tree.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
    for col in ("ID", "Produto", "Preço", "Quantidade"):
        tree.heading(col, text=col)

    def atualizar_tree():
        tree.delete(*tree.get_children())
        tipo = tipo_var.get()
        if tipo:
            componentes = obter_componentes(tipo)
            for id, produto, preco, quantidade in componentes:
                tree.insert("", "end", values=(id, produto, f"R${preco:.2f}", quantidade))

    tipo_combobox.bind("<<ComboboxSelected>>", lambda e: atualizar_tree())

    # Frame do carrinho
    frame_carrinho = ttk.Frame(janela, padding=10)
    frame_carrinho.grid(row=0, column=1, padx=10, pady=10)

    ttk.Label(frame_carrinho, text="Carrinho:").grid(row=0, column=0, sticky="w", pady=5)

    carrinho_tree = ttk.Treeview(frame_carrinho, columns=("Produto", "Preço", "Quantidade"), show="headings", height=8)
    carrinho_tree.grid(row=1, column=0, padx=10, pady=10)
    for col in ("Produto", "Preço", "Quantidade"):
        carrinho_tree.heading(col, text=col)

    carrinho = []

    # Botões
    adicionar_btn = ttk.Button(janela, text="Adicionar ao Carrinho", command=lambda: adicionar_ao_carrinho(tree, carrinho_tree, carrinho))
    adicionar_btn.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    limpar_btn = ttk.Button(janela, text="Limpar Carrinho", command=lambda: limpar_carrinho(carrinho_tree, carrinho))
    limpar_btn.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

    finalizar_btn = ttk.Button(janela, text="Finalizar Compra", command=lambda: finalizar_compra(carrinho_tree, carrinho))
    finalizar_btn.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

    janela.mainloop()

# Inicializar aplicação
if __name__ == "__main__":
    criar_tabela()
    inserir_dados()
    criar_janela()
