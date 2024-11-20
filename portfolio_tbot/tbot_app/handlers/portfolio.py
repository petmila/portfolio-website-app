from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from tbot_app.app import dp
from tbot_app.data_dispatch import put_portfolio
from tbot_app.data_fetch import get_portfolio
from tbot_app.keyboards.inline_keyboard import make_inline_keyboard
from tbot_app.messages import PORTFOLIO_UPDATE_MESSAGE, TAG_CREATION_MESSAGE, TAG_DELETED_MESSAGE, PORTFOLIO_MESSAGE
from tbot_app.states import TagCreateStates, PortfolioUpdateStates

#
# @dp.message_handler(commands=['create_tag'])
# async def process_create_tag_command(message_: types.Message, state: FSMContext):
#     await state.set_state(TagCreateStates.add_info)
#     await message_.reply(text=TAG_CREATION_MESSAGE)


@dp.message_handler(state=PortfolioUpdateStates.update_name)
async def process_tag_info(message_: types.Message, state: FSMContext):
    await state.finish()
    portfolio = await get_portfolio()
    name_portfolio_info = {'site_name': message_.text,
                           'site_description': portfolio['site_description'],
                           'about': portfolio['about'],
                           'service_list': portfolio['service_list']}
    await put_portfolio(name_portfolio_info)
    # await message_.reply(text=f'{TAG_CREATED_MESSAGE}')


@dp.message_handler(commands=['portfolio'])
async def process_portfolio_command(message_: types.Message):
    portfolio = await get_portfolio()
    await message_.reply(
        text=f'{PORTFOLIO_MESSAGE}\n{portfolio}',
    )


@dp.message_handler(commands=['update'])
async def process_update_portfolio_command(message_: types.Message):
    portfolio_fields = {'site_name': 'Название сайта', 'site_description': 'Описание сайта', 'about': 'Обо мне', 'service_list': 'Список услуг'}
    await message_.reply(
        text=PORTFOLIO_UPDATE_MESSAGE,
        reply_markup=make_inline_keyboard(portfolio_fields),
    )


# async def update_view_posts(message_: types.Message, new_value):
#     global paginator
#     await message_.edit_text(
#         text=new_value,
#         reply_markup=make_pagination_keyboard(
#             ['<<', paginator.position(), '>>']
#         )
#     )


@dp.callback_query_handler(F.data == "site_name")
async def update_site_name(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(PortfolioUpdateStates.update_name)
    await callback.message.reply('Введите новое имя для сайта')
    await callback.answer()


@dp.callback_query_handler(F.data == "site_description")
async def update_site_description(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(PortfolioUpdateStates.update_description)
    await callback.message.reply('Введите новое описание для сайта')
    await callback.answer()
