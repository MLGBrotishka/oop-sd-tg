from loader import dp
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType, Message, InputFile
from states import txt2img

from kafka import KafkaProducer, KafkaConsumer

producer = KafkaProducer(bootstrap_servers='localhost:9092')
consumer = KafkaConsumer('client',bootstrap_servers='localhost:9092')

@dp.message_handler(Command('txt2img'))
async def txt2img_(message: Message):
    await message.answer('Введите описание изображения')
    await txt2img.test1.set()

@dp.message_handler(state = txt2img.test1)
async def state1 (message: Message, state: FSMContext):
    text = message.text
    message_id = message.message_id
    chat_id = message.from_user.id
    key = bytes(str(chat_id), encoding='utf-8')
    value_send = str(message_id) + ' ' + text
    value_send = bytes(value_send, encoding='utf-8')
    producer.send('server', key=key, value=value_send)
    producer.flush()
    await state.finish()
    await message.answer('Ваш запрос обрабатывается')
    for message in consumer:
        if (message.key == key):
            path_to_file = message.value.decode("utf-8")
            break
    photo_bytes = InputFile(path_or_bytesio=path_to_file)
    await dp.bot.send_photo(chat_id=chat_id, photo=photo_bytes)