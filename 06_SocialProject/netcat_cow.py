import sys
import socket
import cmd
import threading
import readline
import cowsay
import time

class simple(cmd.Cmd):

    def do_echo(self, arg):
        print(arg)

def spam(cmdline, timeout, count):
    for i in range(count):
        time.sleep(timeout)
        print(f"\nI'm a message № {i}!\n{cmdline.prompt}{readline.get_line_buffer()}", end="", flush=True)


cmdline = simple()
timer = threading.Thread(target=spam, args=(cmdline, 3, 10))
timer.start()
cmdline.cmdloop()

