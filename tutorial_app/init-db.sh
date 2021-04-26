#!/bin/sh

docker run -d --name fastapi-db \
    -p 3306:3306 \
    -e MYSQL_ROOT_PASSWORD=1234 \
    -e MYSQL_DATABASE=dev \
    -e MYSQL_USER=admin \
    -e MYSQL_PASSWORD=1234 \
    mysql:8.0 --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci