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
    
    def parse_cows_arguments(self, parameters):
        arguments = {'message': parameters[0],
                     'cow': 'default',
                     'preset': None,
                     'eyes': 'oo',
                     'tongue': '  ',
                     'width': 40,
                     'wrap_text': True,
                     'cowfile': None}
        k = 1
        for i in parameters[1:]:
            if '=' in i:
                arguments[i.split('=')[0]] = type(arguments[i.split('=')[0]])(i.split('=')[1])
            else:
                arguments[list(arguments.keys())[k]] = i
                k += 1
        return arguments

   
    def do_cowsay(self, args):
        s = shlex.split(args)
        parameters_1 = self.parse_cows_arguments(s[:s.index("reply")])
        parameters_2 = self.parse_cows_arguments(s[s.index("reply") + 1:])


    def dow_cowthink(self, args):
        pass

if __name__ == '__main__':
    cmd_cow().cmdloop() 
