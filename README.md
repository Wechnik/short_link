# Short link
Сервис для сокращения ссылок



docker run --name short_link -p 5434:5432 -d -e POSTGRES_USER='short_link' -e POSTGRES_PASSWORD='short_link' -e POSTGRES_DB='short_link' postgres:11