import pyodbc
import os
import platform
import time

dados_conexao = (
    "Driver={MySQL ODBC 9.0 Unicode Driver};"
    "Servidor=186.209.76.31:3306;"
    "Database=lojainformatica;"
    "USER=root;"
    "PASSWORD=admin;"
)

def obter_opcoes(tipo):
    opcoes = {}
    conexao = None
    cursor = None
    try:
        conexao = pyodbc.connect(dados_conexao)
        cursor = conexao.cursor()
        
        cursor.execute(f"""SELECT ID, Produto, Preco FROM estoque WHERE Tipo = '{tipo}'""")
        rows = cursor.fetchall()
        
        for row in rows:
            id = row.ID
            produto = row.Produto
            preco = row.Preco
            opcoes[id] = (produto, preco)

    except pyodbc.Error as e:
        print(f"Erro ao consultar o banco de dados: {e}")
    finally:
        if cursor is not None:
            cursor.close()
        if conexao is not None:
            conexao.close()
    
    return opcoes

def selecionar_componente(opcoes):
    for id, valor in opcoes.items():
        print(f"[{id}] - {valor[0]} - R${valor[1]:.2f}")
    modelo = int(input("Digite o modelo desejado: "))
    return opcoes.get(modelo, ("Modelo inválido", 0.0))

def mod_processador():
    opcoes = obter_opcoes('Processador')
    return selecionar_componente(opcoes)

def mod_memoria():
    opcoes = obter_opcoes('Memoria_Ram')
    return selecionar_componente(opcoes)

def mod_ssd():
    opcoes = obter_opcoes('SSD')
    return selecionar_componente(opcoes)

def mod_fonte():
    opcoes = obter_opcoes('Fonte')
    return selecionar_componente(opcoes)

def mod_placaMae():
    opcoes = obter_opcoes('Placa_Mae')
    return selecionar_componente(opcoes)

def mod_placaVideo():
    opcoes = obter_opcoes('Placa_Video')
    return selecionar_componente(opcoes)

def mod_gabinete():
    opcoes = obter_opcoes('Gabinete')
    return selecionar_componente(opcoes)

def limpar_tela():
    sistema = platform.system()
    if sistema == "Windows":
        os.system('cls')
    else:
        os.system('clear')

estoque = [
    "processador", 
    "memoriaRam",
    "ssd",
    "fonte",
    "placaMae",
    "placaVideo",
    "gabinete",
]

carrinho = []

print("\n!!!Olá, Seja Muito Bem-Vindo à Nossa Loja!!!\n\nVocê Deseja Realizar seu Pedido?")
realizar = int(input("\n[1] - Para Seguir com o pedido.\n[2] - Para Sair!\nDigite: "))

while realizar == 1:
    print(" ___________________________________")
    print("|[0] - Processador                  |")
    print("|[1] - Memória Ram                  |")
    print("|[2] - SSD                          |")
    print("|[3] - Fonte                        |")
    print("|[4] - Placa Mãe                    |")
    print("|[5] - Placa de Vídeo               |")
    print("|[6] - Gabinete                     |")
    print("|___________________________________|")

    try:
        pedido = int(input("Digite o número do componente desejado: "))
        
        if 0 <= pedido <= 6:
            if pedido == 0:
                descricao, preco = mod_processador()
            elif pedido == 1:
                descricao, preco = mod_memoria()
            elif pedido == 2:
                descricao, preco = mod_ssd()
            elif pedido == 3:
                descricao, preco = mod_fonte()
            elif pedido == 4:
                descricao, preco = mod_placaMae()
            elif pedido == 5:
                descricao, preco = mod_placaVideo()
            elif pedido == 6:
                descricao, preco = mod_gabinete()

            carrinho.append((estoque[pedido], descricao, preco))

        else:
            print("Número inválido. Por favor, escolha um número entre 0 e 6.")

        realizar = int(input("\nDigite 2 para sair ou 1 para continuar: "))

        time.sleep(0)
        limpar_tela()

    except ValueError:
        print("Entrada inválida. Por favor, digite um número inteiro.")

print("Seu Carrinho Contém:\n")
total = 0

for item in carrinho:
    componente, descricao, preco = item
    print(f"|{componente}: {descricao} - R${preco:.2f}")
    total += preco

print(f"\nTotal do Carrinho: R${total:.2f}")

print("Muito obrigado! Até logo.")