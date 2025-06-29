import stomp
import time

class MeuListener(stomp.ConnectionListener):
    def on_message(self, frame):
        print("Mensagem recebida no tópico:", frame.body)

conn = stomp.Connection([('localhost', 61613)])
conn.set_listener('', MeuListener())

conn.connect('admin', 'admin', wait=True)

# Subcreve ao tópico (não a fila)
conn.subscribe(destination='/topic/topico.exemplo', id=1, ack='auto')

print("Assinado ao tópico. Aguardando mensagens...\n")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    conn.disconnect()
