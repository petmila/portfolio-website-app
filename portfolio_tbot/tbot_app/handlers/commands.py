from aiogram import types

from tbot_app import messages

from tbot_app.app import dp


@dp.message_handler(commands=["start"])
async def send_welcome(message_: types.Message):
    await message_.answer(messages.WELCOME_MESSAGE)
