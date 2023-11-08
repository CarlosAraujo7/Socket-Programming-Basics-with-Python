import socket

# Configurações do cliente
endereçoIP = '127.0.0.1'  # Endereço IP do servidor
porta = 12345       # Porta do servidor

# Função para enviar comandos ao servidor e receber respostas
def enviar_comando(comando):
    # Cria um socket para a comunicação com o servidor
    # AF_INET cria um socket com o protocolo IPv4
    # SOCK_STREAM permite que tanto o cliente e o servidor possam enviar e receber dados
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
        try:
            # Tenta conectar ao servidor usando o endereço e porta especificados
            cliente.connect((endereçoIP, porta))
            
            # Envia o comando ao servidor codificado em bytes
            cliente.sendall(comando.encode())
            
            # Recebe a resposta do servidor (até 1024 bytes) e decodifica para uma string
            resposta = cliente.recv(1024).decode()
            
            # Retorna a resposta do servidor
            return resposta
        except ConnectionRefusedError:
            # Trata o erro se a conexão for recusada (servidor não está disponível)
            return "Erro de conexão: O servidor não está disponível."
        except Exception as erros:
            # Trata outros erros e mostra eles na resposta
            return f"Erro inesperado: {erros}"

# Função para exibir o menu de comandos e receber a escolha do usuário
def menu_comandos():
    print("Opções de Comando:")
    print("1. CONSULTA")
    print("2. HORA")
    print("3. ARQUIVO <nome>")
    print("4. LISTAR")
    print("5. SAIR")
    escolha = input("Escolha um comando ([1], [2], [3], [4] ou [5]): ").strip()
    return escolha

# Menu de comandos disponíveis para o cliente
while True:
    escolha = menu_comandos()

    if escolha == "1":
        comando = "CONSULTA"
    elif escolha == "2":
        comando = "HORA"
    elif escolha.startswith("3"):
        nome_arquivo = input("Digite o nome do arquivo: ").strip()
        comando = f"ARQUIVO {nome_arquivo}"
    elif escolha == "4":
        comando = "LISTAR"
    elif escolha == "5":
        comando = "SAIR"
    else:
        print("Comando inválido. Tente novamente.")
        continue

    resposta = enviar_comando(comando)
    print(f"Resposta do servidor: {resposta}")

    if resposta == "ADEUS":
        # Encerra o loop se a resposta do servidor for "ADEUS"
        break
