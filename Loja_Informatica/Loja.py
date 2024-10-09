import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# Função para conectar ao banco de dados SQLite3
def conectar_banco():
    try:
        conexao = sqlite3.connect('lojainformatica.db')  # Cria um banco de dados local
        return conexao
    except sqlite3.Error as e:
        messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {e}")
        return None

# Função para criar a tabela "estoque" no banco de dados (caso não exista)
def criar_tabela():
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS estoque (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Produto TEXT NOT NULL,
        Preco REAL NOT NULL,
        Tipo TEXT NOT NULL
    )
    ''')
    
    conexao.commit()
    cursor.close()
    conexao.close()

# Função para verificar se o produto já está no banco
def produto_existe(conexao, produto):
    cursor = conexao.cursor()
    cursor.execute("SELECT 1 FROM estoque WHERE Produto = ?", (produto,))
    return cursor.fetchone() is not None

# Função para inserir dados na tabela estoque sem duplicação
def inserir_dados():
    conexao = conectar_banco()
    cursor = conexao.cursor()

    dados = [
        ("Intel i7", 1200.00, "Processador"),
        ("AMD Ryzen 5", 900.00, "Processador"),
        ("Memória Kingston 8GB", 300.00, "Memória RAM"),
        ("Memória Corsair 16GB", 600.00, "Memória RAM"),
        ("SSD Kingston 500GB", 350.00, "SSD"),
        ("Fonte Corsair 600W", 250.00, "Fonte"),
        ("Placa Mãe ASUS", 500.00, "Placa Mãe"),
        ("Placa de Vídeo Nvidia RTX 3060", 2500.00, "Placa de Vídeo"),
        ("Gabinete Cooler Master", 400.00, "Gabinete")
    ]

    for produto, preco, tipo in dados:
        if not produto_existe(conexao, produto):
            cursor.execute("INSERT INTO estoque (Produto, Preco, Tipo) VALUES (?, ?, ?)", (produto, preco, tipo))

    conexao.commit()
    cursor.close()
    conexao.close()


# Função para obter as opções do banco de dados SQLite3
def obter_opcoes(tipo):
    opcoes = {}
    try:
        conexao = conectar_banco()
        cursor = conexao.cursor()
        cursor.execute(f"SELECT ID, Produto, Preco FROM estoque WHERE Tipo = ?", (tipo,))
        rows = cursor.fetchall()
        
        for row in rows:
            id, produto, preco = row
            opcoes[id] = (produto, preco)
    except sqlite3.Error as e:
        messagebox.showerror("Erro", f"Erro ao consultar o banco de dados: {e}")
    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()
    return opcoes

# Função para selecionar um componente e mostrar no carrinho
def selecionar_componente(tree, tipo, carrinho_tree, carrinho):
    tree.delete(*tree.get_children())  # Limpar árvore de componentes
    opcoes = obter_opcoes(tipo)
    for id, valor in opcoes.items():
        tree.insert("", "end", values=(id, valor[0], f"R${valor[1]:.2f}"))

    def adicionar_item():
        selected_item = tree.selection()
        if selected_item:
            item = tree.item(selected_item, "values")
            descricao, preco = item[1], float(item[2][2:])  # Remove 'R$'
            carrinho.append((descricao, preco))
            carrinho_tree.insert("", "end", values=(descricao, f"R${preco:.2f}"))
        else:
            messagebox.showwarning("Atenção", "Selecione um item para adicionar ao carrinho.")

    # Botão de adicionar ao carrinho
    adicionar_btn = ttk.Button(janela, text="Adicionar ao Carrinho", command=adicionar_item)
    adicionar_btn.grid(row=3, column=1, padx=10, pady=10)

# Função para exibir o total do carrinho
def exibir_total(carrinho):
    total = sum([item[1] for item in carrinho])
    messagebox.showinfo("Total", f"Total do Carrinho: R${total:.2f}")

# Função para limpar o carrinho
def limpar_carrinho(carrinho_tree, carrinho):
    carrinho.clear()
    carrinho_tree.delete(*carrinho_tree.get_children())

# Configuração da janela principal
def criar_janela():
    global janela
    janela = tk.Tk()
    janela.title("Loja de Informática")
    
    # Lista de componentes disponíveis
    componentes = ["Processador", "Memória RAM", "SSD", "Fonte", "Placa Mãe", "Placa de Vídeo", "Gabinete"]
    tipo_var = tk.StringVar(value="Selecionar")

    # Frame de seleção de componentes
    frame_selecao = ttk.Frame(janela)
    frame_selecao.grid(row=0, column=0, padx=10, pady=10)

    ttk.Label(frame_selecao, text="Escolha o componente:").grid(row=0, column=0)

    tipo_combobox = ttk.Combobox(frame_selecao, textvariable=tipo_var, values=componentes, state="readonly")
    tipo_combobox.grid(row=0, column=1)

    # Treeview para exibir componentes
    tree = ttk.Treeview(frame_selecao, columns=("ID", "Produto", "Preço"), show="headings", height=6)
    tree.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
    tree.heading("ID", text="ID")
    tree.heading("Produto", text="Produto")
    tree.heading("Preço", text="Preço")
    
    # Frame para carrinho de compras
    frame_carrinho = ttk.Frame(janela)
    frame_carrinho.grid(row=0, column=1, padx=10, pady=10)

    ttk.Label(frame_carrinho, text="Carrinho de Compras:").grid(row=0, column=0)

    carrinho_tree = ttk.Treeview(frame_carrinho, columns=("Produto", "Preço"), show="headings", height=6)
    carrinho_tree.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
    carrinho_tree.heading("Produto", text="Produto")
    carrinho_tree.heading("Preço", text="Preço")

    carrinho = []

    # Botões para adicionar e limpar o carrinho
    selecionar_btn = ttk.Button(janela, text="Selecionar", command=lambda: selecionar_componente(tree, tipo_var.get(), carrinho_tree, carrinho))
    selecionar_btn.grid(row=2, column=0, padx=10, pady=10)

    limpar_btn = ttk.Button(janela, text="Limpar Carrinho", command=lambda: limpar_carrinho(carrinho_tree, carrinho))
    limpar_btn.grid(row=2, column=1, padx=10, pady=10)

    total_btn = ttk.Button(janela, text="Exibir Total", command=lambda: exibir_total(carrinho))
    total_btn.grid(row=3, column=0, padx=10, pady=10)

    janela.mainloop()

# Inicializar a aplicação, criar a tabela e inserir os dados
if __name__ == "__main__":
    criar_tabela()  # Certifique-se de que a tabela existe
    inserir_dados()  # Insere os dados no banco
    criar_janela()  # Inicia a interface gráfica
 