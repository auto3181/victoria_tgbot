from aiogram import Bot, Dispatcher, executor, types, filters
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import aioschedule
import random
import pandas as pd
from config import API_TOKEN
from config import FILENAME
from config import bt_names
from config import id_list
from config import nicknames
from config import emoji
excel_data = pd.read_excel(FILENAME, usecols=[0])
data = pd.DataFrame(excel_data)
phrases = data['name'].tolist()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
urlkb = InlineKeyboardMarkup(row_width=1)
urlButton1 = InlineKeyboardButton(text='ТГ', url='https://t.me/esaulov_lev')
urlButton2 = InlineKeyboardButton(text='ВК', url='https://vk.me/esaulov_lev')
urlkb.add(urlButton1, urlButton2)


def check_access(ID):
    if str(ID) in id_list:
        return 1
    else:
        return 0


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text=bt_names[0]),
            types.KeyboardButton(text=bt_names[1]),
            types.KeyboardButton(text=bt_names[2])
        ],
    ]
    if check_access(message.from_user.id):
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
        await message.reply("Привет!\nЯ бот, который создан Львом для Вики. Нажми на кнопки снизу.",
                            reply_markup=keyboard)
    else:
        print(message.from_user.id)
        await message.reply("Вы не Вика")


@dp.message_handler(filters.Text(bt_names[0]))
async def with_puree(message: types.Message):
    await message.reply(phrases[random.randint(1, 154)])


@dp.message_handler(filters.Text(bt_names[1]))
async def upload_photo(message: types.Message):
    await message.answer_photo(types.InputFile(f"photo/{random.randint(1, 48)}.jpg"))


@dp.message_handler(filters.Text(bt_names[2]))
async def url_command(message: types.Message):
    if check_access(message.from_user.id):
        await message.answer('Ссылки на аккаунты:', reply_markup=urlkb)
    else:
        print(message.from_user.id)
        await message.reply("Вы не Вика")


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer("Я пока не знаю данной команды. Обратитесь к Создателю, чтобы он меня научил.")


async def good_night():
    for user in id_list:
        await bot.send_message(chat_id=user, text=f"Спокойной ночи, "
                                                  f"{nicknames[random.randint(0,9)] + emoji[random.randint(0,11)]}")


async def good_morning():
    for user in id_list:
        await bot.send_message(chat_id=user, text=f"Доброе утро, "
                                                  f"{nicknames[random.randint(0,9)] + emoji[random.randint(0,11)]}")


async def scheduler():
    aioschedule.every().day.at("8:30").do(good_morning)
    aioschedule.every().day.at("00:25").do(good_night)

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(dp):
    asyncio.create_task(scheduler())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)