from aiogram import types
from magic_filter import F
from tbot_app.app import dp
from tbot_app.data_dispatch import put_client, delete_client
from tbot_app.keyboards.pagination_keyboard import make_pagination_keyboard
from tbot_app.data_fetch import get_active_clients, get_archived_clients, get_client
from tbot_app.messages import CLIENT_ARCHIVED_MESSAGE, CLIENT_SKIPPED_MESSAGE, CLIENT_VIEW_MESSAGE, CLIENT_DELETE_MESSAGE
from tbot_app.paginator import ListPaginatorByOne

global client_paginator
client_paginator: ListPaginatorByOne
client_information: dict


@dp.message_handler(commands=['active_clients'])
async def process_view_clients_command(message_: types.Message):
    global client_paginator
    clients = await get_active_clients()
    client_paginator = ListPaginatorByOne(clients)
    data = client_paginator.next()
    if data is not None:
        await message_.reply(
            text=await format_client_info(data),
            reply_markup=make_pagination_keyboard(
                [{'<<': 'prev', 'Архивировать': 'archive_current',
                  client_paginator.position(): "f{client_paginator.position()}", '>>': 'next'}]
            )
        )


@dp.message_handler(commands=['archive_clients'])
async def process_view_clients_command(message_: types.Message):
    global client_paginator
    clients = await get_archived_clients()
    client_paginator = ListPaginatorByOne(clients)
    data = client_paginator.next()
    if data is not None:
        await message_.reply(
            text=await format_client_info(data),
            reply_markup=make_pagination_keyboard(
                [{'<<': 'prev', 'Удалить': 'delete',
                  client_paginator.position(): "f{client_paginator.position()}", '>>': 'next'}]
            )
        )


async def update_view_client(message_: types.Message, new_value):
    global client_paginator
    await message_.edit_text(
        text=await format_client_info(new_value),
        reply_markup=make_pagination_keyboard(
            [{'<<': 'prev', 'Архивировать': 'archive_current',
              client_paginator.position(): "f{client_paginator.position()}", '>>': 'next'}]
        )
    )


@dp.callback_query_handler(F.data == "prev")
async def archive_client(callback: types.CallbackQuery):
    global client_paginator
    data = client_paginator.prev()
    if data is not None:
        await update_view_client(callback.message, data)
    await callback.answer()


@dp.callback_query_handler(F.data == "next")
async def skip_client(callback: types.CallbackQuery):
    global client_paginator
    data = client_paginator.next()
    await update_view_client(callback.message, data)
    await callback.answer()


@dp.callback_query_handler(F.data == "delete")
async def delete_post_(callback: types.CallbackQuery):
    global client_paginator
    pk = client_paginator.value()['email']
    await delete_client(pk)
    await callback.message.reply(text=CLIENT_DELETE_MESSAGE)
    await callback.answer()


@dp.callback_query_handler(F.data == "archive_current")
async def archive_client(callback: types.CallbackQuery):
    global client_paginator
    pk = client_paginator.value()['email']
    client_data = await get_client(pk)
    client_data['state'] = 'AR'
    res = await put_client(pk, client_data)
    print(res)
    await update_view_client(callback.message, client_paginator.next())
    await callback.answer()


@dp.callback_query_handler(F.data == "archive")
async def archive_client(callback: types.CallbackQuery):
    data = {
        "email": "<N/A>"
    }
    entities = callback.message.entities or []
    for item in entities:
        if item.type in data.keys():
            data[item.type] = callback.message.text[item.offset: item.offset + item.length]
    client_data = await get_client(data['email'])
    client_data['state'] = 'AR'
    await put_client(data['email'], client_data)
    await callback.message.reply(text=CLIENT_ARCHIVED_MESSAGE)
    await callback.answer()


@dp.callback_query_handler(F.data == "skip")
async def skip_client(callback: types.CallbackQuery):
    await callback.message.reply(text=CLIENT_SKIPPED_MESSAGE)
    await callback.answer()


async def format_client_info(client):
    return CLIENT_VIEW_MESSAGE.format(name=client['name'],
                                      company=client['company'],
                                      telegram=client['telegram'],
                                      email=client['email'],
                                      additional_info=client['additional_info'])
