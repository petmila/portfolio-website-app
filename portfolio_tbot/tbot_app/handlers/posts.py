from copy import copy

from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F
from tbot_app.app import dp
from tbot_app.data_dispatch import post_new_post, put_post, delete_post
from tbot_app.keyboards.pagination_keyboard import make_pagination_keyboard
from tbot_app.keyboards.checkbox_keyboard import make_checkbox_keyboard
from tbot_app.data_fetch import get_posts, get_tag, get_tags
from tbot_app.messages import POST_CREATION_MESSAGE, POST_CREATION_TAGS_MESSAGE, POST_CREATED_MESSAGE, \
    TAGS_LIST_MESSAGE, POST_VIEW_MESSAGE, POST_CREATION_KEY_PHRASE_MESSAGE, POST_UPDATE_MESSAGE, POST_DELETE_MESSAGE
from tbot_app.paginator import ListPaginatorByOne
from tbot_app.states import PostCreateStates

global post_paginator
post_paginator: ListPaginatorByOne
post_information: dict
tags_information: list[dict]


@dp.message_handler(commands=['create_post'])
async def process_create_post_command(message_: types.Message, state: FSMContext):
    global post_information
    post_information = {}
    await state.set_state(PostCreateStates.add_text)
    await message_.reply(text=POST_CREATION_MESSAGE)


@dp.message_handler(state=PostCreateStates.add_text)
async def process_post_key_phrase(message_: types.Message, state: FSMContext):
    global post_information, tags_information
    post_information['text'] = message_.text
    await state.set_state(PostCreateStates.add_key_phrase)
    await message_.reply(text=POST_CREATION_KEY_PHRASE_MESSAGE)


@dp.message_handler(state=PostCreateStates.add_key_phrase)
async def process_post_text(message_: types.Message, state: FSMContext):
    global post_information, tags_information
    post_information['key_phrase'] = message_.text
    post_information['tags'] = []
    await state.finish()
    tags_information = []
    tags_list = await get_tags()
    for tag in tags_list:
        new_tag = {'text': tag['name'], 'callback': tag['id'], 'check': False}
        tags_information.append(new_tag)
    await message_.reply(text=f'{POST_CREATION_TAGS_MESSAGE}',
                         reply_markup=make_checkbox_keyboard(tags_information)
                         )


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


@dp.callback_query_handler(F.data == "update")
async def update_post(callback: types.CallbackQuery, state: FSMContext):
    global post_paginator, post_information
    post_information = copy(post_paginator.value())

    await state.set_state(PostCreateStates.add_text)
    await callback.message.reply(text=POST_UPDATE_MESSAGE)
    await callback.answer()


@dp.callback_query_handler(F.data == "delete")
async def delete_post_(callback: types.CallbackQuery):
    global post_paginator
    post_id = post_paginator.value()['id']
    await delete_post(post_id)
    await callback.message.reply(text=POST_DELETE_MESSAGE)
    await callback.answer()


@dp.callback_query_handler(F.data.startswith('post_tag_checkbox__'))
async def checkbox_update(callback: types.CallbackQuery):
    global tags_information
    action = callback.data.split("__")[1]
    for i in range(len(tags_information)):
        if int(action) == int(tags_information[i]['callback']):
            if tags_information[i]['check'] is True:
                tags_information[i]['check'] = False
            else:
                tags_information[i]['check'] = True
    tags_information.append({'text': 'сохранить', 'callback': 'save'})
    await callback.message.edit_text(
        text=f"{TAGS_LIST_MESSAGE}",
        reply_markup=make_checkbox_keyboard(tags_information)
    )
    tags_information.pop()
    await callback.answer()


@dp.callback_query_handler(F.data == 'save')
async def checkbox_update(callback: types.CallbackQuery):
    global post_paginator, tags_information
    post_information['tags'] = [tag['callback'] for tag in tags_information]
    if 'id' in post_information:
        await put_post(post_information['id'], post_information)
    else:
        await post_new_post(post_information)
    await callback.message.reply(text=POST_CREATED_MESSAGE)
    await callback.answer()
