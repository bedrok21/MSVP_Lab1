import argparse
import random
import string
import sys


def get_symbol():
    if sys.platform.startswith('win'):
        import msvcrt
        return msvcrt.getch().decode()
    else:
        import termios
        import tty
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            symbol = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return symbol


class PasswordGen:
    def __init__(self, args) -> None:
        self.args = args
    
    def generate(self):
        symbols = list(int(self.args.use_lowercase) * string.ascii_lowercase + \
        int(self.args.use_uppercase) * string.ascii_uppercase + \
        int(self.args.use_digits) * string.digits + \
        int(self.args.use_specials) * '!@#$%^&*()-=_+[]{}|;:,.<>?')
        
        setup = [
            list(int(self.args.use_lowercase) * string.ascii_lowercase),
            list(int(self.args.use_uppercase) * string.ascii_uppercase),
            list(int(self.args.use_digits) * string.digits),
            list(int(self.args.use_specials) * '!@#$%^&*()-=_+[]{}|;:,.<>?')
        ]
        setup = [lst for lst in setup if lst]
        
        if not setup:
            setup = [list(string.ascii_lowercase)]
            symbols = string.ascii_lowercase

        if self.args.use_unique:
            if len(symbols) < self.args.length:
                raise ValueError
            
            pwd_symbols = []
            for s in setup:
                pwd_symbols += random.choice(s)
                s.remove(pwd_symbols[-1])

            pwd_symbols += random.sample([el for sub in setup for el in sub], self.args.length - len(setup))

        else:
            pwd_symbols = [random.choice(s) for s in setup]
            
            pwd_symbols += [random.choice([el for sub in setup for el in sub]) for _ in range(self.args.length - len(setup))]
            
        random.shuffle(pwd_symbols)
      
        return ''.join(pwd_symbols)



def main(args):

    pwg = PasswordGen(args=args)

    while True:
        print(pwg.generate(), end='\r')

        symbol = get_symbol()

        if symbol == 'q':
            break



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="qqq")
    parser.add_argument("-l", "--use-lowercase", action="store_true")
    parser.add_argument("-u", "--use-uppercase", action="store_true")
    parser.add_argument("-d", "--use-digits", action="store_true")
    parser.add_argument("-s", "--use-specials", action="store_true")
    parser.add_argument("-r", "--use-unique", action="store_true")
    parser.add_argument("-L", "--length", type=int, default=8)

    args =parser.parse_args()
    main(args)

    