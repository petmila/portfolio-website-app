from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from tbot_app.app import dp
from tbot_app.data_dispatch import post_new_tag, delete_tag
from tbot_app.data_fetch import get_tags
from tbot_app.keyboards.inline_keyboard import make_inline_keyboard
from tbot_app.messages import TAG_VIEW_MESSAGE, TAGS_LIST_UPDATE_MESSAGE
from tbot_app.states import TagCreateStates


@dp.message_handler(state=TagCreateStates.add_info)
async def process_tag_info(message_: types.Message, state: FSMContext):
    await state.finish()
    old_tags = await get_tags()
    text = message_.text
    for tag in old_tags:
        if text.find(tag['name']) == -1:
            await delete_tag(tag['id'])
        text = text.replace(tag['name'], '').replace(tag['description'], '')

    for item in text.split('\n'):
        new_value = item.strip(': ')
        if new_value != '':
            new_value = new_value.split(':')
            await post_new_tag({'name': new_value[0].strip(' '), 'description': new_value[1].strip(' ')})

    await message_.reply(text=await format_tags(await get_tags()),
                         reply_markup=make_inline_keyboard({'update_portfolio': 'Редактировать'})
                         )


@dp.message_handler(commands=['tags'])
async def process_tags_command(message_: types.Message):
    tags = await get_tags()
    await message_.reply(
        text=await format_tags(tags),
        reply_markup=make_inline_keyboard({'update_tags': 'Редактировать'})
    )


async def format_tags(tags):
    formatted_tags = ''
    for tag in tags:
        formatted_tags += TAG_VIEW_MESSAGE.format(name=tag['name'],
                                                  description=tag['description'])
    return formatted_tags


@dp.callback_query_handler(F.data == "update_tags")
async def process_update_portfolio_command(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(TagCreateStates.add_info)
    await callback.message.reply(
        text=TAGS_LIST_UPDATE_MESSAGE
    )
    await callback.answer()
