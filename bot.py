import os
import asyncio
import json
import yaml
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiokafka import AIOKafkaConsumer

# Загружаем переменные окружения из файла .env
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'telegram_messages')
CHAT_IDS = json.loads(os.getenv('CHAT_IDS'))  # Парсим список из строки
json_to_yaml = os.getenv('JSON_TO_YAML', "FALSE").lower() == 'true' # Преобразование строки в булев тип

print(f'Отправка будет вестись в такое число чатов: {len(CHAT_IDS)}')
print(f'Список обрабатываемых чатов: {CHAT_IDS}')
if json_to_yaml:
    print("Сообщения будут переводиться из json в yaml формат перед выводом")
else:
    print("Сообщения будут выводиться в той же форме, как приходят")

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command('info'))
async def send_chat_id(message: types.Message):
    chat_id = message.chat.id
    await message.answer(f"ID этого чата: {chat_id}")

async def consume_kafka_messages():
    # Инициализация Kafka Consumer внутри асинхронной функции
    consumer = AIOKafkaConsumer(
        KAFKA_TOPIC,
        group_id ="bot_reader",
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    # Подключение к Kafka и начало чтения сообщений
    await consumer.start()
    try:
        # Бесконечное чтение сообщений из Kafka
        async for msg in consumer:
            # Распарсиваем JSON сообщение
            message_data = msg.value

            if json_to_yaml:
                # Преобразуем словарь в YAML формат
                yaml_message = yaml.dump(message_data, default_flow_style=False)
                # Отправляем сообщение в Telegram в каждый указанный чат
                for chat_id in CHAT_IDS:
                    await bot.send_message(chat_id=chat_id, text=f"\n{yaml_message}\n", parse_mode="Markdown")
            else:
                for chat_id in CHAT_IDS:
                    await bot.send_message(chat_id=chat_id, text=str(message_data))
            print('Сообщение отправлено')
    finally:
        # Завершение чтения и отключение от Kafka
        await consumer.stop()

async def main():
    # Запуск асинхронной задачи для чтения Kafka сообщений
    asyncio.create_task(consume_kafka_messages())
    # Запуск бота для обработки команд
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    asyncio.run(main())
