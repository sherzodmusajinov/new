import logging
from os import remove
from PIL import Image, ImageFont, ImageDraw
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile, MediaGroup

logging.basicConfig(level=logging.INFO)
bot = Bot('7904405390:AAEop57udFqqO0FWLjVHBoufOM9GdRR1kkY')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class UserState(StatesGroup):
    name = State()

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer('Привет, получите новогодний открытку.')
    await UserState.name.set()
    await message.answer("Введите ваше имя и фамилию:")

@dp.message_handler(state=UserState.name)
async def get_phone(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

        writer_func(data['name'])
    await state.finish()
    await message.answer('Ваш открытка готов! Для его просмотра нажмите /new')

def writer_func(name):
    img1 = Image.open('1.png')
    draw = ImageDraw.Draw(img1)

    font1 = ImageFont.truetype("font.ttf", 85)

    # Получаем bounding box для текста
    bbox = draw.textbbox((0, 0), name.title(), font=font1)
    text_width = bbox[2] - bbox[0]  # Ширина текста

    # Вычисляем позицию для центрирования
    image_width, image_height = img1.size
    position = ((image_width - text_width) // 2, 363)

    draw.text(
        position,
        name.title(),
        fill=(255, 255, 255),  # Белый цвет
        font=font1
    )

    img1.save(f'2025.png')
    print('Сертификат успешно создан и сохранен.')

    @dp.message_handler(commands=['new'])
    async def send_image(message: types.Message):
        media = MediaGroup()
        media.attach_photo(InputFile('2025.png'))
        await bot.send_media_group(chat_id=message.chat.id, media=media)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
