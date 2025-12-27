#!/usr/bin/env python3
# run.py - run all files, and check

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

def prepare_folder(path: str) -> None:
    """
    Prepare a folder.

    If `path` already exists, delete all items inside it.
    If it doesn't, create it.
    """
    
    folder = Path(path)
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
    folder = Path(path)

    if folder.exists() and folder.is_dir():
        shutil.rmtree(folder)

def run_command(cmd: str, lang: str, action: str = "run") -> None:
    out_file = Path(OUT) / f"{lang}.txt"
    try:
        with out_file.open("w") as f:
            subprocess.run(cmd, shell=True, check=True, stdout=f, stderr=subprocess.STDOUT)
        msg(f"{lang} {action} succeeded")
    except subprocess.CalledProcessError:
        msg(f"{lang} {action} failed")
     
run = partial(run_command, action="run")
compile = partial(run_command, action="compilation")

# Constants
BUILD = "build"
OUT   = "out"
SRC   = "src"

TOOLS = {
    "c"   : "gcc",
    "cpp" : "g++",
    "py"  : "python3",
    "js"  : "node",
    "sh"  : "sh"
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
            msg(f"tool for {tool} exists")
        else:
            msg(f"tool for {tool} doesn't exist")

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

    # JavaScript
    if available.get("js"):
        run(f"{TOOLS['js']} {SRC}/hello.js", "js")

    # Shell
    if available.get("sh"):
        run(f"{TOOLS['sh']} {SRC}/hello.sh", "sh")

    msg("\nDone, checking now.")
    
    all_langs = []
    valid_langs = 0
    
    for file in Path(OUT).glob("*.txt"):
        lang = file.stem  # filename without .txt
        all_langs.append(lang)
    
        result = subprocess.run(
            ["diff", str(file), str(GOOD_FILE)],
            stdout=subprocess.DEVNULL
        )
        if result.returncode == 0:
            msg(f"{lang} valid")
            valid_langs += 1
        else:
            msg(f"{lang} invalid")
            
    if not args.quiet: print()
    print(f"{valid_langs}/{len(all_langs)} languages are valid")

if __name__ == "__main__":
    main()
