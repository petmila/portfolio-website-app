import logging
from .app import bot, dp
from .handlers import commands, posts, clients

logging.basicConfig(level=logging.DEBUG)
