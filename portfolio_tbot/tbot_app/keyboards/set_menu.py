from aiogram import Dispatcher
from aiogram.types import BotCommand

LEXICON_COMMANDS_RU: dict[str, str] = {
    '/portfolio': 'command_1 desription',
    '/view_posts': 'command_2 desription',
    '/create_post': 'command_3 desription',
    '/active_clients': 'command_4 desription',
    '/archive_clients': 'command_4 desription',
    '/tags': 'command_4 desription',
}


async def set_main_menu(dispatcher: Dispatcher):
    main_menu_commands = [
        BotCommand(
            command=command,
            description=description
        ) for command, description in LEXICON_COMMANDS_RU.items()
    ]
    await dispatcher.bot.set_my_commands(main_menu_commands)