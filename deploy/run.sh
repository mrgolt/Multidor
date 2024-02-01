#!/usr/bin/env sh

cd ../

git pull

if [ $? -eq 0 ]; then
  echo "Готово"
else
  echo "Произошла ошибка при выполнении git pull"
fi