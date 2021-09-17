T1 - INF1407 - Relatório

Integrantes:
-Luiz Fellipe da Silveira Câmara Augusto - 1711256
-Bruno Coutinho Moretta Monteiro - 1910392

Objetivo: Implementação de um Servidor Web

Como Utilizar:

O sevidor possui dois arquivos principais, o "server.py", onde foi programado o servidor em si
e o "arquivo.py", onde os padrões do servidor podem ser configurados à vontade (Ex: Porta, página de erro, extensões conhecidas, etc)

Primeiramente é necessário adicionar pelo menos um arquivo na lista de arquivos default no "arquivo.py" que esteja presente no diretório do trabalho. 
Este será o arquivo default utilizado caso o pedido não receber nenhum nome de arquivo.

O Diretório Físico do trabalho deverá ser indicado no "arquivo.py".

Também é importante que exista um arquivo de erro404 no diretório para ser exibido quando um caminho ou arquivo requisitado não existir.


Execução do servidor (no cmd):

Linux: python ./server.py porta

A porta do servidor pode ou não ser indicada durante execução. Caso não seja explicitada, a porta default presente no "arquivo.py" será utilizada.

Atenção: O servidor deve ser executado em uma máquina Linux uma vez que processos são utilizados para permitir o acesso simultâneo da página.




Desenvolvimento:

Para o desenvolvimento do trabalho, nós utilizamos de base o código disponibilizado nos slides da matéria e completamos
com as funcionalidades requisitadas e diversas funções auxiliares  

