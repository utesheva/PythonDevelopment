import sys
import socket
import cmd
import threading
import readline
import cowsay
import time

class chat_cmd(cmd.Cmd):
    prompt = "cow chat> "

    def __init__(self, *args, socket, **kwargs):
        self.s = socket
        return super().__init__(*args, **kwargs)

    def do_who(self, args):
        self.s.sendall("who\n")

    def do_cows(self, args):
        self.s.sendall("cows\n")

    def do_login(self, args):
        self.s.sendall(f"login {args}\n")

    def do_say(self, args):
        self.s.sendall(f"say {args}\n")

    def do_yield(self, args):
        self.s.sendall(f"yield {args}\n")

    def do_quit(self, args):
        self.s.sendall("quit\n")

    def default(self, args):
        print("Invalid command")

    def complete_login(self, text, line, begidx, endidx):
        if len((line[:endidx] + ".").split()) == 2:
            self.compl = True
            self.s.sendall("cows\n")
            while self.compl:
                continue
            return [c for c in self.response if c.startswith(text)]

        
    def complete_say(self, text, line, begidx, endidx):
        if len((line[:endidx] + ".").split()) == 2:
            self.compl = True
            self.s.sendall("who\n")
            while self.compl:
                continue
            return [c for c in self.response if c.startswith(text)]

    def do_EOF(self, args):
        return 1

    def get_message(self, cmdline, s):
        while response := s.recv(1024).rstrip().decode().split():
            if response[0] == '0':
                if self.compl: 
                    self.response = response
                    self.compl = False
                else:
                    print(f"\n{'\n'.join(response[1:])}\n{cmdline.prompt}{readline.get_line_buffer()}", end="", flush=True)

            else:
                print(f"\n{cowsay.cowsay(response[1], cow=' '.join(response[2:]))}\n{cmdline.prompt}{readline.get_line_buffer()}", end="", flush=True)


if __name__ == '__main__':
    host = "localhost" if len(sys.argv) < 2 else sys.argv[1]
    port = 1337 if len(sys.argv) < 3 else int(sys.argv[2])
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    cmdline = chat_cmd(socket=s)
    mes = threading.Thread(target=cmdline.get_message, args = (cmdline, s))
    mes.start()
    cmdline.cmdloop()
    d.disconnect()

