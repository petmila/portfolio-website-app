from aiogram.utils import executor

from tbot_app import dp
from tbot_app.keyboards.set_menu import set_main_menu

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=set_main_menu)

