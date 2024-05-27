
Итоговый бот был собран и залит на докерхаб. Готовый образ можно стянуть следующей командой: `docker pull koldim2001/tg_bot_kafka:1.0`

Контейнер с ботом в вашем проекте может стать одним из сервисов, который можно будет удобно подключить в docker-compose.yaml

Пример докер компоуз файла, содержащего все необходимые иструменты (см файл docker-compose.yaml в репозитории), можно запустить данной командой:
```
docker-compose -p test_kafka up -d
```
 Только перд запуском необходимо внести изменения в переменные окружения:

```
  tg_bot_kafka:
    image: koldim2001/tg_bot_kafka:1.0
    container_name: tg_bot_kafka
    restart: always
    depends_on:
      - kafka
    environment:
      - BOT_TOKEN=???????????????????????????????
      - CHAT_IDS=["?????????"]
      - KAFKA_BOOTSTRAP_SERVERS=kafka:29092
      - KAFKA_TOPIC=tg_bot_data
      - JSON_TO_YAML=TRUE
```

Пример необходимых переменных окружения для запуска проекта:


| Переменная окружения | Описание | Пример задания |
| --- | --- | --- |
| `BOT_TOKEN` | Токен бота, используемый для аутентификации в Telegram API. | `BOT_TOKEN=12345:ABCDEFGHIJKLMNOPQ` |
| `CHAT_IDS` | Список идентификаторов чатов, в которые бот будет отправлять сообщения. | `CHAT_IDS=["111111","222222"]` |
| `KAFKA_BOOTSTRAP_SERVERS` | Сервер Kafka, к которому будет подключаться бот для чтения сообщений. | `KAFKA_BOOTSTRAP_SERVERS=kafka:29092` |
| `KAFKA_TOPIC` | Топик Kafka, из которого бот будет читать сообщения. | `KAFKA_TOPIC=tg_bot_data` |
| `JSON_TO_YAML` | Флаг, определяющий, будут ли JSON сообщения преобразовываться в более читабельный вид перед отправкой в Telegram. Если `TRUE`, то сообщения будут преобразованы. Если `FALSE`, то сообщения будут отправлены ровно так, как и были посланы в Kafka. | `JSON_TO_YAML=TRUE` |

Чтобы узнать chat_id, необходимо после запуска компоуза добавить бота в желаемый чат и отправить в команду ```/info```. Бот выведет номер чата. Этот номер необходимо будет указать в переменных окружения перед запуском docker compose. 

Помимо этого есть еще вариант Как узнать идентификатор chat_id без бота и кода - [ссылка](https://pikabu.ru/story/kak_uznat_identifikator_telegram_kanalachatagruppyi_kak_uznat_chat_id_telegram_bez_botov_i_koda_11099278)

