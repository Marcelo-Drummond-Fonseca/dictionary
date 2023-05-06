# dictionary

Nome: Marcelo Drummond Fonseca
DRE: 117216621

Os arquivos permitem realizar uma conexão cliente-servidor onde é guardado um dicionário disponível para uso por multiplos clientes.

ATIVIDADE 1: ARQUITETURA DE SOFTWARE:

A arquitetura de software é composta de três componentes principais: A Interface, o Servidor, e o Dicionario, cada um tendo uma classe com seu respectivo nome.

O estilo arquitetural escolhido foi a arquitetura em camadas, com a Interface relacionando com o usuário, o Servidor realizando o processamento e o Dicionario armazenando os dados.

A Interface serve para que o cliente envie e receba informações do Servidor. Possui funções para estabalecer conexão com o Servidor e enviar e receber mensagens dele (usando TCP). Claro, também instrui o usuário em como utilizar o sistema, recebe seus inputs e devolve as mensagens retornadas pelo Servidor. A Interface também pode cortar a conexãao a qualquer momento digitando "fim".

O Servidor passivamente espera receber conexão e mensagens da Interface, e trata elas de acordo, trocando informações até obter o que precisa para realizar uma operação no banco. Pode ser uma operação de leitura, em que retornará os dados que obtem do banco para o usuáriom ou de escrita, em que vai inserir os dados do usuário no banco. Se comunica com o banco através de chamadas de leitura ou escrita informado a chave e componente (se houver). Além de realizar essa comunicação e processamento, também possui imbutida uma interface para o administrador, em que este pode remover elementos do dicionário usando o comando "R" ou fechar o servidor usando o comando "fim".

Os dados do Dicionario são armazenados em um json contendo o dicionário. Utilizando funções nativas do python além de uma tranca para impedir que multiplos processos tentem mexer no banco ao mesmo tempo.

ATIVIDADE 2: ARQUITETURA DE SISTEMA:

Para a arquitetura de cliente/servidor implementada, ficou bem claro o papel de cada componente: A Interface fica do lado do cliente, e o Servidor e Dicionario ficam do lado do servidor.

As mensagens que são trocadas entre o cliente e o servidor devem seguir o seguinte padrão: O cliente envia uma mensagem escrita "L" (de Ler) ou "E" (de escrever), informando ao servidor qual operação deseja realizar. O servidor então retorna a mensagem "Escreva a chave", pedindo que o cliente informe qual chave deseja consultar ou realizar escrita. O cliente então pede ao usuário e manda mensagem com a chave, e existem duas possibilidades para o servidor: se é leitura, o servidor consulta o dicionário em busca da lista associada à chave. Se a chave não está no dicionário, retorna "None". Se está, retorna a lista associada à chave. Se a operação escolhida foi escrita, o servidor enviará uma outra mensagem para o cliente, "Escreva o texto associado à chave", pedindo o texto que deve escrever no banco. O cliente então pede ao usuário e manda mensagem com o texto, que o servidor receberá e vai pedir uma operação de escrita no banco, inserindo o texto na lista da chave passada.

Se o cliente escrever "fim", imediatamente encerra a conexão com o servidor. Ao escrever qualquer outra mensagem, o servidor retornará "Comando não reconhecido".
