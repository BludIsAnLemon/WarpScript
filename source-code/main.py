# -----------------------------------------------------------------
import sys
import os
# -----------------------------------------------------------------
from rich.console import Console
# -----------------------------------------------------------------
from rich.text import Text
# -----------------------------------------------------------------
from rich.align import Align
# -----------------------------------------------------------------
from rich.table import Table
# -----------------------------------------------------------------
from rich import print as rprint
# -----------------------------------------------------------------
helpTable = Table(show_lines=True, expand=True)

helpTable.add_column("Methods", justify="center")
helpTable.add_column("What they do", justify="center")

helpTable.add_row("help", "Shows this tab.")
helpTable.add_row("compile", "Compile the output file path and execute it")
# -----------------------------------------------------------------
console = Console()
parsingText = Text("[WS] Parsing...", style="bold yellow")
compilingText = Text("[WS] Compiling to Python...", style="bold yellow")
executingText = Text("[WS] Executing...", style="bold yellow")

parsingText = Align.center(parsingText, vertical="middle")
compilingText = Align.center(compilingText, vertical="middle")
executingText = Align.center(executingText, vertical="middle")
# -----------------------------------------------------------------

print()

compiler_method = ''
# -----------------------------------------------------------------
try:
    compiler_method = sys.argv[1]
except Exception:
    os.system('python main.py help main.py')
    exit()
file_path = ''
# -----------------------------------------------------------------
try:
    file_path = sys.argv[2]
except Exception:
    if not compiler_method == "help":
        rprint("[italic bold red]Please input a filepath!")
    else:
        os.system('python main.py help main.py')
    exit()
# -----------------------------------------------------------------
match compiler_method:
    case 'help':
        console.log(f"[bold green]run python main.py 'method' 'file_path'")
        console.print(helpTable)
        print()
        exit()
    case 'compile':
        console.print(parsingText)
    case _:
        os.system('python main.py help main.py')
        exit()
program_lines = []
try:
    with open(file_path, "r") as file:
        program_lines = [
            line.strip()
                for line in file.readlines()
        ]
except Exception:
    rprint(f"[italic bold red]File Path {file_path} does not exist!")
    exit()
# -----------------------------------------------------------------
console.print(compilingText)

program = []
for line in program_lines:
    parts = line.split(" ")
    opcode = parts[0]

    if opcode == "":
        continue;

    program.append(opcode)

    if opcode == 'say' or opcode == 'ask':
        if parts[1] == "username" or parts[1] == "answer":
            program.append(parts[1])
        else:
            string_literal = ' '.join(parts[1:])[1: -1] or int(parts[1])
            program.append(string_literal)
    elif opcode == 'wait':
        number = int(parts[1])
        program.append(number)
# -----------------------------------------------------------------
py_filepath = f"{file_path[:(len(file_path) - 3)]}.py"
out = open(py_filepath, "w")
# -----------------------------------------------------------------
ip = 0
# -----------------------------------------------------------------
# Import modules for commands
out.write("from rich.console import Console\n")
out.write("from rich.prompt import Prompt\n")
out.write("from os import getlogin\n")
out.write("import time\n\n")
out.write("console = Console()\n\n")
out.write("username = getlogin()\n")
out.write("answer = ''\n\n")
# -----------------------------------------------------------------
while ip < len(program):
    opcode = program[ip]
    ip += 1

    if opcode == "say":
        if program[ip] == "username":
            out.write("console.log(username)\n")
        elif program[ip] == "answer":
            out.write("console.log(answer)\n")
        else:
            out.write(f'console.log(f{repr(program[ip])})\n')
        ip += 1
    elif opcode == "ask":
        if program[ip] == "username" or program[ip] == "answer":
            out.write(f"answer = Prompt.ask({program[ip]})\n")
        else:
            out.write(f'answer = Prompt.ask(f{repr(program[ip])})\n')
        ip += 1
    elif opcode == "wait":
        out.write(f'time.sleep({program[ip]})\n')
        ip += 1
    elif opcode == "stop_this_script":
        out.write("exit()\n")

out.close()
# -----------------------------------------------------------------
console.print(executingText)
print()

os.system(f"python {py_filepath}")
os.remove(py_filepath)
# -----------------------------------------------------------------
print()
rprint("[bold green]Done executing code!")
print()
# -----------------------------------------------------------------
