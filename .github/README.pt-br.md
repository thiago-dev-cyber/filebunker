<h1 align="center">File Bunker</h1> 

[English version](https://github.com/thiago-dev-cyber/filebunker/blob/dev/.github/README.md)

<p align="center">
  <img src="http://img.shields.io/static/v1?label=python&message=3.11.2&color=blue&style=for-the-badge&logo=python"/>
  <img src="http://img.shields.io/static/v1?label=STATUS&message=EM%20DESENVOLVIMENTO&color=RED&style=for-the-badge"/>
  <img src="http://img.shields.io/static/v1?label=License&message=MIT&color=green&style=for-the-badge"/>
</p>

> Status do Projeto: :heavy_check_mark: :warning: (em desenvolvimento)

### Tópicos 

:small_blue_diamond: [Descrição do projeto](#descrição-do-projeto)

:small_blue_diamond: [Funcionalidades](#funcionalidades)

:small_blue_diamond: [Deploy da Aplicação](#deploy-da-aplicação-dash)

:small_blue_diamond: [Pré-requisitos](#pré-requisitos)

:small_blue_diamond: [Como rodar a aplicação](#como-rodar-a-aplicação-arrow_forward)


## Descrição do projeto 

<p align="justify">
  Guarde seus arquivos na nuvem com privacidade. O <b>File Bunker</b> criptografa cada arquivo com uma chave diferente antes de enviá-los para a nuvem! 
</p>

## Funcionalidades

:heavy_check_mark: Criptografia individual dos arquivos.

## Pré-requisitos

:warning: [Python](https://www.python.org/)

    - pycryptodome
    - mega.py
    - python-dotenv
    

## Como rodar a aplicação :arrow_forward:

Na URL oficial do repositório ([https://github.com/thiago-dev-cyber/filebunker](https://github.com/thiago-dev-cyber/filebunker)) Faça um fork do projeto para o seu próprio GitHub e então, no terminal, clone o projeto:

```bash
git clone https://github.com/<YOUR_GITHUB_USERNAME>/filebunker.git
```

Em seguida, navegue até o diretório do projeto:

```bash
cd filebunker
```

Instale o  [uv](https://docs.astral.sh/uv/) use o pip (não recomendado) ou siga a  **documentação oficial** (ALTAMENTE RECOMENDADO) e sincronize as dependências (o uv cria e gerencia automaticamente um .venv, então você não precisa):

```bash
uv sync
```

Agora use `uv run` para executar os comandos desejados. Eles serão executados usando o `.venv` também (por exemplo, `python3 -m pytest` ou `pytest` agora se torna `uv run pytest`)

## Resolvendo Problemas :exclamation:

Em [issues]() foram registrados alguns problemas gerados durante o desenvolvimento deste projeto e como foram resolvidos. 

## Tarefas em aberto

Se for o caso, liste tarefas/funcionalidades que ainda precisam ser implementadas na sua aplicação:

:memo: Terminar de configurar o conector  mega. 


## Desenvolvedores/Contribuintes :octocat:

| [<img src="https://img.freepik.com/premium-vector/mexican-men-avatar_7814-348.jpg?semt=ais_hybrid" width=115><br><sub> Thiago-Dev</sub>](https://github.com/thiago-dev-cyper) |   
| :---: |

## Licença 

A [MIT License]() (MIT)

Copyright :copyright: 2025 - File Bunker
