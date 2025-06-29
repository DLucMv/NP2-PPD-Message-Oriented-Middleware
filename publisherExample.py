import stomp

conn = stomp.Connection([('localhost', 61613)])
conn.connect('admin', 'admin', wait=True)

mensagem = "Mensagem de broadcast via tópico"
conn.send(destination='/topic/topico.exemplo', body=mensagem)

print("Mensagem enviada ao tópico.")
conn.disconnect()
