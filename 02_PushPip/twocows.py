import argparse
from cowsay import cowsay, list_cows

parser = argparse.ArgumentParser(
    description="Generates an ASCII image of a 2 cows saying the given text",
)

parser.add_argument(
    "-e",
    type=str,
    help="An eye string for the first cow",
    dest="eyes_1",
    default ='oo',
    metavar="eye_string_1",
)

parser.add_argument(
    "-E",
    type=str,
    help="An eye string for the second cow",
    dest="eyes_2",
    default ='oo',
    metavar="eye_string_2",
)

parser.add_argument(
    "-f", 
    type=str, 
    metavar="cowfile_1",
    help="Either the name of a cow specified in the COWPATH, "
         "or a path to a cowfile (if provided as a path, the path must "
         "contain at least one path separator)",
)

parser.add_argument(
    "-F",
    type=str,
    metavar="cowfile_2",
    help="Either the name of a cow specified in the COWPATH, "
         "or a path to a cowfile (if provided as a path, the path must "
         "contain at least one path separator)",
)

parser.add_argument(
    "-l", action="store_true",
    help="Lists all cows in the cow path and exits"
)

parser.add_argument(
    "-n", action="store_false",
    help="If given, text in the speech bubble of the first cow will not be wrapped"
)

parser.add_argument(
    "-N", action="store_false",
    help="If given, text in the speech bubble of the second cow will not be wrapped"
)

parser.add_argument(
    "-T", type=str, dest="tongue",
    help="A tongue string. This is ignored if a preset mode is given",
    default='  ', metavar="tongue_string"
)
parser.add_argument(
    "-W", type=int, default=40, dest="width", metavar="column",
    help="Width in characters to wrap the speech bubble (default 40)",
)

group = parser.add_argument_group(
    title="Mode",
    description="There are several out of the box modes "
                "which change the appearance of the cow. "
                "If multiple modes are given, the one furthest "
                "down this list is selected"
)
group.add_argument("-b", action="store_const", const="b", help="Borg")
group.add_argument("-d", action="store_const", const="d", help="dead")
group.add_argument("-g", action="store_const", const="g", help="greedy")
group.add_argument("-p", action="store_const", const="p", help="paranoid")
group.add_argument("-s", action="store_const", const="s", help="stoned")
group.add_argument("-t", action="store_const", const="t", help="tired")
group.add_argument("-w", action="store_const", const="w", help="wired")
group.add_argument("-y", action="store_const", const="y", help="young")

parser.add_argument(
    "--random", action="store_true",
    help="If provided, picks a random cow from the COWPATH. "
         "Is superseded by the -f option",
)

parser.add_argument(
    "message_1", default=None, nargs='?',
    help="The message to include in the speech bubble. "
         "If not given, stdin is used instead."
)

parser.add_argument(
    "message_2", default=None, nargs='?',
    help="The message to include in the speech bubble. "
         "If not given, stdin is used instead."
)

def get_preset(args):
    return (
            args.y or args.w or args.t or args.s
            or args.p or args.g or args.d or args.b
    )

args = parser.parse_args()
if args.l:
    print("\n".join(list_cows()))
else:
    cow1 = cowsay(message=args.message_1, 
                  cow=args.f, 
                  preset=get_preset(args),
                  eyes=args.eyes_1,
                  tongue=args.tongue,
                  width=args.width,
                  wrap_text=args.n,
                  ).split('\n')
    cow2 = cowsay(message=args.message_2,
                  cow=args.F, 
                  preset=get_preset(args),
                  eyes=args.eyes_2,
                  tongue=args.tongue,
                  width=args.width,
                  wrap_text=args.N,
                  ).split('\n')
    dif = abs(len(cow2) - len(cow1))
    if len(cow1) > len(cow2):
        cow2 = [''] * dif  + cow2
    else:
        cow1 = [''] * dif + cow1
    max_len_1 = max([len(i) for i in cow1])
    max_len_2 = max([len(i) for i in cow2])
    print('\n'.join([f'{i[0]:<{max_len_1}}{i[1]:<{max_len_2}}' for i in zip(cow1, cow2)]))
