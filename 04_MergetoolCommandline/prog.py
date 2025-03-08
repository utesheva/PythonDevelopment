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

    def cow_from_parameters(self, command, parameters):
        cow = command(message = parameters['message'],
                              cow = parameters['cow'],
                              preset = parameters['preset'],
                              eyes = parameters['eyes'],
                              tongue = parameters['tongue'],
                              width = parameters['width'],
                              wrap_text = parameters['wrap_text'],
                              cowfile = parameters['cowfile'])
        return cow.split('\n')   
    
    def draw_two_cows(self, cow1, cow2):
        dif = abs(len(cow2) - len(cow1))
        if len(cow1) > len(cow2):
            cow2 = [''] * dif  + cow2
        else:
            cow1 = [''] * dif + cow1
        max_len_1 = max([len(i) for i in cow1])
        max_len_2 = max([len(i) for i in cow2])
        print('\n'.join([f'{i[0]:<{max_len_1}}{i[1]:<{max_len_2}}'
                         for i in zip(cow1, cow2)]))

    def do_cowsay(self, args):
        """
        Usage: cowsay message [cow [param=value ...]] reply answer [cow [param=value ...]]
        - message and answer are strings to be displayed
        - user can add type of cow and parameters after message or answer
        - name of parameters are from the list below

        Prints two cows with their messages

        :param cow: – the available cows can be found by calling list_cows
        :param preset
        :param eyes: eye string
        :param tongue: tongue string
        :param width: width
        :param wrap_text: True or False
        :param cowfile: a string containing the cow file text (chars are not
        decoded as they are in read_dot_cow) if this parameter is provided the
        cow parameter is ignored
        """
        s = shlex.split(args)
        parameters_1 = self.parse_cows_arguments(s[:s.index("reply")])
        parameters_2 = self.parse_cows_arguments(s[s.index("reply") + 1:])
        cow1 = self.cow_from_parameters(cowsay.cowsay, parameters_1)
        cow2 = self.cow_from_parameters(cowsay.cowsay, parameters_2)
        self.draw_two_cows(cow1, cow2)

    def do_cowthink(self, args):
        """
        Same to cowsay
        Usage: cowthink message [cow [param=value ...]] reply answer [cow [param=value ...]]
        - message and answer are strings to be displayed
        - user can add type of cow and parameters after message or answer
        - name of parameters are from the list below

        Prints two cows with their messages

        :param cow: – the available cows can be found by calling list_cows
        :param preset
        :param eyes: eye string
        :param tongue: tongue string
        :param width: width
        :param wrap_text: True or False
        :param cowfile: a string containing the cow file text (chars are not
        decoded as they are in read_dot_cow) if this parameter is provided the
        cow parameter is ignored
        """
        s = shlex.split(args)
        parameters_1 = self.parse_cows_arguments(s[:s.index("reply")])
        parameters_2 = self.parse_cows_arguments(s[s.index("reply") + 1:])
        cow1 = self.cow_from_parameters(cowsay.cowthink, parameters_1)
        cow2 = self.cow_from_parameters(cowsay.cowthink, parameters_2)
        self.draw_two_cows(cow1, cow2)


if __name__ == '__main__':
    cmd_cow().cmdloop() 
