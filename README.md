# kanastra

Para rodar o projeto de nome 'kanastra' navegue até a pasta canastra e inicialize os container docker->

        Instale o docker em seu ambiente
        execute o comando - 'docker compose up'

em seguida execute o comando que configura o banco de dados dentro do container ->

        'docker compose exec backend python manage.py migrate'

Para processar um arquivo csv , utilizando o postman ->

    instale o postman em seu ambiente
    selecione o metodo como POST
    use a URL: http://localhost:8000/charge/create-charge/
    na aba Body, selecione form-data
    Adicione uma chave(key) com nome 'file', no valor selecione o arquivo CSV em sua maquina

Foi utilizado logs no nível de WARNING para que seja de fácil visualização no container docker

A funcionalidade para envio de emails foi feita atravé de uma tarefa agendada que roda a cada 1 minuto

para rodar testes (que estao dentro da pasta tests) ->
no arquivo settings.py, alterar o host do database para localhost
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "admin",
        "USER": "user",
        "PASSWORD": "root",
        "HOST": "db", --> "localhost",
        "PORT": "3306",
    }
}

fornecer privilégios para o usuário no banco de dados->

docker exec -it kanastra-db-1 mysql -u root -p
GRANT ALL PRIVILEGES ON test_admin.* TO 'user'@'%';
FLUSH PRIVILEGES;
