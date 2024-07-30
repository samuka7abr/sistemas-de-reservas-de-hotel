import datetime


quartos = {}
reservas = {}

def menu():
    print("\n--- Sistema de Reservas de Hotel ---")
    print("\n1. Adicionar quarto")
    print("2. Listar quartos disponíveis")
    print("3. Fazer reserva")
    print("4. Listar reservas ativas")
    print("5. Cancelar reserva")
    print("6. Calcular valor da reserva")
    print("7. Sair")
    escolha = input("Escolha uma opção: ")
    return escolha

def adicionar_quarto():
    numero = input("\nNúmero do quarto: ")
    tipo = input("Tipo do quarto (simples, duplo, suíte): ")
    preco = float(input("Preço por noite: "))
    quartos[numero] = {'tipo': tipo, 'preco': preco}
    print(f"\nQuarto {numero} adicionado com sucesso!")

def listar_quartos():
    if quartos:
        for numero, detalhes in quartos.items():
            print(f"\nNúmero: {numero}")
            print(f"Tipo: {detalhes['tipo']}")
            print(f"Preço por noite: R${detalhes['preco']:.2f}")
    else:
        print("\nNenhum quarto disponível.")

def fazer_reserva():
    nome = input("\nNome do cliente: ")
    numero_quarto = input("Número do quarto: ")
    if numero_quarto in quartos:
        check_in = input("Data de check-in (YYYY-MM-DD): ")
        check_out = input("Data de check-out (YYYY-MM-DD): ")
        check_in_date = datetime.datetime.strptime(check_in, "%Y-%m-%d")
        check_out_date = datetime.datetime.strptime(check_out, "%Y-%m-%d")
        if check_out_date > check_in_date:
            reservas[nome] = {'numero_quarto': numero_quarto, 'check_in': check_in_date, 'check_out': check_out_date}
            print(f"\nReserva para {nome} no quarto {numero_quarto} feita com sucesso!")
        else:
            print("\nData de check-out deve ser posterior à data de check-in.")
    else:
        print("\nQuarto não encontrado.")

def listar_reservas():
    if reservas:
        for nome, detalhes in reservas.items():
            print(f"\nNome do cliente: {nome}")
            print(f"Quarto: {detalhes['numero_quarto']}")
            print(f"Check-in: {detalhes['check_in'].strftime('%Y-%m-%d')}")
            print(f"Check-out: {detalhes['check_out'].strftime('%Y-%m-%d')}")
    else:
        print("\nNenhuma reserva ativa.")

def cancelar_reserva():
    nome = input("\nNome do cliente para cancelar a reserva: ")
    if nome in reservas:
        del reservas[nome]
        print(f"\nReserva de {nome} cancelada com sucesso!")
    else:
        print("\nReserva não encontrada.")

def calcular_valor_reserva():
    nome = input("\nNome do cliente: ")
    if nome in reservas:
        detalhes = reservas[nome]
        numero_quarto = detalhes['numero_quarto']
        preco_por_noite = quartos[numero_quarto]['preco']
        noites = (detalhes['check_out'] - detalhes['check_in']).days
        valor_total = noites * preco_por_noite
        print(f"\nValor total da reserva para {nome}: R${valor_total:.2f}")
    else:
        print("\nReserva não encontrada.")

def main():
    while True:
        escolha = menu()
        if escolha == '1':
            adicionar_quarto()
        elif escolha == '2':
            listar_quartos()
        elif escolha == '3':
            fazer_reserva()
        elif escolha == '4':
            listar_reservas()
        elif escolha == '5':
            cancelar_reserva()
        elif escolha == '6':
            calcular_valor_reserva()
        elif escolha == '7':
            print("Saindo...")
            break
        else:
            print("\nOpção inválida, tente novamente.")

if __name__ == "__main__":
    main()
