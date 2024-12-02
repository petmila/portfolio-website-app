from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiohttp import ClientSession

from local_settings import API_KEY
from aiogram import Bot, Dispatcher, types


bot = Bot(token=API_KEY, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
AIOHTTP_SESSION = ClientSession()
