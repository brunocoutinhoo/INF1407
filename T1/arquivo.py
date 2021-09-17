"""Arquivo de configuração do servidor. Possui 6 variáveis:
ARQUIVOS_DEFAULT, PORTA, DIRETORIO_FISICO, PAGINA_DE_ERRO_404 e
EXTENSOES_CONHECIDAS, DELAY
"""


#Insira aqui a lista de arquivos que deverá ser consultada caso
#não seja fornecido um caminho para arquivo. Essa lista será consultada
#em ordem.
ARQUIVOS_DEFAULT = [
    "home.html",
    "index.html",
    "default.html",
    "home.htm",
    "index.htm",
    "default.htm",
]

#Seleciona a porta do Servidor. Deve ser inteiro positivo.
PORTA = 8080

#Diretório físico da máquina local onde se encontram os arquivos publicados na web.
#ATENÇÂO: deve terminar em '/'. Exemplo:
#DIRETORIO_FISICO = "C:/Users/nome/Documents/Trabalhos/INF1407/T1/"
DIRETORIO_FISICO = ""

#Arquivo referente à página que será exibida em caso de erro. Como exemplo, temos
#uma página html erro404.html". Não adicione o diretório
#físico antes, basta colocar o caminho para o arquivo a partir dele.
PAGINA_DE_ERRO_404 = "erro404.html"

#Lista das extensões de arquivo que o servidor aceita, junto com os respectivos MIME types.
#Caso queira disponibilizar outro tipo de arquivo, coloque a extensão junto com o MIME type.
EXTENSOES_CONHECIDAS = {
    "html": "text/html",
    "htm": "text/html",
    "js": "text/javascript",
    "jpeg": "image/jpeg",
    "jpg": "image/jpeg",
    "png": "image/png",
    "gif": "image/gif",
}

#Caso queira adicionar um delay na resposta ao servidor para testar conexões simultâneas,
#coloque um número positivo. Caso contrário, deixe em 0
DELAY = 0
