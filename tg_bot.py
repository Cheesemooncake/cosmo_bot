import json

import requests
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hlink, hitalic, escape_md, hbold
from aiogram.dispatcher.filters import Text
from config import token, api_key
from main import check_news_update

bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_buttons = ["Last five news", "Fresh news", "Picture of the Day"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.reply("Hello, I'm a bot that can send you the latest space news.\nAlso i can show you NASA picture "
                        "of the day🚀", reply_markup=keyboard)


@dp.message_handler(Text(equals="Last five news"))
async def get_last_five_news(message: types.Message):
    with open("news_dict.json") as file:
        news_dict = json.load(file)

    for k, v in sorted(news_dict.items())[-5:]:
        news = f"{hitalic(v['article_date_time'])}\n\n" \
               f"{hlink(v['article_title'], v['article_url'])}"

        await message.answer(news)


@dp.message_handler(Text(equals="Fresh news"))
async def get_fresh_news(message: types.Message):
    fresh_news = check_news_update()

    if len(fresh_news) >= 1:
        for k, v in sorted(fresh_news.items()):
            news = f"{hitalic(v['article_date_time'])}\n\n" \
                   f"{hlink(v['article_title'], v['article_url'])}"

            await message.answer(news)

    else:
        await message.answer("No news yet")



@dp.message_handler(Text(equals="Picture of the Day"))
async def picture_of_the_day(message: types.Message):
    response = requests.get(f'https://api.nasa.gov/planetary/apod?api_key={api_key}')
    #print(response.status_code)
    if response.status_code == 200:
        data = response.json()
        img_url = data['url']
        img_title = data['title']
        img_desc = data['explanation']
        formatted_title = hbold(img_title)
        formatted_desc = hitalic(img_desc)
        caption = f"{formatted_title}\n\n{formatted_desc}"
        await bot.send_photo(message.chat.id, photo=img_url, caption=caption)
    else:
        await message.answer("An error has occurred. Try again.")


if __name__ == "__main__":
    executor.start_polling(dp)
