from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F
from tbot_app.app import dp
from tbot_app.data_dispatch import put_client
from tbot_app.keyboards.pagination_keyboard import make_pagination_keyboard
from tbot_app.data_fetch import get_active_clients, get_archived_clients, get_client
from tbot_app.messages import CLIENT_ARCHIVED_MESSAGE, CLIENT_SKIPPED_MESSAGE, POST_CREATED_MESSAGE, TAGS_LIST_MESSAGE
from tbot_app.paginator import ListPaginatorByOne

global client_paginator
client_paginator: ListPaginatorByOne
client_information: dict


# @dp.message_handler(commands=['create_post'])
# async def process_create_post_command(message_: types.Message, state: FSMContext):
#     global post_information
#     post_information = {}
#     await state.set_state(PostCreateStates.add_text)
#     await message_.reply(text=POST_CREATION_MESSAGE)


# @dp.message_handler(state=PostCreateStates.add_text)
# async def process_post_text(message_: types.Message, state: FSMContext):
#     global post_information
#     post_information['text'] = message_.text
#     post_information['tags'] = []
#     tags_list = await get_tags()
#     await state.set_state(PostCreateStates.add_tags)
#     await message_.reply(text=f'{POST_CREATION_TAGS_MESSAGE}\n{tags_list}')
#
#
# @dp.message_handler(state=PostCreateStates.add_tags)
# async def process_post_tags(message_: types.Message, state: FSMContext):
#     global post_information
#     if message_.text == 'save':
#         await state.finish()
#         post_information['key_phrase'] = post_information['text']
#         await post_new_post(post_information)
#         await message_.reply(text=POST_CREATED_MESSAGE)
#     elif message_.text.startswith('+'):
#         post_information['tags'].append(message_.text.split('+')[1])
#         await message_.reply(
#             text=TAGS_LIST_MESSAGE,
#             reply_markup=make_pagination_keyboard(
#                 {'сохранить': 'save'}
#             )
#         )
#     elif message_.text.startswith('-'):
#         post_information['tags'].append(message_.text.split('-')[1])
#         await message_.reply(text=TAGS_LIST_MESSAGE)


@dp.message_handler(commands=['active_clients'])
async def process_view_clients_command(message_: types.Message):
    global client_paginator
    clients = await get_active_clients()
    client_paginator = ListPaginatorByOne(clients)
    await message_.reply(
        text=client_paginator.next(),
        reply_markup=make_pagination_keyboard(
            {'<<': 'backward', 'Архивировать': 'archive_current', client_paginator.position(): "f{client_paginator.position()}", '>>': 'forward'}
        )
    )


async def update_view_client(message_: types.Message, new_value):
    global client_paginator
    await message_.edit_text(
        text=new_value,
        reply_markup=make_pagination_keyboard(
            {'<<': 'backward', 'Архивировать': 'archive_current', client_paginator.position(): "f{client_paginator.position()}", '>>': 'forward'}
        )
    )


@dp.callback_query_handler(F.data == "prev")
async def archive_client(callback: types.CallbackQuery):
    global client_paginator
    await update_view_client(callback.message, client_paginator.prev())
    await callback.answer()


@dp.callback_query_handler(F.data == "next")
async def skip_client(callback: types.CallbackQuery):
    global client_paginator
    await update_view_client(callback.message, client_paginator.next())
    await callback.answer()


@dp.callback_query_handler(F.data == "archive_current")
async def archive_client(callback: types.CallbackQuery):
    global client_paginator
    pk = client_paginator.value()['email']
    client_data = await get_client(pk)
    client_data['state'] = 'Archived'
    res = await put_client(pk, client_data)
    await update_view_client(callback.message, client_paginator.prev())
    await callback.answer()


@dp.callback_query_handler(F.data == "archive")
async def archive_client(callback: types.CallbackQuery):
    data = {
        "email": "<N/A>"
    }
    entities = callback.message.entities or []
    for item in entities:
        if item.type in data.keys():
            data[item.type] = callback.message.text[item.offset : item.offset+item.length]
    client_data = await get_client(data['email'])
    client_data['state'] = 'Archived'
    res = await put_client(data['email'], client_data)
    await callback.message.reply(text=CLIENT_ARCHIVED_MESSAGE)
    await callback.answer()


@dp.callback_query_handler(F.data == "skip")
async def skip_client(callback: types.CallbackQuery):
    await callback.message.reply(text=CLIENT_SKIPPED_MESSAGE)
    await callback.answer()
