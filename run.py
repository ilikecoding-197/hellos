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
from functools import partial
from pathlib import Path

msg = None

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
        msg(f"{lang_name(lang)} {action} succeeded")
    except subprocess.CalledProcessError:
        msg(f"{lang_name(lang)} {action} failed")
     
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
        """
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
        msg = print

    # --clean
    if args.clean:
        delete_folder(BUILD)
        delete_folder(OUT)

        msg("build/out folders cleaned")
        return
        
    prepare_folder(BUILD)
    prepare_folder(OUT)

    msg("Checking for language compilers/interpreters...")
    available = {}

    for tool, exe in TOOLS.items():
        has = have(exe)

        if has:
            msg(f"tool for {lang_name(tool)} exists")
        else:
            msg(f"tool for {lang_name(tool)} doesn't exist")

        available[tool] = has

    msg("\nDone, compiling/running now")

    # C
    if available.get("c"):
        compile(f"{TOOLS['c']} -o {BUILD}/c src/hello.c", "c")
        run(f"{BUILD}/c", "c")

    # CPP
    if available.get("cpp"):
        compile(f"{TOOLS['cpp']} -o {BUILD}/cpp src/hello.cpp", "cpp")
        run(f"{BUILD}/cpp", "cpp")

    # Python
    if available.get("py"):
        run(f"{TOOLS['py']} {SRC}/hello.py", "py")

    # Lua
    if available.get("lua"):
        run(f"{TOOLS['lua']} {SRC}/hello.lua", "lua")

    # Ruby
    if available.get("ruby"):
        run(f"{TOOLS['ruby']} {SRC}/hello.rb", "ruby")

    # JavaScript
    if available.get("js"):
        run(f"{TOOLS['js']} {SRC}/hello.js", "js")

    # Shell
    if available.get("sh"):
        run(f"{TOOLS['sh']} {SRC}/hello.sh", "sh")
        
    # Brainfuck
    bf_out = run_brainfuck(SRC / "hello.bf")
    with (OUT / "bf.txt").open("w") as f:
        f.write(bf_out)
    msg("Assuming BF ran correctly")

    msg("\nDone, checking now.")
    
    all_langs = []
    valid_langs = 0
    
    for file in OUT.glob("*.txt"):
        lang = file.stem  # filename without .txt
        all_langs.append(lang)
    
        result = subprocess.run(
            ["diff", str(file), str(GOOD_FILE)],
            stdout=subprocess.DEVNULL
        )
        if result.returncode == 0:
            msg(f"{lang_name(lang)} valid")
            valid_langs += 1
        else:
            msg(f"{lang_name(lang)} invalid")
            
    if not args.quiet: print()
    print(f"{valid_langs}/{len(all_langs)} languages are valid")

if __name__ == "__main__":
    main()
