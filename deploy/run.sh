#!/usr/bin/env sh

git pull
if [ $? -ne 0 ]; then
    echo "Произошла ошибка при выполнении git pull"
    exit 1
fi

docker-compose build
if [ $? -ne 0 ]; then
    echo "Произошла ошибка при выполнении docker-compose build"
    exit 1
fi

docker-compose up -d
if [ $? -ne 0 ]; then
    echo "Произошла ошибка при выполнении docker-compose up -d"
    exit 1
fi

curl -X POST -H 'Content-type: application/json' --data '{"text":"https://hooks.slack.com/services/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"}'
echo "Все шаги завершены успешно"