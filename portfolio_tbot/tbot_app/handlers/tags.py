from aiogram import types
from aiogram.dispatcher import FSMContext
from tbot_app.app import dp
from tbot_app.data_dispatch import post_new_tag
from tbot_app.data_fetch import get_tags
from tbot_app.messages import TAG_CREATED_MESSAGE, TAG_CREATION_MESSAGE, TAG_DELETED_MESSAGE
from tbot_app.states import TagCreateStates


@dp.message_handler(commands=['create_tag'])
async def process_create_tag_command(message_: types.Message, state: FSMContext):
    await state.set_state(TagCreateStates.add_info)
    await message_.reply(text=TAG_CREATION_MESSAGE)


@dp.message_handler(state=TagCreateStates.add_info)
async def process_tag_info(message_: types.Message, state: FSMContext):
    await state.finish()
    tag_info = {'name': message_.text, 'description': message_.text}
    await post_new_tag(tag_info)
    await message_.reply(text=f'{TAG_CREATED_MESSAGE}')


@dp.message_handler(commands=['tags'])
async def process_tags_command(message_: types.Message):
    tags = await get_tags()
    await message_.reply(
        text=tags,
    )


@dp.message_handler(commands=['delete_tag'])
async def process_delete_tag_command(message_: types.Message, state: FSMContext, args):
    print(args)
    await message_.reply(text=f'{TAG_DELETED_MESSAGE}')

# async def update_view_posts(message_: types.Message, new_value):
#     global paginator
#     await message_.edit_text(
#         text=new_value,
#         reply_markup=make_pagination_keyboard(
#             ['<<', paginator.position(), '>>']
#         )
#     )


# @dp.callback_query_handler(F.data == "backward")
# async def prev_post(callback: types.CallbackQuery):
#     global paginator
#     await update_view_posts(callback.message, paginator.prev())
#     await callback.answer()
#
#
# @dp.callback_query_handler(F.data == "forward")
# async def next_post(callback: types.CallbackQuery):
#     global paginator
#     await update_view_posts(callback.message, paginator.next())
#     await callback.answer()
