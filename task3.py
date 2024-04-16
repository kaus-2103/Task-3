import sys 
import random
import hmac
import hashlib
from tabulate import tabulate

class Play:
    def __init__(self,inputs):
        self.inputs = inputs
        self.key = self.gen_key()

    def gen_key(self): # key generation 
        return ''.join(random.choices('0123456789ABCDEF0',k=64))
    
    def cal_hmac(self,inpt): #every 'input' for inputs and generating hmac
        move_bytes = bytes(self.inputs[inpt-1],'utf-8')
        key_bytes = bytes.fromhex(self.key)
        return hmac.new(key_bytes,move_bytes,hashlib.sha256).hexdigest()
    
    def move_menu(self):
        print("Available moves:")
        for _,i in enumerate(self.inputs,start=1):
            print(f"{_} - {i}")
        print("0 - exit")
        print("? - help")

    def print_help(self):
            header = ['']+self.inputs
            table = []

            for _ in range(len(self.inputs)):
                row = [self.inputs[_]]
                for i in range(len(self.inputs)):
                    if _ == i:
                        row.append("Draw")
                    elif (i-_) % len(self.inputs) == 1 or (i-_) % len(self.inputs) == 2:
                        row.append("Win")
                    else:
                        row.append("Lose")
                table.append(row)
            print(tabulate(table, header, tablefmt="grid"))

    def user_cmd(self):
        while True:
            try:
                cmd = input("Enter your moves: ")
                if cmd =="0":
                    sys.exit(0)
                elif cmd == "?":
                    self.print_help()
                else:
                    cmd = int(cmd)
                    if 1 <= cmd <= len(self.inputs):
                        return cmd
                    else:
                        print("Error: Invalid move.")
                        print(f"Enter 1 to {len(self.inputs)} for inputing a move. ? for help and 0 for exit")
            except ValueError:
                print(f"Error: Invalid input. Please Try a valid Input. \nSuch as 1 to {len(self.inputs)} for moves , ? for help and 0 for exit")

    def result(self,user_cmd,cpu_turn):
        if user_cmd == cpu_turn:
            return "It's a draw."
        elif (user_cmd+1)%len(self.inputs) == cpu_turn or (user_cmd+2)%len(self.inputs) == cpu_turn:
            return "You win!"
        else:
            return "Computer wins!" 
    
    def start(self):
        print("HMAC:",self.cal_hmac(random.randint(1, len(self.inputs))))
        self.move_menu()
        user_cmd = self.user_cmd()
        cpu_turn = random.randint(1, len(self.inputs))
        print("Your Move:",self.inputs[user_cmd - 1])
        print("Computer Move:", self.inputs(cpu_turn-1))
        result = self.result(user_cmd,cpu_turn)
        print(result)
        print("HMAC key:",self.key)
        
if len(sys.argv[1:]) % 2 == 0 or len(sys.argv) < 3 or len(set(sys.argv[1:])) != len(sys.argv[1:]) :
    print("Error: Please provide an odd number of strings more than three and it must not have repetition.")
    print("For example: \n python task3 rock paper scissors tank plane")

arr = Play(sys.argv[1:])
arr.start()