# INF1407
Trabalhos Prog Web

T1 - INF1407 - Relatório

Professor: Alexandre Malheiros Meslin

Integrantes:
-Luiz Fellipe da Silveira Câmara Augusto - 1711256
-Bruno Coutinho Moretta Monteiro - 1910392

Objetivo: Implementação de um Servidor Web

== Como Utilizar ==

O sevidor possui dois arquivos principais, o "server.py", onde foi programado o servidor em si
e o "arquivo.py", onde os padrões do servidor podem ser configurados à vontade (Ex: Porta, página de erro, extensões conhecidas, etc)

Primeiramente é necessário adicionar pelo menos um arquivo na lista de arquivos default no "arquivo.py" que esteja presente no diretório do trabalho. 
Este será o arquivo default utilizado caso o pedido não receber nenhum nome de arquivo.

O Diretório Físico do trabalho deverá ser indicado no "arquivo.py".

Também é importante que exista um arquivo de erro404 no diretório para ser exibido quando um caminho ou arquivo requisitado não existir. Deixamos um
arquivo de erro html como exemplo.


Execução do servidor (no cmd):

Linux: python ./server.py porta

A porta do servidor pode ou não ser indicada durante execução. Caso não seja explicitada, a porta default presente no "arquivo.py" será utilizada.

Atenção: O servidor deve ser executado em uma máquina Linux uma vez que processos são utilizados para permitir o acesso simultâneo da página.




== Desenvolvimento ==

Para o desenvolvimento do trabalho, nós utilizamos de base o código disponibilizado nos slides da matéria e completamos
com as funcionalidades requisitadas e diversas funções auxiliares.

GET:

Para a leitura do GET criamos a função "leRequisicao" que recebe o "buffer" que condiz com o texto completo do requerimento GET
e divide cada informação relevante da primeira linha desse texto. Para isso, fazemos um split e dividimos cada informação em uma variável diferente,
sendo estas o "caminho" (caminho do arquivo), "versão" (versão HTTP) e "tipo do arquivo" (extensão do arquivo. Ex: html, gif, jpg, etc), sendo que este
último nós fizemos uma função "getExtensaoArquivo" que utiliza um regex que identifica apenas os caracteres do "caminho" após o ponto ("."), ou seja, 
a extensão do arquivo ao final.


Tratamento de Arquivos:

Criamos a função "encontraArquivo" que recebe o caminho requisitado e primeiramente checa se este trata-se de um diretório, caso sim, percorre a lista
de arquivos default presentes no "arquivo.py" até encontrar um válido, ao encontrá-lo, retorna o arquivo, seu tipo de arquivo (extensão) e o status
code de sucesso(200). Caso não exista nenhum arquivo válido na lista, será retornado o status code de erro (404) e a página de erro indicada no "arquivo.py".
No caso da função receber um arquivo ao invés de um diretório, ela checará se o arquivo é válido e se sua extensão é conhecida, caso sim, o retornará
juntamente com o status code de sucesso. Caso contrário, retornará o status code de erro, assim como a página de erro 404.


Resposta ao GET:

Para montar a resposta ao GET lido, fizemos a função "montaResposta" que recebe o "codigo_status" (inteiro correspondente à status code 200 ou 404),
"tipo_arquivo" (extensão do arquivo) e "caminho" (caminho para o arquivo que deverá ser passado para o cliente). Para o header da resposta, criamos
outras três funções auxiliares "primeiraLinhaHeader" (Retorna a primeira linha do header no formato bytes de acordo com código.), 
"segundaLinhaHeader" (Retorna linha Content-Type do header no formato bytes de acordo com tipo do arquivo.) e "terceiraLinhaHeader" (Retorna linha Content-Length 
do header no formato bytes de acordo com tamanho do arquivo.). Já o body resposta equivale a uma leitura do arquivo recebido. Assim, a função "montaResposta"
retorna a resposta completa que será dada ao cliente, contendo o header e o body.


Validação do arquivo de Configuração:

Assim que o servidor é executado, fazemos a conferência de todos os parâmetros presentes no arquivo de configuração, primeiramente conferimos se todas as
variáveis existem e em seguida fazemos testes individuais em cima delas.


Testes:

Utilizamos o browser no ambiente linux para testar nossas funcionalidades (acessamos a página localhost:porta). Testamos todas as funcionalidades requisitadas
no trabalho, sendo elas:

TESTE: Requisição GET para arquivo válido (para todos os tipos de arquivos com extensões conhecidas).
Resultado: Resposta ao pedido GET com status code de sucesso e a página requisitada.

TESTE: Requisição GET com caminho inválido.
Resultado: Resposta ao pedido GET com status code de erro e página 404.

TESTE: Requisição GET com diretório válido e pelo menos um arquivo default válido.
Resultado: Resposta ao pedido GET com status code de sucesso e o primeiro arquivo default válido.

TESTE: Requisição GET com diretório válido e nenhum arquivo default válido.
Resultado: Resposta ao pedido GET com status code de erro e página 404.

TESTE: Conexão simultânea de clientes.
Resultado: Conexão aceita.

PS: Para este teste, utilizamos um delay de 20 segundos (pode ser configurado no "arquivo.py") e notamos que ao abrir diversas abas ao mesmo tempo,
todas carregaram simultanemente (com um intervalo ínfimo de tempo entre cada uma) após os 20 segundos, indicando que os pedidos foram processados em paralelo.

TESTE: Diretório físico inválido.
Resultado: Mensagem de erro e Servidor não é aberto.
