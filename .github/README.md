<h1 align="center">File Bunker</h1>

[Versão em Português](https://github.com/thiago-dev-cyber/filebunker/blob/dev/README.pt-br.md)

<p align="center">
  <img src="http://img.shields.io/static/v1?label=python&message=3.11.2&color=blue&style=for-the-badge&logo=python"/>
  <img src="http://img.shields.io/static/v1?label=STATUS&message=IN%20DEVELOPMENT&color=RED&style=for-the-badge"/>
  <img src="http://img.shields.io/static/v1?label=License&message=MIT&color=green&style=for-the-badge"/>
</p>

> Project Status: :heavy_check_mark: :warning: (in development)

### Topics

:small_blue_diamond: [Project Description](#project-description)

:small_blue_diamond: [Features](#features)

:small_blue_diamond: [Application Deployment](#application-deployment-dash)

:small_blue_diamond: [Prerequisites](#prerequisites)

:small_blue_diamond: [How to Run the Application](#how-to-run-the-application-arrow_forward)

## Project Description

<p align="justify">
  Store your files in the cloud with privacy. <b>File Bunker</b> encrypts each file with a different key before uploading them to the cloud!
</p>

## Features

:heavy_check_mark: Individual encryption of files.

## Prerequisites

:warning: [Python](https://www.python.org/)

    - pycryptodome
    - mega.py
    - python-dotenv

## How to Run the Application :arrow_forward:

At the official repo URL ([https://github.com/thiago-dev-cyber/filebunker](https://github.com/thiago-dev-cyber/filebunker)) fork the project to your own GitHub and the, in the terminal, clone the project:

```bash
git clone https://github.com/<YOUR_GITHUB_USERNAME>/filebunker.git
```

Then navigate to the project directory:

```bash
cd filebunker
```

Install [uv](https://docs.astral.sh/uv/) using pip (not recommended) or following the **official documentation** (HIGHLY RECOMMENDED) and sync the dependencies (uv creates and handles automatically a `.venv` so you do not need to):

```bash
uv sync
```

Now use `uv run` to run the desired commands. They will be executed using `.venv` as well (e.g. `python3 -m pytest` or `pytest` now becames `uv run pytest`).

## Troubleshooting :exclamation:

Some issues encountered during the development of this project and how they were resolved are documented in issues.

## Open Tasks

If applicable, list tasks/features that still need to be implemented in your application:

- :memo: Finish configuring the Mega connector.

## Developers/Contributors :octocat:

| <img src="https://img.freepik.com/premium-vector/mexican-men-avatar_7814-348.jpg?semt=ais_hybrid" width=115><br><sub> Thiago-Dev</sub> |
| :------------------------------------------------------------------------------------------------------------------------------------: |

## License

The [MIT License](https://github.com/thiago-dev-cyber/filebunker/blob/main/LICENSE)

Copyright :copyright: 2025 - File Bunker
