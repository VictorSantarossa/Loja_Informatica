def entrada1():
    while True:  
        entrada = input("Digite o primeiro valor: ")
        try:
            num = float(entrada)
            return num
        except ValueError:
            print("Erro: valor inválido. Por favor, digite um número válido.")

def entrada2():
    while True:
        entrada = input("Digite o segundo valor: ")
        try:
            num = float(entrada)
            return num
        except ValueError:
            print("Erro: valor inválido. Por favor, digite um número válido.")

def calcular(num1, num2, operacao):
    if operacao == "1":
        return num1 + num2
    elif operacao == "2":
        return num1 - num2
    elif operacao == "3":
        if num2 == 0:
            return "Erro: divisão por zero."
        return num1 / num2
    elif operacao == "4":
        return num1 * num2
    else:
        return "Operação inválida."

num1 = entrada1()
num2 = entrada2()

calculo = input("Digite 1 = +"
                "\nDigite 2 = -"
                "\nDigite 3 = /"
                "\nDigite 4 = *"
                "\nSelecione qual o cálculo que deseja: ")

resultado = calcular(num1, num2, calculo)
print(f"O cálculo entre {num1} e {num2} é: {resultado}")