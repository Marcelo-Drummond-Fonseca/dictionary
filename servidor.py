#servidor de echo: lado servidor
#com finalizacao do lado do servidor
#com multiprocesso
import socket
import select
import sys
import multiprocessing
import json
import struct




class Dicionario:

    def lerDicionario(self, chave, lock):
        '''Carrega o dicionario e retorna o valor desejado de acordo com a chave'''
        lock.acquire()
        dicionario = json.load(open("dicionario.txt"))
        lock.release()
        return str(dicionario.get(chave))

    def escreverDicionario(self, chave, texto, lock):
        '''Carrega o dicionario e escreve o valor desejado na lista da chave'''
        lock.acquire()
        dicionario = json.load(open("dicionario.txt"))
        if chave in dicionario:
            dicionario[chave].append(texto)
        else:
            dicionario[chave] = [texto]
        json.dump(dicionario, open("dicionario.txt",'w'))
        lock.release()

    def removerChaveDicionario(self, chave, lock):
        '''Carrega o dicionario e remove o valor desejado na lista da chave'''
        lock.acquire()
        dicionario = json.load(open("dicionario.txt"))
        if chave in dicionario:
            del dicionario[chave]
        json.dump(dicionario, open("dicionario.txt",'w'))
        lock.release()

    def removerElementoDicionario(self, chave, texto, lock):
        '''Carrega o dicionario e remove o valor desejado na lista da chave'''
        lock.acquire()
        dicionario = json.load(open("dicionario.txt"))
        if chave in dicionario:
            if texto in dicionario[chave]:
                dicionario[chave].remove(texto)
        json.dump(dicionario, open("dicionario.txt",'w'))
        lock.release()

class Servidor:
    # define a localizacao do servidor
    HOST = '' # vazio indica que podera receber requisicoes a partir de qq interface de rede da maquina
    PORT = 10011 # porta de acesso

    #define a lista de I/O de interesse (jah inclui a entrada padrao)
    entradas = [sys.stdin]
    #armazena historico de conexoes
    conexoes = {}

    dicionario = Dicionario()
    lock = multiprocessing.Lock()

    def sendMessage(self, sock, message):
        convertedMessage = message.encode('utf-8')
        sock.sendall(struct.pack('>I', len(convertedMessage)))
        sock.sendall(convertedMessage)
        
    def recvMessage(self, sock):
        sizeData = sock.recv(4)
        if not sizeData: # dados vazios: cliente encerrou
            return 0
        msglen = struct.unpack('>I', sizeData)[0]
        received = b''
        remaining = msglen
        while remaining != 0:
            received += sock.recv(remaining)
            remaining = msglen - len(received)
        return received

    def atendeRequisicoes(self, clisock, endr):
        '''Recebe mensagens e as envia de volta para o cliente (ate o cliente finalizar)
        Entrada: socket da conexao e endereco do cliente
        Saida: '''
        while True:
            #recebe dados do cliente
            data = self.recvMessage(clisock)
            if data == 0:
                print(str(endr) + '-> encerrou')
                clisock.close() # encerra a conexao com o cliente
                return
            print(str(endr) + ': ' + str(data, encoding='utf-8'))
            if str(data, encoding='utf-8') == "E":
                self.sendMessage(clisock,"Escreva a chave")
                chave = self.recvMessage(clisock) 
                if chave == 0:
                    print(str(endr) + '-> encerrou')
                    clisock.close() # encerra a conexao com o cliente
                    return
                print(str(endr) + ': ' + str(chave, encoding='utf-8'))
                self.sendMessage(clisock,"Escreva o texto associado à chave")
                texto = self.recvMessage(clisock) 
                if texto == 0:
                    print(str(endr) + '-> encerrou')
                    clisock.close() # encerra a conexao com o cliente
                    return
                print(str(endr) + ': ' + str(texto, encoding='utf-8'))
                self.dicionario.escreverDicionario(str(chave, encoding='utf-8'),str(texto, encoding='utf-8'), self.lock)
                self.sendMessage(clisock, str(texto, encoding='utf-8') + ' foi incluido na chave ' + str(chave, encoding='utf-8'))
            elif str(data, encoding='utf-8') == "L":
                self.sendMessage(clisock,"Escreva a chave")
                chave = self.recvMessage(clisock) 
                if chave == 0:
                    print(str(endr) + '-> encerrou')
                    clisock.close() # encerra a conexao com o cliente
                    return
                print(str(endr) + ': ' + str(chave, encoding='utf-8'))
                texto = self.dicionario.lerDicionario(str(chave, encoding='utf-8'), self.lock)
                self.sendMessage(clisock,texto)
            else: self.sendMessage(clisock,"Comando nao reconhecido") # ecoa os dados para o cliente

    def iniciaServidor(self):
        '''Cria um socket de servidor e o coloca em modo de espera por conexoes
        Saida: o socket criado'''
        # cria o socket 
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Internet( IPv4 + TCP) 

        # vincula a localizacao do servidor
        sock.bind((self.HOST, self.PORT))

        # coloca-se em modo de espera por conexoes
        sock.listen(5) 

        # configura o socket para o modo nao-bloqueante
        sock.setblocking(False)

        # inclui o socket principal na lista de entradas de interesse
        self.entradas.append(sock)

        return sock

    def aceitaConexao(self, sock):
        '''Aceita o pedido de conexao de um cliente
        Entrada: o socket do servidor
        Saida: o novo socket da conexao e o endereco do cliente'''

        # estabelece conexao com o proximo cliente
        clisock, endr = sock.accept()

        # registra a nova conexao
        self.conexoes[clisock] = endr 

        return clisock, endr



    def mainServidor(self):
        '''Inicializa e implementa o loop principal (infinito) do servidor'''
        clientes=[] #armazena os processos criados para fazer join
        sock = self.iniciaServidor()
        print("Pronto para receber conexoes...")
        while True:
            #espera por qualquer entrada de interesse
            leitura, escrita, excecao = select.select(self.entradas, [], [])
            #tratar todas as entradas prontas
            for pronto in leitura:
                if pronto == sock:  #pedido novo de conexao
                    clisock, endr = self.aceitaConexao(sock)
                    print ('Conectado com: ', endr)
                    #cria novo processo para atender o cliente
                    cliente = multiprocessing.Process(target=self.atendeRequisicoes, args=(clisock,endr))
                    cliente.start()
                    clientes.append(cliente) #armazena a referencia da thread para usar com join()
                elif pronto == sys.stdin: #entrada padrao
                    cmd = input()
                    if cmd == 'fim': #solicitacao de finalizacao do servidor
                        for c in clientes: #aguarda todos os processos terminarem
                            c.join()
                        sock.close()
                        sys.exit()
                    elif cmd == 'hist': #outro exemplo de comando para o servidor
                        print(str(self.conexoes.values()))
                    elif cmd == 'R': #Remove um elemento do dicionario
                        print('Remover Chave (C) ou elemento (E) da lista?: ')
                        cmd = input()
                        if cmd == 'C':
                            print('Digite a chave a ser removida: ')
                            cmd = input()
                            self.dicionario.removerChaveDicionario(cmd, self.lock)
                        elif cmd == 'E':
                            print('Digite a chave do elemento: ')
                            chave = input()
                            print('Digite o elemento: ')
                            texto = input()
                            self.dicionario.removerElementoDicionario(chave, texto, self.lock)

def main():
    servidor = Servidor()
    servidor.mainServidor()

main()
