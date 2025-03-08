import cowsay
import cmd
import shlex

class cmd_cow(cmd.Cmd):
    prompt = "twocows>"

    def do_list_cows(self, args):
        """
        Lists all cow file names in the given directory or in the default directory
        """
        if args:
            print(cowsay.list_cows(args))
        else:
            print(cowsay.list_cows())

    def do_make_bubble(self, args):
        """
        Sets text inside a bubble.
        This is the text that appears above the cows
        """
        print(cowsay.make_bubble(args))

    def do_cowsay(self, args):
        pass

    def dow_cowthink(self, args):
        pass

if __name__ == '__main__':
    cmd_cow().cmdloop() 
