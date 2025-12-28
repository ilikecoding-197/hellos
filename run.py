#!/usr/bin/env python3
#
# run.py - run all files, and check
#
# hello-world - several hello world programs in different languages
# Copyright (C) 2025 ilikecoding-197
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import shutil
import subprocess
import argparse
import sys
from rich.console import Console
from rich.progress import Progress
from rich_argparse import RichHelpFormatter
from functools import partial
from pathlib import Path
from tqdm import tqdm

msg = None
console = Console()

# Helpers
def have(tool_name: str) -> bool:
    """Check if a command-line tool exists in PATH."""
    return shutil.which(tool_name) is not None

def prepare_folder(path: Path) -> None:
    """
    Prepare a folder.

    If `path` already exists, delete all items inside it.
    If it doesn't, create it.
    """
    
    folder = path
    if folder.exists():
        # Delete everything inside
        for item in folder.iterdir():
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()
    else:
        folder.mkdir(parents=True)

def delete_folder(path: str) -> None:
    """Delete a folder."""
    folder = path

    if folder.exists() and folder.is_dir():
        shutil.rmtree(folder)

def run_command(cmd: str, lang: str, action: str = "run") -> None:
    out_file = OUT / f"{lang}.txt"
    try:
        with out_file.open("w") as f:
            subprocess.run(cmd, shell=True, check=True, stdout=f, stderr=subprocess.STDOUT)
        msg(f"[blue]{lang_name(lang)} {action} [green]succeeded")
    except subprocess.CalledProcessError:
        msg(f"[blue]{lang_name(lang)} {action} [red]failed")
     
run = partial(run_command, action="run")
compile = partial(run_command, action="compilation")
    
def lang_name(lang):
    return LANG_NAMES.get(lang, lang)

# Intergrated Brainfuck runner because its so simple
# we might as well include it in here
def run_brainfuck(path: Path):
    with path.open("r") as f:
        code = f.read()
        
    array = [0] * 10 # we dont need much space
    pointer_location = 0
    instruction_pointer = 0
    output = ""
    
    while instruction_pointer < len(code):
        command = code[instruction_pointer]

        if command == '>':
            pointer_location += 1
        elif command == '<':
            pointer_location -= 1
        elif command == '+':
            array[pointer_location] = (array[pointer_location] + 1) % 256
        elif command == '-':
            array[pointer_location] = (array[pointer_location] - 1) % 256
        elif command == '.':
            output += chr(array[pointer_location])
        # no , command - we dont need it
        elif command == '[':
            if array[pointer_location] == 0:
                loop_count = 1
                while loop_count > 0:
                    instruction_pointer += 1
                    if code[instruction_pointer] == '[':
                        loop_count += 1
                    elif code[instruction_pointer] == ']':
                        loop_count -= 1
        elif command == ']':
            if array[pointer_location] != 0:
                loop_count = 1
                while loop_count > 0:
                    instruction_pointer -= 1
                    if code[instruction_pointer] == ']':
                        loop_count += 1
                    elif code[instruction_pointer] == '[':
                        loop_count -= 1
        
        instruction_pointer += 1

    return output

# Constants
BUILD = Path("build")
OUT   = Path("out")
SRC   = Path("src")

TOOLS = {
    "c"    : "gcc",
    "cpp"  : "g++",
    "py"   : "python3",
    "js"   : "node",
    "sh"   : "sh",
    "lua"  : "lua",
    "ruby" : "ruby"
}

LANG_NAMES = {
    "c"   : "C",
    "cpp" : "C++",
    "py"  : "Python",
    "js"  : "JavaScript",
    "sh"  : "Shell",
    "lua" : "Lua",
    "ruby": "Ruby",
    "bf"  : "Brainfuck"
}

GOOD_FILE = Path("good.txt")

def main() -> None:
    """Main function."""
    
    # Arguments
    parser = argparse.ArgumentParser(
        description="Run/check all hello world programs",
        prog="run",
        epilog="""
        "hello-world" made by ilikecoding-197
        See README.md for more information
        """,
        formatter_class=RichHelpFormatter
    )
    
    parser.add_argument(
        "--clean",
        "-c",
        action="store_true",
        help="Delete build/out folders and do nothing else"
    )

    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Silence all messages except for final validity output"
    )

    args = parser.parse_args()

    # --quiet
    # if args.quiet, msg will be a no-op, else a print
    global msg
    if args.quiet:
        msg = lambda *a, **k: None
    else:
        msg = lambda *a, **k: console.print(*a, **k)

    # --clean
    if args.clean:
        delete_folder(BUILD)
        delete_folder(OUT)

        msg("[green bold]build/out folders cleaned")
        return
        
    prepare_folder(BUILD)
    prepare_folder(OUT)

    with Progress(transient=True) as progress:
        global console
        console = progress.console

        task = progress.add_task("[bold green]Checking for tools...", total=len(TOOLS))
        msg("[bold]Checking for language compilers/interpreters...")
        available = {}

        for tool, exe in TOOLS.items():
            has = have(exe)

            if has:
                msg(f"tool for [blue]{lang_name(tool)} [yellow]exists")
            else:
                msg(f"tool for [blue]{lang_name(tool)} [red]doesn't exist")

            available[tool] = has
            progress.update(task, advance=1)

        progress.remove_task(task)
        msg("\n[bold]Done, compiling/running now")

        # compute totals
        total = 1 # integrated BF
        if available.get("c"): total += 2
        if available.get("cpp"): total += 2
        if available.get("py"): total += 1
        if available.get("lua"): total += 1
        if available.get("ruby"): total += 1
        if available.get("js"): total += 1
        if available.get("sh"): total += 1


        task = progress.add_task("[bold green]Compiling/running...", total=total)
        
        # C
        if available.get("c"):
            compile(f"{TOOLS['c']} -o {BUILD}/c src/hello.c", "c")
            progress.update(task, advance=1)
            run(f"{BUILD}/c", "c")
            progress.update(task, advance=1)

        # CPP
        if available.get("cpp"):
            compile(f"{TOOLS['cpp']} -o {BUILD}/cpp src/hello.cpp", "cpp")
            progress.update(task, advance=1)
            run(f"{BUILD}/cpp", "cpp")
            progress.update(task, advance=1)

        # Python
        if available.get("py"):
            run(f"{TOOLS['py']} {SRC}/hello.py", "py")
            progress.update(task, advance=1)

        # Lua
        if available.get("lua"):
            run(f"{TOOLS['lua']} {SRC}/hello.lua", "lua")
            progress.update(task, advance=1)

        # Ruby
        if available.get("ruby"):
            run(f"{TOOLS['ruby']} {SRC}/hello.rb", "ruby")
            progress.update(task, advance=1)

        # JavaScript
        if available.get("js"):
            run(f"{TOOLS['js']} {SRC}/hello.js", "js")
            progress.update(task, advance=1)
        
        # Shell
        if available.get("sh"):
            run(f"{TOOLS['sh']} {SRC}/hello.sh", "sh")
            progress.update(task, advance=1)
            
        # Brainfuck
        bf_out = run_brainfuck(SRC / "hello.bf")
        with (OUT / "bf.txt").open("w") as f:
            f.write(bf_out)
        msg("[gray]Assuming BF ran correctly")
        progress.update(task, advance=1)

        msg("\n[bold]Done, checking now.")
        progress.remove_task(task)
        
        all_langs = []
        valid_langs = 0
        glob = list(OUT.glob("*.txt"))

        task = progress.add_task("Checking output...", total=len(glob))
        for file in glob:
            lang = file.stem  # filename without .txt
            all_langs.append(lang)
        
            result = subprocess.run(
                ["diff", str(file), str(GOOD_FILE)],
                stdout=subprocess.DEVNULL
            )
            if result.returncode == 0:
                msg(f"[blue]{lang_name(lang)} [green]valid")
                valid_langs += 1
            else:
                msg(f"[blue]{lang_name(lang)} [red]invalid")

            progress.update(task, advance=1)
        progress.remove_task(task)
    console.print(f"[blue]{valid_langs}/{len(all_langs)}[/] languages are valid")

if __name__ == "__main__":
    main()
