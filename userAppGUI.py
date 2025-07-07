import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext, Listbox
import stomp
import threading
import time
import re
from momManager import get_manager, is_username_locked, lock_username, unlock_username

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

        # Interface
        self.create_widgets()

        # Só assina após a interface estar pronta
        self.conn.subscribe(destination=self.queue, id=1, ack='auto')

        threading.Thread(target=self.listen_loop, daemon=True).start()

    def create_widgets(self):
        self.msg_area = scrolledtext.ScrolledText(self.root, width=60, height=20, state='disabled')
        self.msg_area.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Enviar para usuário
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

        # Tópicos assinados
        tk.Label(self.root, text="Tópicos assinados:").grid(row=8, column=0, sticky='ne')
        self.topic_listbox = Listbox(self.root, height=5)
        self.topic_listbox.grid(row=8, column=1, sticky='w')

        # Botões de listagem
        btn_list_users = tk.Button(self.root, text="Listar usuários conectados", command=self.show_connected_users)
        btn_list_users.grid(row=9, column=0, columnspan=2, pady=5)

        btn_list_topics = tk.Button(self.root, text="Listar tópicos existentes", command=self.show_existing_topics)
        btn_list_topics.grid(row=10, column=0, columnspan=2, pady=5)

    def append_message(self, text):
        if hasattr(self, "msg_area"):
            self.msg_area.configure(state='normal')
            self.msg_area.insert(tk.END, f"{text}\n")
            self.msg_area.configure(state='disabled')
            self.msg_area.see(tk.END)

    def on_message(self, frame):
        self.root.after(0, lambda: self.append_message(f"📩 {frame.body}"))

    def is_valid_name(self, name):
        return re.match(r'^[\w.-]+$', name) is not None

    def send_to_user(self):
        target = self.entry_user.get().strip()
        msg = self.entry_msg_user.get().strip()
        if not target or not msg:
            messagebox.showwarning("Campos obrigatórios", "Preencha usuário e mensagem.")
            return
        if not self.is_valid_name(target):
            messagebox.showerror("Nome inválido", "Nome de usuário inválido.")
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
        if not self.is_valid_name(topic):
            messagebox.showerror("Nome inválido", "Nome de tópico inválido.")
            return
        dest = f"/topic/{topic}"
        full_msg = f"[{self.username}] (tópico): {msg}"
        self.conn.send(destination=dest, body=full_msg)
        self.append_message(f"📢 Enviado para tópico '{topic}': {msg}")
        self.entry_msg_topic.delete(0, tk.END)

    def subscribe_topic(self):
        topic = simpledialog.askstring("Assinar Tópico", "Digite o nome do tópico:")
        if topic:
            topic = topic.strip()
            if not self.is_valid_name(topic):
                messagebox.showerror("Nome inválido", "Nome de tópico inválido.")
                return
            dest = f"/topic/{topic}"
            if dest in self.subscribed_topics:
                messagebox.showinfo("Já assinado", f"Você já está inscrito em {topic}")
                return
            self.conn.subscribe(destination=dest, id=len(self.subscribed_topics)+2, ack='auto')
            self.subscribed_topics.add(dest)
            self.topic_listbox.insert(tk.END, topic)
            get_manager().add_topic(topic)
            self.append_message(f"🔔 Assinado ao tópico: {topic}")

    def show_connected_users(self):
        users = get_manager().get_users()
        messagebox.showinfo("Usuários conectados", "\n".join(users) if users else "Nenhum usuário conectado.")

    def show_existing_topics(self):
        topics = get_manager().get_topics()
        messagebox.showinfo("Tópicos existentes", "\n".join(topics) if topics else "Nenhum tópico existente.")

    def listen_loop(self):
        while True:
            time.sleep(1)

    def on_close(self):
        if self.conn.is_connected():
            self.conn.disconnect()
        get_manager().unregister_user(self.username)
        unlock_username(self.username)  # desbloqueia o usuário no arquivo
        self.root.destroy()


# Execução
if __name__ == "__main__":
    root = tk.Tk()
    nome = simpledialog.askstring("Usuário", "Digite seu nome de usuário:", parent=root)
    if nome:
        nome = nome.strip()

        if is_username_locked(nome):
            messagebox.showerror("Erro", "Este nome de usuário já está em uso (por outro processo).")
            root.destroy()
        else:
            lock_username(nome)  # bloqueia nome via arquivo

            manager = get_manager()
            if not manager.register_user(nome):
                messagebox.showerror("Erro", "Este nome de usuário já está em uso (local).")
                unlock_username(nome)  # limpa bloqueio se já estiver registrado localmente
                root.destroy()
            else:
                app = UserAppGUI(root, nome)
                root.protocol("WM_DELETE_WINDOW", app.on_close)
                root.mainloop()