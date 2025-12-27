# hello-world

Project simply running a "Hello, world!" program across multiple languages,
with a python script to run them.

## Running
Simply run `run.py` (you can run it as `./run.py`) to compile/run
the languages it can. There are a couple options you can use with it,
run it with `-h` or `--help` to check them out.

## Adding new languages
To add a new language, follow these steps:

1. Add the code file to `src/`
2. Make sure you put this kind of comment at the top of the file:

   ```python
   # hello-world language
   # author:   [YOUR GITHUB NAME]
   # language: [LANGUAGE]
   #
   # hello-world created by ilikecoding-197
   # see README.md in project root
   ```

   Replace the info in `author` and `language`! Make sure to use
   the exact format, but of course change the comment symbol
   if needed.
2. Edit `run.py`. Add the tool to compile/interpret your language
   into the TOOLS dictionary (format: `[tool]: [exec_name]`),
   add the language next to the others in the `main` function.
   Make sure to test the changes.
3. Add instructions in `README.md` on how to install the tool
   for your language

## Tools you might have to install
| Language | Tool    |
|----------|---------|
| C        | gcc     |
| C++      | g++     |
| Python   | python3 |
| JS       | node    |

Search online on how to install each tool, if your package
manager doesn't have it under the tool name (e.g. `sudo apt install node`
fails)
