import stomp

class MeuListener(stomp.ConnectionListener):
    def on_message(self, frame):
        print("Mensagem recebida:", frame.body)

conn = stomp.Connection([('localhost', 61613)])
conn.set_listener('', MeuListener())

conn.connect('admin', 'admin', wait=True)
conn.subscribe(destination='/queue/fila.exemplo', id=1, ack='auto')

print("Aguardando mensagens... pressione Ctrl+C para sair.")
import time
while True:
    time.sleep(1)
