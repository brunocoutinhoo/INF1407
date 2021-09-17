""" Módulo principal do servidor web.

Deve ser executado em ambiente linux. Caso queira especificar uma porta diferente
da que está no arquivo de configuração (arquivo.py), execute este arquivo passando
como único argumento o número da porta. Caso contrário, execute sem argumentos adicionais.
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
from arquivo import EXTENSOES_CONHECIDAS, ARQUIVOS_DEFAULT, PAGINA_DE_ERRO_404, PORTA,\
     DIRETORIO_FISICO, DELAY

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

def getExtensaoArquivo(caminho):
    """Recebe caminho para um arquivo e retorna string com sua extensão."""

    tipo_regex = re.compile(r'[^.]*$')    #Regex que identifica apenas caracteres após o ponto.
    procura_pattern = tipo_regex.search(caminho) #O Regex é utilizado no caminho no arquivo para identificar a extensão do mesmo.
    return procura_pattern.group(0)

def leRequisicao(buffer):
    """ Recebe buffer da requisição, faz o parse e, caso ok, retorna endereço para arquivo solicitado.
    
    Args:
        buffer: string com texto da requisição
    Returns:
        - None, caso haja erro na requisição ou caso não seja do tipo GET
        - caminho, versao, tipo_arquivo. três strings: caminho para o arquivo solicitado (caso seja
            vazio, será "/"), versão HTTP e tipo do arquivo, caso haja
    """

    # Lê a string da requisição GET e divide cada informação relevante da primeira linha (Caminho do arquivo, versão e extensão do arquivo).
    if buffer[:3] == 'GET':
        comando_completo = buffer.split()
        caminho = comando_completo[1]
        versao = comando_completo[2]
        tipo_arquivo = getExtensaoArquivo(caminho)
    else:
        print("Comando GET não encontrado")
        return None
    # adiciona diretório local antes do caminho fornecido
    caminho = DIRETORIO_FISICO + caminho[1:]
    return caminho, versao, tipo_arquivo

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

    # se caminho passado for um diretório, procura nos arquivos default
    if path.isdir(caminho):
        for arquivo_default in ARQUIVOS_DEFAULT:
            arquivo_default = DIRETORIO_FISICO + arquivo_default
            tipo_arquivo_default = getExtensaoArquivo(arquivo_default)
            # se arquivo default for válido, retorna ele
            if path.isfile(arquivo_default) and EXTENSOES_CONHECIDAS.get(tipo_arquivo_default, 0):
                return 200, arquivo_default, tipo_arquivo_default
        # se nenhum arquivo default for válido, retorna 404
        return 404, PAGINA_DE_ERRO_404, "html"
    # se caminho e tipo arquivo ok
    elif path.isfile(caminho) and EXTENSOES_CONHECIDAS.get(tipo_arquivo, 0):
        return 200, caminho, tipo_arquivo
    else:
        arquivo_erro = DIRETORIO_FISICO + PAGINA_DE_ERRO_404
        return 404, arquivo_erro, getExtensaoArquivo(arquivo_erro)

def primeiraLinhaHeader(codigo_status):
    """Retorna a primeira linha do header no formato bytes de acordo com código."""

    if codigo_status == 200:
        return bytes("HTTP/1.1 200 OK\r\n", "utf-8")
    elif codigo_status == 404:
        return bytes("HTTP/1.1 404 Not Found\r\n", "utf-8")
    else:
        print("Erro: Resposta não conhecida", file=stderr)
        abort()

def segundaLinhaHeader(tipo_arquivo):
    """Retorna linha Content-Type do header no formato bytes de acordo com tipo do arquivo."""
    
    # obs: já foi conferido antes que o tipo do arquivo está nas extensões conhecidas
    mime_type = EXTENSOES_CONHECIDAS.get(tipo_arquivo)
    return bytes(f"Content-Type: {mime_type}\r\n", "utf-8")

def terceiraLinhaHeader(caminho):
    """Retorna linha Content-Length do header no formato bytes de acordo com tamanho do arquivo."""

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

    header = primeiraLinhaHeader(codigo_status) + segundaLinhaHeader(tipo_arquivo) +\
        terceiraLinhaHeader(caminho)
    with open(caminho, 'rb') as file:
        body = file.read()
    return header + body

def fazTudo(fd):
    while True:
        buffer = fd.recv(1024).decode("utf-8")
        print(buffer)
        if not buffer:
            break
        try:
            caminho, versao, tipo_arquivo = leRequisicao(buffer)
        except TypeError:
            print("Requisição desconhecida")
            continue
        codigo_status, caminho, tipo_arquivo = encontraArquivo(caminho, tipo_arquivo)
        texto_resposta = montaResposta(codigo_status, tipo_arquivo, caminho)
        time.sleep(DELAY)
        print(f"Resposta enviada: {texto_resposta}")
        fd.send(texto_resposta)
    return

def confere_configuracao():
    """Critica variáveis do arquivo de configuração. Em caso de erro, aborta."""

    try: EXTENSOES_CONHECIDAS and ARQUIVOS_DEFAULT and PAGINA_DE_ERRO_404 and PORTA and \
         DIRETORIO_FISICO and DELAY
    except NameError:
        print("Erro: variável de configuração não encontrada", file=stderr)
        abort()
    if type(ARQUIVOS_DEFAULT) != list:
        print("Erro: lista de arquivos default deve ser do tipo lista", file=stderr)
        abort()
    if type(PORTA) != int or PORTA < 0:
        print("Erro: porta deve ser inteiro positivo", file=stderr)
        abort()
    if (not path.isdir(DIRETORIO_FISICO)) or (DIRETORIO_FISICO[-1:] != '/'):
        print("Erro: diretório físico deve ser diretório válido terminado em '/'", file=stderr)
        abort()
    extensao_pag_erro = getExtensaoArquivo(DIRETORIO_FISICO + PAGINA_DE_ERRO_404)
    if (not path.isfile(PAGINA_DE_ERRO_404)) or not EXTENSOES_CONHECIDAS.get(extensao_pag_erro, 0):
        print("Erro: página 404 deve ser um arquivo válido", file=stderr)
        abort()
    if type(EXTENSOES_CONHECIDAS) != dict:
        print("Erro: lista de extensões conhecidas deve ser do tipo dict", file=stderr)
        abort()
    if (type(DELAY) != int and type(DELAY) != float) or DELAY < 0:
        print("Erro: delay deve ser número positivo (se quiser que não haja delay, coloque 0)", file=stderr)
        abort()
    return

def main():
    confere_configuracao()
    if len(argv) == 2:
        porta = int(argv[1])
    else:
        porta = PORTA
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