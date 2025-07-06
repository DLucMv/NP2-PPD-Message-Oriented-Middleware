import stomp
import time
import threading

class UserApp(stomp.ConnectionListener):
    def __init__(self, username):
        self.username = username
        self.queue = f"/queue/user.{username}"
        self.conn = stomp.Connection([('localhost', 61613)])
        self.conn.set_listener('', self)
        self.conn.connect('admin', 'admin', wait=True)

    def on_message(self):
        #To-Do

    def subscribe_topic(self):
        #To-Do

    def send_to_user(self):
        #To-Do

    def send_to_topic(self):
        #To-Do

    def run(self):
        def loop():
            while True:
                print("\n🔹 Menu:")
                print("1. Assinar tópico")
                print("2. Enviar mensagem para usuário")
                print("3. Enviar mensagem para tópico")
                print("4. Sair")
                opcao = input("Escolha: ").strip()

                if opcao == '1':
                    #To-Do
                elif opcao == '2':
                    #To-Do
                elif opcao == '3':
                    #To-Do
                elif opcao == '4':
                    #To-Do
                    break
                else:
                    print("Opção inválida.")

# Exemplo de execução
if __name__ == "__main__":
    nome = input("Digite seu nome de usuário: ").strip()
    app = UserApp(nome)
    app.run()
