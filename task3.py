import sys 
import random
import hmac
import hashlib
from tabulate import tabulate

class Generator: # key generation 
    def __init__(self,inputs):
        self.inputs=inputs

    @staticmethod
    def gen_key(): 
        return ''.join(random.choices('0123456789ABCDEF0',k=64))
    
    def cal_hmac(self,inpt,key): #every 'input' for inputs and generating hmac
        move_bytes = bytes(self.inputs[inpt-1],'utf-8')
        key_bytes = bytes.fromhex(key)
        return hmac.new(key_bytes,move_bytes,hashlib.sha256).hexdigest()

class Table: #drawing table
    def __init__(self, inputs):
        self.inputs = inputs

    def print_help(self):
        header = ['']+self.inputs
        table = []

        moves_count = len(self.inputs)
    
        for idx, current_move in enumerate(self.inputs):
            row = [current_move]
            for next_move_idx in range(moves_count):
                distance = (next_move_idx - idx) % moves_count
                if distance == 0:  # If the distance is zero, it's a draw
                    row.append("Draw")
                elif distance <= moves_count // 2:  # If the distance is less than or equal to half of the moves count
                    row.append("Win")
                else:
                    row.append("Lose")
            table.append(row)
    
        print(tabulate(table, header, tablefmt="grid"))


class Result: #for user commands and its result
    def __init__(self, inputs, key):
        self.inputs = inputs
        self.key = key

    def user_cmd(self):
        while True:
            try:
                cmd = input("Enter your moves: ")
                if cmd =="0":
                    sys.exit(0)
                elif cmd == "?":
                    Table(self.inputs).print_help()
                else:
                    cmd = int(cmd)
                    if 1 <= cmd <= len(self.inputs):
                        return cmd
                    else:
                        print("Error: Invalid move.")
                        print(f"Enter 1 to {len(self.inputs)} for inputting a move. ? for help and 0 for exit")
            except ValueError:
                print(f"Error: Invalid input. Please Try a valid Input. \nSuch as 1 to {len(self.inputs)} for moves , ? for help and 0 for exit")

    def result(self,user_cmd,cpu_turn):
        distance = (cpu_turn-user_cmd) % len(self.inputs)
        if distance == 0:
            return "It's a draw."
        elif distance<= len(self.inputs)//2:
            return "You win!"
        else:
            return "Computer wins!"
 

class Play: #main menu classs
    def __init__(self, inputs):
        self.inputs = inputs
        self.key = Generator.gen_key()
        Gen = Generator(self.inputs)
        self.cal_hmac=Gen.cal_hmac(random.randint(1, len(self.inputs)),self.key)


    def move_menu(self):
        print("Available moves:")
        for _,i in enumerate(self.inputs,start=1):
            print(f"{_} - {i}")
        print("0 - exit")
        print("? - help")

    def start(self):
        print("HMAC:",self.cal_hmac)
        self.move_menu()
        user_cmd = Result(self.inputs, self.key).user_cmd()
        cpu_turn = random.randint(1, len(self.inputs))
        # cpu_turn = 7
        print("Your Move:",self.inputs[user_cmd - 1])
        print("Computer Move:", self.inputs[cpu_turn-1])
        result = Result(self.inputs, self.key).result(user_cmd,cpu_turn)
        print(result)
        print("HMAC key:",self.key)

if len(sys.argv[1:]) % 2 == 0 or len(sys.argv) < 3 or len(set(sys.argv[1:])) != len(sys.argv[1:]) :
    print("Error: Please provide an odd number of strings more than three and it must not have repetition.")
    print("For example: \n python task3 rock paper scissors tank plane")
else:
    arr = Play(sys.argv[1:])
    arr.start()

# Gen() -> gen_key(),cal_hmac(inpt in inputs)
# Table(arr) ->  print_help()
# Result(arr,key) -> user_cmd(),result(user_cmd,cpu_turn)
# Play(arr) -> move_menu(),start()