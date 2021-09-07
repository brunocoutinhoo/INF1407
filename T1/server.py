from sys import argv, stderr
from posix import abort
from socket import getaddrinfo, socket
from socket import AF_INET, SOCK_STREAM, AI_ADDRCONFIG, AI_PASSIVE
from socket import IPPROTO_TCP, SOL_SOCKET, SO_REUSEADDR
from socket import gethostbyname
from socket import gaierror

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

def fazTudo(fd):
    while True:
        buffer = fd.recv(1024).decode("utf-8")
        if not buffer:
            break
        print('==>', buffer)
        fd.send(bytearray(buffer, 'utf-8'))
    print("Conexão terminada com", fd)
    fd.close()
    return

if __name__ == '__main__':
    main()