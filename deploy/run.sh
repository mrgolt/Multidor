git pull

# Проверка успешности git pull
if [ $? -ne 0 ]; then
    echo "Произошла ошибка при выполнении git pull"
    exit 1
fi

# Шаг 2: Сборка Docker-образов
docker-compose build

# Проверка успешности сборки
if [ $? -ne 0 ]; then
    echo "Произошла ошибка при выполнении docker-compose build"
    exit 1
fi

# Шаг 3: Запуск Docker-контейнеров
docker-compose up -d

# Проверка успешности запуска
if [ $? -ne 0 ]; then
    echo "Произошла ошибка при выполнении docker-compose up -d"
    exit 1
fi

curl -X POST -H 'Content-type: application/json' --data '{"text":"New deploy from Git is successful"}' https://hooks.slack.com/services/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

echo "Все шаги завершены успешно"