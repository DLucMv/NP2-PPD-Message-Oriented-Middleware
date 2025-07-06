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
        self.conn.subscribe(destination=self.queue, id=1, ack='auto')
        self.subscribed_topics = set()
        print(f"[{self.username}] conectado e ouvindo sua fila pessoal: {self.queue}")

    def on_message(self, frame):
        print(f"\n📩 [{self.username}] Nova mensagem: {frame.body}")

    def subscribe_topic(self, topic_name):
        destination = f"/topic/{topic_name}"
        if destination in self.subscribed_topics:
            print(f"[{self.username}] Já inscrito em {destination}")
        else:
            self.conn.subscribe(destination=destination, id=len(self.subscribed_topics)+2, ack='auto')
            self.subscribed_topics.add(destination)
            print(f"[{self.username}] Inscrito no tópico {destination}")

    def send_to_user(self, target_user, message):
        destination = f"/queue/user.{target_user}"
        full_msg = f"De {self.username}: {message}"
        self.conn.send(destination=destination, body=full_msg)
        print(f"[{self.username}] Enviou mensagem para {target_user}")

    def send_to_topic(self, topic_name, message):
        destination = f"/topic/{topic_name}"
        full_msg = f"[{self.username}] diz: {message}"
        self.conn.send(destination=destination, body=full_msg)
        print(f"[{self.username}] Enviou mensagem para o tópico '{topic_name}'")

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
                    topic = input("Nome do tópico: ").strip()
                    self.subscribe_topic(topic)
                elif opcao == '2':
                    target = input("Usuário destino: ").strip()
                    msg = input("Mensagem: ")
                    self.send_to_user(target, msg)
                elif opcao == '3':
                    topic = input("Tópico destino: ").strip()
                    msg = input("Mensagem: ")
                    self.send_to_topic(topic, msg)
                elif opcao == '4':
                    print("Encerrando...")
                    self.conn.disconnect()
                    break
                else:
                    print("Opção inválida.")

        threading.Thread(target=loop).start()
        while True:
            time.sleep(1)

# Exemplo de execução
if __name__ == "__main__":
    nome = input("Digite seu nome de usuário: ").strip()
    app = UserApp(nome)
    app.run()
