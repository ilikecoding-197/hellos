# hello-world

Project simply running a "Hello, world!" program across multiple languages,
with a python script to run them.

## Running
1. Clone the repo:

   ```bash
   git clone https://github.com/ilikecoding-197/hello-world.git
   ```

   If you dont have Git installed, install it before.
2. Make sure you have Python3 and venv installed on it, create one, and install
   packages:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate # or whatever it is on your OS
   pip install -r requirements.txt
   ```
3. Finally, run the main script (most of the time you want just `./run.py`)
   ```bash
   ./run.py    # normal run
   ./run.py -q # quiet
   ./run.py -c # clean, delete build and out
   ./run.py -h # get help
   ```

## Adding new languages
First, create a fork of this repo. Then follow these steps
to get your language in there.

1. Add the code file to `src/`
2. Make sure you put this kind of comment at the top of the file:

   ```python
   # hello-world language
   # author:   [YOUR GITHUB NAME]
   # language: [LANGUAGE]
   #
   # hello-world created by ilikecoding-197
   # see README.md in project root
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
   ```

   Replace the info in `author` and `language`! Make sure to use
   the exact format, but of course change the comment symbol
   if needed. Include the license.
3. Edit `run.py`. Add the tool to compile/interpret your language
   into the TOOLS dictionary (format: `[tool]: [exec_name]`),
   add the language next to the others in the `main` function.
   Also, add a human-friendly name into the LANG_NAMES
   dictionary for your language. Make sure to test the changes!
   And actually, once another thing - make sure to add code
   to increment the total counter for the compiling/running
   progress bar (another if for your language)
4. Add instructions in `README.md` on how to install the tool
   for your language

After adding the language(s), create a pull request to the
actual repo from your fork. Include the language(s) you
added in the title of that PR.

## Tools you might have to install
| Language | Tool                          |
|----------|-------------------------------|
| C        | gcc                           |
| C++      | g++                           |
| Python   | python3                       |
| JS       | node                          |
| Lua      | lua (any version should work) |
| Ruby     | ruby                          |

Search online on how to install each tool for your distro,
if your package manager doesn't have it under the tool name
(e.g. `sudo apt install node` fails)
