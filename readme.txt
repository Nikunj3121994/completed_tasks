Демка с тестовыми заданиями.
В данный момент, есть калькулятор и загрузка файлов, фото в скором времени парсер из json/xml(rss)/что-то там в модели проекта.
Т.з в tasks.txt
Из библиотек необходимо поставить под pillow  sudo apt-get install  python-dev libjpeg8-dev
TODO: pep8 код, переделать restframework view и url под viewsets, растащить angular на модули. Сделать незавимые импорты js. Добавить тесты.Посмотреть как ведет себя $event в firefox

перед использованием поставить пакеты
из папки с проектом
sudo apt-get install $(cat ./packages.list)
Сделать virtual-env
virtualenv --no-site-packages .venv
source .venv/bin/activate
Поставить python пакеты
pip install -r requirements.pip
Создать юзера в postgres
sudo -u postgres psql -c "CREATE USER kmut SUPERUSER ENCRYPTED PASSWORD 'dummy';"
Создать базу данных под проект
sudo -u postgres psql -c "CREATE DATABASE completed_task ENCODING 'UTF8' OWNER dummy;"
Синхронизировать базу
python ./manage.py migrate
Создать суперпользователя
python ./manage.py createsuperuser
Запустить сервер
python ./manage.py runserver