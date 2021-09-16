"""

"""

from sys import argv, stderr, exit
from os import abort, path, fork
from socket import getaddrinfo, socket
from socket import AF_INET, SOCK_STREAM, AI_ADDRCONFIG, AI_PASSIVE
from socket import IPPROTO_TCP, SOL_SOCKET, SO_REUSEADDR
from socket import gethostbyname
from socket import gaierror
import re
import time
from arquivo import EXTENSOES_CONHECIDAS, ARQUIVOS_DEFAULT, PAGINA_DE_ERRO_404, PORTA

def getEnderecoHost(porta):
    try:
        enderecoHost = getaddrinfo(
            None,
            porta,
            family=AF_INET,
            type=SOCK_STREAM,
            proto=IPPROTO_TCP,
            flags=AI_ADDRCONFIG | AI_PASSIVE)
    except:
        print("Não obtive informações sobre o servidor (???)", file=stderr)
        abort()
    return enderecoHost

def criaSocket(enderecoServidor):
    fd = socket(enderecoServidor[0][0], enderecoServidor[0][1])
    if not fd:
        print("Não consegui criar o socket")
        abort()
    return fd

def setModo(fd):
    fd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    return

def bindaSocket(fd, porta):
    try:
        fd.bind(('', porta))
    except:
        print("Erro ao dar bind no socket do servidor", porta, file=stderr)
        abort()
    return

def escuta(fd):
    try:
        fd.listen(1)
    except:
        print("Erro ao começar a escutar a porta", file=stderr)
        abort()
    print("Iniciando o serviço")
    return

def conecta(fd):
    (con, cliente) = fd.accept()
    print("Servidor conectado com", cliente)
    return con, cliente

def leRequisicao(buffer):
    """ Recebe buffer da requisição, faz o parse e, caso ok, retorna endereço para arquivo solicitado.
    
    Args:
        buffer: string com texto da requisição
    Returns:
        - None, caso haja erro na requisição ou caso não seja do tipo GET
        - caminho, versao, tipo_arquivo. três strings: caminho para o arquivo solicitado (caso seja
            vazio, será "/"), versão HTTP e tipo do arquivo, caso haja
    """

    if buffer[:3] == 'GET':
        comando_completo = buffer.split()
        caminho = comando_completo[1]
        versao = comando_completo[2]

        tipo_regex = re.compile(r'[^.]*$')
        procura_pattern = tipo_regex.search(caminho)
        tipo_arquivo = procura_pattern.group(0)
    else:
        print("Comando GET não encontrado")
        return None

    return caminho[1:], versao, tipo_arquivo

def encontraArquivo(caminho, tipo_arquivo):
    """ Recebe caminho para arquivo e retorna status code que será dado e caminho.

    Caso arquivo não tenha sido especificado, procura nos arquivos default. 
    Caso a extensão do arquivo seja desconhecida ou se não for encontrado, retorna arquivo 404.

    Args:
        caminho: string com o caminho para o arquivo desejado. Ex: "home/cursos/INF1407.html"
        tipo_arquivo:
    Returns:
        codigo_status, caminho, tipo_arquivo: inteiro correspondente à resposta ao GET (200 ou 404)
            e caminho para o arquivo que deverá ser passado para o cliente
    """

    if tipo_arquivo == "/":
        for arquivo_default in ARQUIVOS_DEFAULT:
            tipo_regex = re.compile(r'[^.]*$')
            procura_pattern = tipo_regex.search(arquivo_default)
            tipo_arquivo_default = procura_pattern.group(0)
            if path.isfile(arquivo_default) and EXTENSOES_CONHECIDAS.get(tipo_arquivo_default,0):
                return 200, arquivo_default, tipo_arquivo_default
        return 404, PAGINA_DE_ERRO_404, "html"
    elif not path.isfile(caminho) or (tipo_arquivo!= "/" and not EXTENSOES_CONHECIDAS.get(tipo_arquivo, 0)):
        return 404, PAGINA_DE_ERRO_404, "html"
    else:
        #TODO: trocar esse [1:]
        "/home.html"
        return 200, caminho, tipo_arquivo

def primeiraLinhaHeader(codigo_status):
    #TODO: cabeçalho
    if codigo_status == 200:
        return bytes("HTTP/1.1 200 OK\r\n", "utf-8")
    elif codigo_status == 404:
        return bytes("HTTP/1.1 404 Not Found\r\n", "utf-8")
    else:
        print("Erro: Resposta não conhecida", file=stderr)
        abort()

def segundaLinhaHeader(tipo_arquivo):
    #TODO: cabeçalho
    mime_type = EXTENSOES_CONHECIDAS.get(tipo_arquivo)
    return bytes(f"Content-Type: {mime_type}\r\n", "utf-8")

def terceiraLinhaHeader(caminho):
    #TODO: cabeçalho
    tamanho = path.getsize(caminho)
    return bytes(f"Content-Length: {tamanho}\r\n\r\n", "utf-8")

def montaResposta(codigo_status, tipo_arquivo, caminho):
    """ Monta bytearray com resposta que será dada ao cliente a partir dos argumentos recebidos.

    Args:
        codigo_status: inteiro correspondente à status code (200 ou 404)
        caminho: caminho para o arquivo que deverá ser passado para o cliente
    Returns:
        bytearray com resposta completa que será dada ao cliente, com status code, mensagem,
            tamanho do arquivo em bytes, etc.
    """
    #TODO: add mais coisa na header? nome do servidor, etc.
    header = primeiraLinhaHeader(codigo_status) + segundaLinhaHeader(tipo_arquivo) + terceiraLinhaHeader(caminho)
    with open(caminho, 'rb') as file:
        body = file.read()
    
    # PRA USAR O HARD CODED P TESTAR: DESCOMENTA AS PROXIMAS LINHAS E COMENTA AS DE CIMA
    #with open('templates/BioBd_LOGO_ORIGINAL.png', 'rb') as file:
    #    body = file.read()
    #header = "HTTP/1.1 200 OK\r\n" + "Content-Type: image/png\r\n" + "Content-Length: 852\r\n\r\n"
    #header = bytes(header, 'utf-8')
    return header + body

def fazTudo(fd):
    while True:
        buffer = fd.recv(1024).decode("utf-8")
        print("RECEBIDO: ", buffer)
        if not buffer:
            break
        try:
            caminho, versao, tipo_arquivo = leRequisicao(buffer)
        except TypeError:
            print("Requisição desconhecida")
            continue
        print(f"CAMINHO: {caminho}")
        codigo_status, caminho, tipo_arquivo = encontraArquivo(caminho, tipo_arquivo)
        texto_resposta = montaResposta(codigo_status, tipo_arquivo, caminho)
        print(texto_resposta)
        time.sleep(20)
        fd.send(texto_resposta)
    return

# def main():
#     if len(argv) == 2:
#         porta = int(argv[1])
#     else:
#         porta = 8752
#     enderecoHost = getEnderecoHost(porta)
#     fd = criaSocket(enderecoHost)
#     setModo(fd)
#     bindaSocket(fd, porta)
#     print("Servidor pronto em", enderecoHost)
#     escuta(fd)
#     while True:
#         con, cliente = conecta(fd)
#         if con == -1:
#             continue
#         fazTudo(con)
#     return

def main(): 
    if len(argv) == 2:
        porta = int(argv[1])
    else:
        porta = 8752
    enderecoHost = getEnderecoHost(porta)
    tcpSocket = criaSocket(enderecoHost)
    setModo(tcpSocket)
    bindaSocket(tcpSocket, porta)
    print("Servidor pronto em", enderecoHost)
    escuta(tcpSocket) 
    while(True):    
        con, cliente = conecta(tcpSocket)
        pid = fork() 
        if pid == 0:             
            tcpSocket.close() 
            print("Servidor connectado com ", cliente) 
            fazTudo(con)        
            print("Conexão terminada com ", cliente) 
            con.close() 
            exit()         
        else: 
            con.close() 
    return

if __name__ == '__main__':
    main()