import stomp
import json
import os

class MOMManager:
    def __init__(self):
        self.conn = stomp.Connection([('localhost', 61613)])
        self.conn.connect('admin', 'admin', wait=True)
        self.users = set()
        self.queues = set()
        self.topics = set()
        self.user_queues = {}

    def add_user(self, username):
        if username in self.users:
            print("Usuário já existe.")
            return False
        self.users.add(username)
        user_queue = f"/queue/user.{username}"
        self.queues.add(user_queue)
        self.user_queues[username] = user_queue
        print(f"Usuário '{username}' adicionado com fila '{user_queue}'")
        return True

    def remove_user(self, username):
        if username not in self.users:
            print("Usuário não existe.")
            return False
        self.queues.discard(self.user_queues[username])
        del self.user_queues[username]
        self.users.remove(username)
        print(f"Usuário '{username}' removido.")
        return True

    def disconnect(self):
        self.conn.disconnect()


from momManager import MOMManager

manager = MOMManager()

manager.add_user("joao")
manager.add_user("maria")

manager.remove_user("joao")
manager.disconnect()
