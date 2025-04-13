import socket
import threading
import tkinter as tk
from tkinter import simpledialog, scrolledtext

port = 5000
serverip = "127.0.0.1"

class ChatClient:
    def __init__(self, chat):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((serverip, port))

        client_port = self.sock.getsockname()[1]
        self.chat = chat
        self.username = simpledialog.askstring("Username", "Enter your name:", parent=self.chat)
        self.chat.title(f"Client {self.username} at {client_port}")

        self.chat_area = scrolledtext.ScrolledText(chat, wrap=tk.WORD, state='disabled') 
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.input_area = tk.Entry(chat)
        self.input_area.pack(padx=10, pady=(0, 10), fill=tk.X)
        self.input_area.bind("<Return>", self.send_message)

        self.running = True

        threading.Thread(target=self.receive_messages, daemon=True).start()

    def send_message(self, event=None):
        message = self.input_area.get().strip()
        if message:
            full_message = f"{self.username}: {message}"
            self.display_message(message)
            self.sock.sendall(full_message.encode())
            self.input_area.delete(0, tk.END)
        return "break"

    def receive_messages(self):
        while self.running:
            msg = self.sock.recv(1024)
            if msg:
                decoded = msg.decode()
                if not decoded.startswith(f"{self.username}:"):
                    self.display_message(decoded)
            else:
                break
            
   

    def display_message(self, msg):
        self.chat_area.configure(state='normal')
        self.chat_area.insert(tk.END, msg + '\n')
        self.chat_area.configure(state='disabled')
        self.chat_area.yview(tk.END)
        

    def close(self):
        self.running = False
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
            self.sock.close()
        except:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    client = ChatClient(root)
    root.mainloop()
