import socket
import os
import threading
from datetime import datetime
from shutil import copyfile

# Configurações do servidor
endereçoIP = '127.0.0.1'  # Endereço IP do servidor
porta = 12345        # Porta para conexão
clientes_limite = 5     # Número máximo de clientes que o servidor pode atender

# Função para processar comandos do cliente
def comando(cliente):
    with cliente:
        try:
            # Exibe uma mensagem de conexão bem-sucedida
            print(f"Conexão estabelecida com {cliente.getpeername()}")
            while True:
                # Recebe dados do cliente (1024 bytes por vez) e decodifica
                data = cliente.recv(1024).decode()
                if not data:
                    break
                # Processa o comando do cliente e recebe uma resposta
                resposta = comando_individual(data)
                # Envia a resposta de volta ao cliente depois de codificar
                cliente.send(resposta.encode())
        except ConnectionResetError:
            # Lidando com uma desconexão abrupta do cliente
            print(f"Conexão encerrada abruptamente com {cliente.getpeername()}")
        except Exception as erro:
            # Lidando com erros inesperados durante a conexão com o cliente
            print(f"Erro inesperado com {cliente.getpeername()}: {erro}")
        finally:
            # Exibe uma mensagem quando a conexão é encerrada
            print(f"Conexão encerrada com {cliente.getpeername()}")

def comando_individual(comando):
    if comando == "CONSULTA":
        return "Esse é um servidor feito com muito esforço e choradeira. Aproveite todas as funcionalidades dele se divirta! <3"
    elif comando == "HORA":
        # Pega a hora atual e a formata a saída
        hora_atual = datetime.now().strftime("%H:%M:%S")
        return f"HORA_ATUAL {hora_atual}"
    elif comando.startswith("ARQUIVO "):
        _, nome_arquivo = comando.split(" ", 1)
        try:
            # Tenta abrir o arquivo e ler o conteúdo
            with open(nome_arquivo, 'r') as arquivo:
                conteudo = arquivo.read()
                copyfile(nome_arquivo, f"//home//carlos//Documentos//Python//Trabalho//Cliente//{nome_arquivo}")
                return f"ARQUIVO {nome_arquivo} {conteudo}"
            # Lida com o caso em que o arquivo não é encontrado
            return "ARQUIVO_NAO_ENCONTRADO"
        except Exception as erro:
            # Lida com outros erros ao manipular o arquivo
            return f"ERRO {erro}"
    elif comando == "LISTAR":
        try:
            # Pega uma lista de arquivos disponíveis no diretório atual
            arquivos_disponiveis = " ".join(os.listdir())
            return f"LISTA_ARQUIVOS {arquivos_disponiveis}"
        except Exception as erro:
            # Lida com erros ao obter a lista de arquivos
            return f"ERRO {erro}"
    elif comando == "SAIR":
        return "ADEUS"
    else:
        # Resposta para comandos desconhecidos
        return "COMANDO_DESCONHECIDO"

# Configuração do socket do servidor
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
    servidor.bind((endereçoIP, porta))
    servidor.listen()
    # Exibe uma mensagem indicando que o servidor está ouvindo
    print(f"Servidor ouvindo em {endereçoIP}:{porta}")

    while True:
        try:
            # Aceita uma nova conexão de cliente
            cliente, endereço_cliente = servidor.accept()
            # Inicia uma nova thread para processar a conexão do cliente
            threading.Thread(target=comando, args=(cliente,)).start()
        except Exception as erro:
            # Lidando com erros ao aceitar conexões
            print(f"Erro ao aceitar conexão: {erro}")
