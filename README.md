# Инструкция для проверки

1. Клонировать репозиторий:

```git clone git@github.com:sparco114/t_tenzor.git```

2. Перейти в директорию проекта:

```cd t_tenzor```

3. Зпустить виртуальное окружение и установить необходимые зависимости:

```poetry shell```

```poetry install```

4. Запустить тесты (будут выполнены все три скрипта):

```python3 -m pytest --log-cli-level=INFO --log-cli-format="%(filename)s:%(funcName)s - %(asctime)s [%(levelname)s] %(message)s " tests/*```
