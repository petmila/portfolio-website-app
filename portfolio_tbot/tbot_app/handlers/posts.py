from copy import copy

from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F
from tbot_app.app import dp
from tbot_app.data_dispatch import post_new_post
from tbot_app.keyboards.pagination_keyboard import make_pagination_keyboard
from tbot_app.data_fetch import get_posts, get_tag, get_tags, get_post
from tbot_app.messages import POST_CREATION_MESSAGE, POST_CREATION_TAGS_MESSAGE, POST_CREATED_MESSAGE, \
    TAGS_LIST_MESSAGE, POST_VIEW_MESSAGE
from tbot_app.paginator import ListPaginatorByOne
from tbot_app.states import PostCreateStates

global post_paginator
post_paginator: ListPaginatorByOne
post_information: dict


@dp.message_handler(commands=['create_post'])
async def process_create_post_command(message_: types.Message, state: FSMContext):
    global post_information
    post_information = {}
    await state.set_state(PostCreateStates.add_text)
    await message_.reply(text=POST_CREATION_MESSAGE)


@dp.message_handler(state=PostCreateStates.add_text)
async def process_post_text(message_: types.Message, state: FSMContext):
    global post_information
    post_information['text'] = message_.text
    post_information['tags'] = []
    tags_list = await get_tags()
    await state.set_state(PostCreateStates.add_tags)
    await message_.reply(text=f'{POST_CREATION_TAGS_MESSAGE}\n{tags_list}')


@dp.message_handler(state=PostCreateStates.add_tags)
async def process_post_tags(message_: types.Message, state: FSMContext):
    global post_information
    if message_.text == 'save':
        await state.finish()
        post_information['key_phrase'] = post_information['text']
        await post_new_post(post_information)
        await message_.reply(text=POST_CREATED_MESSAGE)
    elif message_.text.startswith('+'):
        post_information['tags'].append(message_.text.split('+')[1])
        await message_.reply(
            text=TAGS_LIST_MESSAGE,
            reply_markup=make_pagination_keyboard(
                [{'сохранить': 'save'}]
            )
        )
    elif message_.text.startswith('-'):
        post_information['tags'].append(message_.text.split('-')[1])
        await message_.reply(text=TAGS_LIST_MESSAGE)


@dp.message_handler(commands=['view_posts'])
async def process_view_posts_command(message_: types.Message):
    global post_paginator
    posts = await get_posts()
    post_paginator = ListPaginatorByOne(posts)
    await message_.reply(
        text=await format_post(post_paginator.next()),
        parse_mode="HTML",
        reply_markup=make_pagination_keyboard(
            [{'<<': 'backward', post_paginator.position(): "f{post_paginator.position()}", '>>': 'forward'},
             {'Редактировать': 'update', 'Удалить': 'delete'}]
        )
    )


async def update_view_posts(message_: types.Message, new_value):
    global post_paginator
    await message_.edit_text(
        text=await format_post(new_value),
        reply_markup=make_pagination_keyboard(
            [{'<<': 'backward', post_paginator.position(): "f{post_paginator.position()}", '>>': 'forward'},
             {'Редактировать': 'update', 'Удалить': 'delete'}]
        )
    )

#
# async def update_view_posts_for_update(message_: types.Message):
#     global post_paginator
#     await message_.edit_text(
#         text=await format_post(new_value),
#         reply_markup=make_pagination_keyboard(
#             [{'<<': 'backward', post_paginator.position(): "f{post_paginator.position()}", '>>': 'forward'},
#              {'Редактировать': 'update', 'Удалить': 'delete'}]
#         )
#     )


async def format_post(post):
    tags = ''
    for tag_id in post['tags']:
        tag = await get_tag(tag_id)
        tags += f'# {tag["name"]}\n'
    return POST_VIEW_MESSAGE.format(key_phrase=post['key_phrase'],
                                    text=post['text'],
                                    datetime=post['datetime'],
                                    tags=tags)


@dp.callback_query_handler(F.data == "backward")
async def prev_post(callback: types.CallbackQuery):
    global post_paginator
    await update_view_posts(callback.message, post_paginator.prev())
    await callback.answer()


@dp.callback_query_handler(F.data == "forward")
async def next_post(callback: types.CallbackQuery):
    global post_paginator
    await update_view_posts(callback.message, post_paginator.next())
    await callback.answer()


# @dp.callback_query_handler(F.data == "update")
# async def prev_post(callback: types.CallbackQuery):
#     global post_paginator
#     # pk = post_paginator.value()['datetime']
#     post_information = copy(post_paginator.value())
#     # post_data = await get_post(pk)
#     # post_data['state'] = 'Archived'
#     res = await put_post(pk, post_data)
#     await update_view_client(callback.message, client_paginator.prev())
#     await update_view_posts(callback.message, post_paginator.prev())
#     await callback.answer()
#
#
# @dp.callback_query_handler(F.data == "delete")
# async def next_post(callback: types.CallbackQuery):
#     global post_paginator
#     await update_view_posts(callback.message, post_paginator.next())
#     await callback.answer()
