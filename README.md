# Генерация изображений
Результат проекта телеграм бот, в котором можно в ответ на запрос подсказки получить изображение сгенерированное Stable Diffusion

## Структура проекта
- [Бот](#bot)
- [Сервер](#server)
- [Обучение](#Learning)

### Телеграм Бот

- [main](/bot/app.py) - Приложение для запуск бота, подлкючается к Kafka и генерирует сообщения


### Сервер

- [server](server/Server.py) - Сервер принимает сообщения через Kafka, генерирует изображение и отправляет ответ также через Kafka

### Обучение

- [train](/Learning/Lab_1.ipynb) - Ноутбук с обучением модели

### Архитектура

![Архитектура](Architecture.png)

### Запуск

Запускается 4 терминалами 

~~~
./kafka/bin/zookeeper-server-start.sh ./kafka/config/zookeeper.properties
~~~

~~~
./kafka/bin/kafka-server-start.sh ./kafka/config/server.properties
~~~

~~~
python3 ./server/Server.py
~~~

~~~
python3 ./bot/app.py
~~~


### Использование

В Телеграм и найти бота по имени - @MAI_OOP_Bot https://t.me/MAI_OOP_Bot
Начать командой /start