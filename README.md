# barebones-python-module

Barebones python3 module with testing and logging environment

## Environment

This repo contains the environment to start coding with an enabled App module (main program), a Logger (logging capabilities), and Tests (using pytest). It has been set up so modules can be imported from anywhere without braking the application.

## Settings

Global settings should be configured in `module_config.py` as it is on the root directory.

## Venv

Create an environment and pull modules from `modules.txt`.

- Run as a script:

```shell
$ python -m venv Venv
$ source /Venv/bin/activate
$ (python) pip install -r requirements.txt
```

- Run manually:

```shell
$ python -m venv Venv
$ source /Venv/bin/activate
$ (python) pip install -r requirements.txt
```

# Add me as a submodule:

```shell
mkdir barebones-python-module
cd barebones-python-module/
git init
git submodule add https://github.com/sdmunozsierra/barebones-python-module
cat .gitmodules
git add .gitmodules barebones-python-module
git commit -m "added barebones-python-module as a submodule"
```

```bash
#!/bin/bash
mkdir barebones-python-module
cd barebones-python-module/
git init
git submodule add https://github.com/sdmunozsierra/barebones-python-module
cat .gitmodules
git add .gitmodules barebones-python-module
git commit -m "added barebones-python-module as a submodule"
```

# Fork Me:
