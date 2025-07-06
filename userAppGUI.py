import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
import stomp
import threading
import time

class UserAppGUI(stomp.ConnectionListener):
    def __init__(self, root, username):
        self.root = root
        self.root.title(f"Aplicação de Mensagem - {username}")
        self.username = username
        self.queue = f"/queue/user.{username}"
        self.subscribed_topics = set()

        # STOMP
        self.conn = stomp.Connection([('localhost', 61613)])
        self.conn.set_listener('', self)
        self.conn.connect('admin', 'admin', wait=True)
        self.conn.subscribe(destination=self.queue, id=1, ack='auto')

        # Interface
        self.create_widgets()

        # Thread de escuta
        threading.Thread(target=self.listen_loop, daemon=True).start()

    def create_widgets(self):
        # Área de mensagens recebidas
        self.msg_area = scrolledtext.ScrolledText(self.root, width=60, height=20, state='disabled')
        self.msg_area.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Entrada para enviar a outro usuário
        tk.Label(self.root, text="Usuário destino:").grid(row=1, column=0, sticky='e')
        self.entry_user = tk.Entry(self.root)
        self.entry_user.grid(row=1, column=1, sticky='w')

        tk.Label(self.root, text="Mensagem:").grid(row=2, column=0, sticky='e')
        self.entry_msg_user = tk.Entry(self.root, width=40)
        self.entry_msg_user.grid(row=2, column=1, sticky='w')

        btn_user = tk.Button(self.root, text="Enviar p/ usuário", command=self.send_to_user)
        btn_user.grid(row=3, column=0, columnspan=2, pady=5)

        # Enviar para tópico
        tk.Label(self.root, text="Tópico:").grid(row=4, column=0, sticky='e')
        self.entry_topic = tk.Entry(self.root)
        self.entry_topic.grid(row=4, column=1, sticky='w')

        tk.Label(self.root, text="Mensagem:").grid(row=5, column=0, sticky='e')
        self.entry_msg_topic = tk.Entry(self.root, width=40)
        self.entry_msg_topic.grid(row=5, column=1, sticky='w')

        btn_topic = tk.Button(self.root, text="Enviar p/ tópico", command=self.send_to_topic)
        btn_topic.grid(row=6, column=0, columnspan=2, pady=5)

        # Assinar tópico
        btn_subscribe = tk.Button(self.root, text="Assinar novo tópico", command=self.subscribe_topic)
        btn_subscribe.grid(row=7, column=0, columnspan=2, pady=10)

    def append_message(self, text):
        self.msg_area.configure(state='normal')
        self.msg_area.insert(tk.END, f"{text}\n")
        self.msg_area.configure(state='disabled')
        self.msg_area.see(tk.END)

    def on_message(self, frame):
        self.append_message(f"📩 {frame.body}")

    def send_to_user(self):
        target = self.entry_user.get().strip()
        msg = self.entry_msg_user.get().strip()
        if not target or not msg:
            messagebox.showwarning("Campos obrigatórios", "Preencha usuário e mensagem.")
            return
        dest = f"/queue/user.{target}"
        full_msg = f"[{self.username}] diz: {msg}"
        self.conn.send(destination=dest, body=full_msg)
        self.append_message(f"✅ Enviado para {target}: {msg}")
        self.entry_msg_user.delete(0, tk.END)

    def send_to_topic(self):
        topic = self.entry_topic.get().strip()
        msg = self.entry_msg_topic.get().strip()
        if not topic or not msg:
            messagebox.showwarning("Campos obrigatórios", "Preencha tópico e mensagem.")
            return
        dest = f"/topic/{topic}"
        full_msg = f"[{self.username}] (tópico): {msg}"
        self.conn.send(destination=dest, body=full_msg)
        self.append_message(f"📢 Enviado para tópico '{topic}': {msg}")
        self.entry_msg_topic.delete(0, tk.END)

    def subscribe_topic(self):
        topic = simpledialog.askstring("Assinar Tópico", "Digite o nome do tópico:")
        if topic:
            dest = f"/topic/{topic}"
            if dest in self.subscribed_topics:
                messagebox.showinfo("Já assinado", f"Você já está inscrito em {topic}")
                return
            self.conn.subscribe(destination=dest, id=len(self.subscribed_topics)+2, ack='auto')
            self.subscribed_topics.add(dest)
            self.append_message(f"🔔 Assinado ao tópico: {topic}")

    def listen_loop(self):
        while True:
            time.sleep(1)

# Execução
if __name__ == "__main__":
    root = tk.Tk()
    nome = simpledialog.askstring("Usuário", "Digite seu nome de usuário:", parent=root)
    if nome:
        app = UserAppGUI(root, nome.strip())
        root.mainloop()
