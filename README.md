## Api para o projeto pastel de ideias

Está é uma api que se integra com o sistema Pastel de ideias, ela funciona em python com sqlite 3, foi desenvolvida usando **Flask**, **SQL Alchemy** e **Marshmallow**

> https://palletsprojects.com/p/flask/
>https://flask-marshmallow.readthedocs.io/en/latest/
>https://flask-sqlalchemy.palletsprojects.com/en/2.x/

###### Para executar a api, recomendo usar o pipenv
>https://github.com/pypa/pipenv

Após a instalação do pipenv execute os seguintes comandos para instalar as dependencias

` $ pipenv shell` #Para entrar no workflow

` $ pipenv install --dev ` #Para instalar as dependencias

###### Agora que já está dentro do workflow iremos criar o banco de dados com o seguinte comando

`$ python3 createdb.py`

###### Agora para executar a api

`$ python3 app.py`

