#!/usr/bin/env sh

GIT_REF=${1}
GIT_DIR=${2}
PUID=${3}
PGID=${4}

chown -R ${PUID}:${PGID} ${GIT_DIR}

cd ..

git pull

if [ $? -eq 0 ]; then
  echo "Готово"
else
  echo "Произошла ошибка при выполнении git pull"
fi