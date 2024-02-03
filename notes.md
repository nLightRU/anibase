# PostgreSQL

anibase_admin 1234
anibase_loader 1234

## Users

### Создание

обычно используется GUI утилита

пример с админом и какой-то ролью, которая может только читать

### Granting

Подключаемся к БД к которой хотим дать привелегии

GRANT SELECT ON [table] | ALL TABLES in SCHEMA [schema] to [user]

- Вместо SELECT можно писать UPDATE | DELETE | INSERT
- По умолчанию обычно SCHEMA public

Если мы хотим отозвать привелегию, то пишем REVOKE

Документация

- https://postgrespro.ru/docs/postgresql/9.6/sql-grant
- https://postgrespro.ru/docs/postgresql/9.6/sql-revoke



