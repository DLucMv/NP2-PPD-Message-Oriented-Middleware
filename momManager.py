import stomp

class MOMManager:
    def __init__(self):
        self.conn = stomp.Connection([('localhost', 61613)])
        self.conn.connect('admin', 'admin', wait=True)
        self.users = set()
        self.queues = set()
        self.topics = set()
        self.user_queues = {}

    # === USUÁRIOS ===
    def add_user(self, username):
        if username in self.users:
            print(f"[MOMManager] ❌ Usuário '{username}' já existe.")
            return False
        self.users.add(username)
        self.add_queue(f"user.{username}")
        self.user_queues[username] = f"/queue/user.{username}"
        print(f"[MOMManager] ✅ Usuário '{username}' criado com fila '/queue/user.{username}'")
        return True

    def remove_user(self, username):
        if username not in self.users:
            print(f"[MOMManager] ⚠️ Usuário '{username}' não existe.")
            return False
        queue_name = f"user.{username}"
        self.remove_queue(queue_name)
        del self.user_queues[username]
        self.users.remove(username)
        print(f"[MOMManager] 🗑️ Usuário '{username}' removido.")
        return True

    # === FILAS ===
    def add_queue(self, name):
        queue_path = f"/queue/{name}"
        if queue_path in self.queues:
            print(f"[MOMManager] ⚠️ Fila '{queue_path}' já existe.")
            return False
        self.queues.add(queue_path)
        print(f"[MOMManager] ➕ Fila adicionada: {queue_path}")
        return True

    def remove_queue(self, name):
        queue_path = f"/queue/{name}"
        if queue_path in self.queues:
            self.queues.remove(queue_path)
            print(f"[MOMManager] 🗑️ Fila removida: {queue_path}")
            return True
        print(f"[MOMManager] ⚠️ Fila '{queue_path}' não encontrada.")
        return False

    # === TÓPICOS ===
    def add_topic(self, name):
        topic_path = f"/topic/{name}"
        if topic_path in self.topics:
            print(f"[MOMManager] ⚠️ Tópico '{topic_path}' já existe.")
            return False
        self.topics.add(topic_path)
        print(f"[MOMManager] ➕ Tópico adicionado: {topic_path}")
        return True

    def remove_topic(self, name):
        topic_path = f"/topic/{name}"
        if topic_path in self.topics:
            self.topics.remove(topic_path)
            print(f"[MOMManager] 🗑️ Tópico removido: {topic_path}")
            return True
        print(f"[MOMManager] ⚠️ Tópico '{topic_path}' não encontrado.")
        return False

    # === LISTAGEM ===
    def list_queues(self):
        print("\n📦 Filas registradas:")
        for q in sorted(self.queues):
            print(" -", q)

    def list_topics(self):
        print("\n📢 Tópicos registrados:")
        for t in sorted(self.topics):
            print(" -", t)

    # === OUTROS ===
    def message_count(self, queue_name):
        print(f"[MOMManager] (Simulado) Mensagens em '{queue_name}': N (via JMX/REST)")

    def disconnect(self):
        self.conn.disconnect()


# Singleton para integração
manager_instance = None

def get_manager():
    global manager_instance
    if manager_instance is None:
        manager_instance = MOMManager()
    return manager_instance
