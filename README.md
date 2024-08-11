# fishki_check_auth

Приложение для тестирования аутентификации на учебном стенде

## Стек

- allure-pytest
- selenium

## Установка и настройка

**1** Склонировать репозиторий командой
> **git clone https://github.com/Elegantovich/fishki_check_auth**

**2** Установить Python c [оффициального источника](https://www.python.org/downloads/): 

**3** Cоздать окружение в корне склонированного проекта:
                           
> **python3 -m venv venv**

> активировать его можно командой: **source venv/bin/activate**

> деактивировать можно командой: **deactivate**

**4** Обновить пакетный установщик
> **python3 -m pip install --upgrade pip**  

**5** Установить зависимости: 
> **pip3 install -r requirements.txt**

**6** Создать .env-файл с переменными окружения: 
> **touch .env**

**7** Обогатить .env файл актуальными данными:
> **nano .env**

```
# Среда
ENVIROMENT=PROD
```

**8** Запустить тесты: 
> **pytest -s -v -m regress**

**9** Выгрузить allure-отчёт можно командой 
> **allure serve ./result**

## Директории

> app/ - основной класс приложения
> configs/ - конфигурации приложения
> data/ - какие-либо данные
> pages/ - св-ва, методы и локаторы веб-страниц
> results/ - данные о рез-х прогонов АТ для формирования Allure отчёта
> robot/ - общие методы для работы со всеми объектами
> screenshots/ - скриншоты с фиксацией ошибок
> test/ - тесты  