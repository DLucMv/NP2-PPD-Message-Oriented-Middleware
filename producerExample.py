import stomp

conn = stomp.Connection([('localhost', 61613)])
conn.connect('admin', 'admin', wait=True)

mensagem = "Olá do Python via ActiveMQ!"
conn.send(destination='/queue/fila.exemplo', body=mensagem)

print("Mensagem enviada.")
conn.disconnect()
