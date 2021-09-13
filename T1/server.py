"""

"""

from sys import argv, stderr
from os import abort
from socket import getaddrinfo, socket
from socket import AF_INET, SOCK_STREAM, AI_ADDRCONFIG, AI_PASSIVE
from socket import IPPROTO_TCP, SOL_SOCKET, SO_REUSEADDR
from socket import gethostbyname
from socket import gaierror

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
        fd.listen(0)
    except:
        print("Erro ao começar a escutar a porta", file=stderr)
        abort()
    print("Iniciando o serviço")
    return

def conecta(fd):
    (con, cliente) = fd.accept()
    print("Servidor conectado com", cliente)
    return con

def leRequisicao(buffer):
    """ Recebe buffer da requisição, faz o parse e, caso ok, retorna endereço para arquivo solicitado.
    
    Args:
        buffer: string com texto da requisição
    Returns:
        0, caso haja erro na requisição ou caso não seja do tipo GET
        string com caminho para arquivo.
    """
    return "exemplo_hard_coded.html"

def encontraArquivo(caminho):
    """ Recebe caminho para arquivo e retorna status code que será dado e caminho.

    Caso não encontre arquivo com o nome especificado, procura nos arquivos default. 
    Por último, se não conseguir, retorna arquivo 404.

    Args:
        caminho: string com o caminho para o arquivo desejado. Ex: "home/cursos/INF1407.html"
    Returns:
        codigo_status, caminho: inteiro correspondente à resposta ao GET (200 ou 404)
            e caminho para o arquivo que deverá ser passado para o cliente
    """
    return 200, "exemplo_hard_coded.html"
    pass

def montaResposta(codigo_status, caminho):
    """ Monta bytearray com resposta que será dada ao cliente a partir dos argumentos recebidos.

    Args:
        codigo_status: inteiro correspondente à status code (200 ou 404)
        caminho: caminho para o arquivo que deverá ser passado para o cliente
    Returns:
        bytearray com resposta completa que será dada ao cliente, com status code, mensagem,
            tamanho do arquivo em bytes, etc.
    """

    # obs: tem que contar o tamanho do arquivo em bytes para passar na resposta também.
    buffer_hard_coded = """HTTP/1.1 200 OK
                Content-Type: text/html
                Content-Length: 111

                <html><body>
                <h2>No Host: header received</h2>
                HTTP 1.1 requests must include the Host: header.
                </body></html>"""
    
    # p/ montar de vdd depois:
    #with open('home.html', 'r') as file:
    #   data = bytearray(file.read(), 'utf-8')
    # alem disso, bytearrays podem ser concatenados usando '+'. exemplo:
    # ex1 = bytearray("abc", "utf-8") + bytearray("def", "utf-8")
    # ex1 = bytearray(b'abcdef')
    
    return bytearray(buffer_hard_coded, 'utf-8')

def fazTudo(fd):
    while True:
        buffer = fd.recv(1024).decode("utf-8")
        if not buffer:
            break
        endereco = leRequisicao(buffer)
        if endereco:
            codigo_status, caminho = encontraArquivo(endereco)
            texto_resposta = montaResposta(codigo_status, caminho)
        else:
            pass
        print(texto_resposta)
        fd.send(texto_resposta)

    print("Conexão terminada com", fd)
    fd.close()
    return

def main():
    if len(argv) == 2:
        porta = int(argv[1])
    else:
        porta = 8752
    enderecoHost = getEnderecoHost(porta)
    fd = criaSocket(enderecoHost)
    setModo(fd)
    bindaSocket(fd, porta)
    print("Servidor pronto em", enderecoHost)
    escuta(fd)
    while True:
        con = conecta(fd)
        if con == -1:
            continue
        fazTudo(con)
    return

if __name__ == '__main__':
    main()