import logging
from .app import bot, dp
from .handlers import commands, posts, clients, portfolio, tags

logging.basicConfig(level=logging.DEBUG)
