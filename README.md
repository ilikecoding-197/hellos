# hellos

Project simply running a "Hello, world!" program across multiple languages,
with shell scripts to run them.

## Running
There are three shell scripts in this directory, `run.sh`, `check.sh`, and
`all.sh`. `run.sh` compiles/runs the hello world programs, `check.sh`
checks them (wow!) to see if they match the "Hello, world!" from `good.txt`,
and finally `all.sh` runs both `run.sh` and `check.sh`.

## Adding new languages
To add a new language, follow these steps:

1. Add the code file to `src/`
2. Edit run.sh to compile/run your file

`check.sh` already checks out for any language output, so you dont
have to worry about that.
