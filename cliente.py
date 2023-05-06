#servidor de echo: lado cliente
import socket
import struct


class Interface:

    HOST = 'localhost' # maquina onde esta o servidor
    PORT = 10011       # porta que o servidor esta escutando

    def sendMessage(self, sock, message):
        convertedMessage = message.encode('utf-8')
        sock.sendall(struct.pack('>I', len(convertedMessage)))
        sock.sendall(convertedMessage)
        
    def recvMessage(self,sock):
        msglen = struct.unpack('>I', sock.recv(4))[0]
        received = b''
        remaining = msglen
        while remaining != 0:
            received += sock.recv(remaining)
            remaining = msglen - len(received)
        return received


    def iniciaCliente(self):
        '''Cria um socket de cliente e conecta-se ao servidor.
        Saida: socket criado'''
        # cria socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Internet (IPv4 + TCP) 

        # conecta-se com o servidor
        sock.connect((self.HOST, self.PORT)) 

        return sock

    def fazRequisicoes(self, sock):
        '''Faz requisicoes ao servidor e exibe o resultado.
        Entrada: socket conectado ao servidor'''
        # le as mensagens do usuario ate ele digitar 'fim'
        while True: 
            msg = input("Digite uma mensagem ('fim' para terminar):")
            if msg == 'fim': break 

            # envia a mensagem do usuario para o servidor
            self.sendMessage(sock, msg)

            #espera a resposta do servidor
            msg = self.recvMessage(sock)

            # imprime a mensagem recebida
            print(str(msg, encoding='utf-8'))

        # encerra a conexao
        sock.close()

    def mainInterface(self):
        '''Funcao principal do cliente'''
        #inicia o cliente
        sock = self.iniciaCliente()
        #interage com o servidor ate encerrar
        self.fazRequisicoes(sock)

def main():
    interface = Interface()
    interface.mainInterface()

main()
