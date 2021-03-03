# Python template repo with test/release workflow ![pipeline-checks][pl-checks]

The included workflow will...
- perform the following checks on push to master branch
    - code using `pylint` and `flake8`
    - packaging using `setup.py sdist`
    - deploy using `pip install <sdist>`
- create a new release after pushing a tag starting with v*
    - release name and version will be pulled from `setup.py`
    - release body will be message from triggering git tag

## Installation
Installing using `pipx` isolates packages in their own environment and
exposes their entry points on PATH.
```
pipx install https://github.com/vlntnwbr/mendeley-watchdog-beta/releases/latest/download/mendeley-watchdog.tar.gz
```
Alternatively install using
```
pip install https://github.com/vlntnwbr/mendeley-watchdog-beta/releases/latest/download/mendeley-watchdog.tar.gz
```

[pl-checks]: https://github.com/vlntnwbr/mendeley-watchdog/workflows/checks/badge.svg
